output "ui_bucket" {
  description = "S3 bucket for UI hosting"
  value       = aws_s3_bucket.ui.bucket
}

output "ui_url" {
  description = "Static website endpoint for UI"
  value       = aws_s3_bucket_website_configuration.ui.website_endpoint
}

output "api_url" {
  description = "API Gateway endpoint"
  value       = aws_apigatewayv2_api.api.api_endpoint
}
