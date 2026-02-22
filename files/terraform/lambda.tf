# Upload function
resource "aws_lambda_function" "upload" {
  function_name = "${var.project}-upload-function"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.11"
  handler       = "lambda_function.lambda_handler"

  filename = "../../app/functions/upload.zip"

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.files.bucket
    }
  }
}

# Process function
resource "aws_lambda_function" "process" {
  function_name = "${var.project}-process-function"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.11"
  handler       = "lambda_function.lambda_handler"

  filename = "../../app/functions/process.zip"

  layers = [aws_lambda_layer_version.pdf_layer.arn]

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.files.bucket
    }
  }
}
