terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "petcart-terraform-state-867809929056"
    key            = "pdf-tools/prod.tfstate"
    region         = "us-east-1"
    encrypt        = true
    # Uncomment if your other projects use state locking
    # dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.region
}
