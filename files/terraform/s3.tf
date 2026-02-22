resource "aws_s3_bucket" "ui" {
  bucket = "${var.project}-${var.env}-ui"
}

resource "aws_s3_bucket_public_access_block" "ui" {
  bucket = aws_s3_bucket.ui.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_website_configuration" "ui" {
  bucket = aws_s3_bucket.ui.id

  index_document {
    suffix = "index.html"
  }
}

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

# Processing bucket
resource "aws_s3_bucket" "files" {
  bucket = "${var.project}-${var.env}-files"
}
