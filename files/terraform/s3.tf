/* ================= UI BUCKET ================= */

resource "aws_s3_bucket" "ui" {
  bucket = "${local.prefix}-ui"
}

/* Public access settings */

resource "aws_s3_bucket_public_access_block" "ui" {
  bucket = aws_s3_bucket.ui.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

/* Static website hosting */

resource "aws_s3_bucket_website_configuration" "ui" {
  bucket = aws_s3_bucket.ui.id

  index_document {
    suffix = "index.html"
  }
}

/* Public read policy */

resource "aws_s3_bucket_policy" "ui_public" {
  bucket = aws_s3_bucket.ui.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = "*"
      Action = "s3:GetObject"
      Resource = "${aws_s3_bucket.ui.arn}/*"
    }]
  })
}

/* ================= UI CORS (IMPORTANT) ================= */

resource "aws_s3_bucket_cors_configuration" "ui_cors" {
  bucket = aws_s3_bucket.ui.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    expose_headers  = []
    max_age_seconds = 3000
  }
}


/* ================= FILE PROCESSING BUCKET ================= */

resource "aws_s3_bucket" "files" {
  bucket = "${local.prefix}-files"
}

/* Files bucket CORS (matches your manual config) */

resource "aws_s3_bucket_cors_configuration" "files_cors" {
  bucket = aws_s3_bucket.files.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "GET", "POST", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = []
  }
}
