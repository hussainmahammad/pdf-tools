output "ui_bucket" {
  value = aws_s3_bucket.ui.bucket
}

output "ui_url" {
  value = aws_s3_bucket_website_configuration.ui.website_endpoint
}

output "api_url" {
  value = aws_apigatewayv2_api.api.api_endpoint
}
