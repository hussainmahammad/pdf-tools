import boto3
import json
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']
TMP_DIR = "/tmp/"

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
}

# Download files from S3
def download_files(keys):
    paths = []
    for key in keys:
        filename = key.split("/")[-1]
        path = os.path.join(TMP_DIR, filename)
        s3.download_file(BUCKET, key, path)
        paths.append(path)
    return paths

# Extract base filename from S3 key
def get_base_name(key):
    filename = key.split("/")[-1]
    return os.path.splitext(filename)[0]

# Upload with custom filename
def upload_and_get_url(path, filename):
    output_key = f"outputs/{filename}"
    s3.upload_file(path, BUCKET, output_key)

    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': BUCKET,
            'Key': output_key,
            'ResponseContentDisposition': f'attachment; filename="{filename}"'
        },
        ExpiresIn=600
    )
    return url


def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        operation = body.get("operation")
        files = body.get("files", [])
        password = body.get("password", "")
        ranges_input = body.get("ranges", "").strip()

        if not files:
            return {
                "statusCode": 400,
                "headers": HEADERS,
                "body": json.dumps({"error": "No files provided"})
            }

        base_name = get_base_name(files[0])
        local_files = download_files(files)
        output_path = os.path.join(TMP_DIR, "output.pdf")

        # -------- MERGE --------
        if operation == "merge":
            merger = PdfMerger()
            for file in local_files:
                merger.append(file)
            merger.write(output_path)
            merger.close()

            filename = f"{base_name}_merged.pdf"
            url = upload_and_get_url(output_path, filename)
            result = {"download_url": url}

        # -------- SPLIT --------
        elif operation == "split":
            reader = PdfReader(local_files[0])
            total_pages = len(reader.pages)
            urls = []

            if total_pages < 2:
                return {
                    "statusCode": 400,
                    "headers": HEADERS,
                    "body": json.dumps({"error": "PDF must have at least 2 pages to split"})
                }

            # Case 1: User provided ranges
            if ranges_input:
                try:
                    parts = ranges_input.split(",")
                    file_index = 1

                    for part in parts:
                        part = part.strip()
                        writer = PdfWriter()

                        if "-" in part:
                            start, end = part.split("-")
                            start = int(start)
                            end = int(end)
                        else:
                            start = end = int(part)

                        if start < 1 or end > total_pages or start > end:
                            return {
                                "statusCode": 400,
                                "headers": HEADERS,
                                "body": json.dumps({"error": f"Invalid range: {part}"})
                            }

                        for page_num in range(start - 1, end):
                            writer.add_page(reader.pages[page_num])

                        split_path = os.path.join(TMP_DIR, f"split_{file_index}.pdf")
                        with open(split_path, "wb") as f:
                            writer.write(f)

                        filename = f"{base_name}_split_{file_index}.pdf"
                        urls.append(upload_and_get_url(split_path, filename))
                        file_index += 1

                except Exception:
                    return {
                        "statusCode": 400,
                        "headers": HEADERS,
                        "body": json.dumps({"error": "Invalid range format. Use example: 1-5,8,10-15"})
                    }

            # Case 2: No ranges → Split into equal halves
            else:
                mid = total_pages // 2

                writer1 = PdfWriter()
                for i in range(0, mid):
                    writer1.add_page(reader.pages[i])

                path1 = os.path.join(TMP_DIR, "half1.pdf")
                with open(path1, "wb") as f:
                    writer1.write(f)

                urls.append(upload_and_get_url(path1, f"{base_name}_part1.pdf"))

                writer2 = PdfWriter()
                for i in range(mid, total_pages):
                    writer2.add_page(reader.pages[i])

                path2 = os.path.join(TMP_DIR, "half2.pdf")
                with open(path2, "wb") as f:
                    writer2.write(f)

                urls.append(upload_and_get_url(path2, f"{base_name}_part2.pdf"))

            result = {"files": urls}

        # -------- UNLOCK --------
        elif operation == "unlock":
            reader = PdfReader(local_files[0])

            if reader.is_encrypted:
                if not password:
                    return {
                        "statusCode": 400,
                        "headers": HEADERS,
                        "body": json.dumps({"error": "Password required for unlock"})
                    }
                reader.decrypt(password)

            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with open(output_path, "wb") as f:
                writer.write(f)

            filename = f"{base_name}_unlocked.pdf"
            url = upload_and_get_url(output_path, filename)
            result = {"download_url": url}

        # -------- LOCK --------
        elif operation == "lock":
            if not password:
                return {
                    "statusCode": 400,
                    "headers": HEADERS,
                    "body": json.dumps({"error": "Password required for lock"})
                }

            reader = PdfReader(local_files[0])
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(password)

            with open(output_path, "wb") as f:
                writer.write(f)

            filename = f"{base_name}_locked.pdf"
            url = upload_and_get_url(output_path, filename)
            result = {"download_url": url}

        else:
            return {
                "statusCode": 400,
                "headers": HEADERS,
                "body": json.dumps({"error": "Invalid operation"})
            }

        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": HEADERS,
            "body": json.dumps({"error": str(e)})
        }
