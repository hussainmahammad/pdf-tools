variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "pdf-tools"
}

variable "owner" {
  description = "Owner name (used for global uniqueness)"
  type        = string
  default     = "hussain"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "prod"
}

variable "build_id" {
  description = "Jenkins build number for unique resource naming"
  type        = string
}
