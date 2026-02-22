resource "aws_lambda_layer_version" "pdf_layer" {
  filename            = "../../app/layers/layer.zip"
  layer_name          = "${local.prefix}-layer"
  compatible_runtimes = ["python3.11"]

  source_code_hash = filebase64sha256("../../app/layers/layer.zip")
}
