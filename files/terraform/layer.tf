resource "aws_lambda_layer_version" "pdf_layer" {
  filename            = "../../app/layers/layer.zip"
  layer_name          = "${var.project}-layer"
  compatible_runtimes = ["python3.11"]
}
