<div align="center">

# PDFTools

_All-in-One PDF Tools — Lock, Unlock, Merge & Split PDFs directly in your browser_

![AWS](https://img.shields.io/badge/AWS-Serverless-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?style=flat-square)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red?style=flat-square)

**Lock PDF · Unlock PDF · Merge PDF · Split PDF**

</div>

![PDFTools Architecture](docs/architecture.png)

## Key Features

- **Lock PDF:** Protect PDF files with a password
- **Unlock PDF:** Remove password protection from PDF files
- **Merge PDF:** Combine multiple PDF files into one
- **Split PDF:** Split PDF files into separate files
- **Simple Interface:** Select a tool, upload your PDF, process it, and download the result
- **Serverless:** Built using AWS serverless services with no traditional application server

## How It Works

PDFTools uses a simple serverless workflow:

1. The user opens the PDFTools website hosted on **Amazon S3**.
2. The user selects **Lock, Unlock, Merge, or Split** and uploads the required PDF file.
3. The browser sends the request to **Amazon API Gateway**.
4. API Gateway routes the request to the appropriate **AWS Lambda** function.
5. Lambda handles the upload or PDF processing operation.
6. PDF files are stored in **Amazon S3** during the processing workflow.
7. The processed PDF is returned to the user for download.

## AWS Services

- **Amazon S3** — Static website hosting and PDF file storage
- **Amazon API Gateway** — HTTP API for the frontend
- **AWS Lambda** — Upload and PDF processing functions
- **AWS Lambda Layer** — PDF processing dependencies
- **AWS IAM** — Lambda permissions and access control

## Infrastructure & Deployment

- **Terraform** — Provisions and manages AWS infrastructure
- **Jenkins** — Automates application deployment
- **AWS CLI** — Used for deployment operations

The deployment pipeline automatically:

1. Packages the Lambda functions
2. Runs Terraform
3. Creates or updates AWS resources
4. Configures the API URL
5. Uploads the frontend to the S3 website bucket

A separate Jenkins pipeline is provided to destroy the Terraform-managed infrastructure.

## Project Structure

```text
app/
├── functions/
│   ├── upload/
│   │   └── lambda_function.py
│   └── process/
│       └── lambda_function.py
├── layers/
│   └── layer.zip
└── ui/
    ├── icons/
    ├── index.html
    └── style.css

Jenkinsfile.deploy
Jenkinsfile.destroy
