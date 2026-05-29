terraform {
  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    # Required for time_sleep
    time = {
      source  = "hashicorp/time"
      version = "~> 0.9"
    }

    # Required for random_id
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  backend "s3" {
    bucket  = "tfstates-hussainmahammad.online"
    key     = "pdf-tools/prod.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.region
}
