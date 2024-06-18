terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  access_key = ""
  secret_key = "" 
}

resource "aws_s3_bucket" "bucket" {
  bucket = "viveksnewbucket1234"

  tags = {
    Name        = "My bucket"
  }
}

resource "aws_s3_bucket_object" "file" {
  bucket = aws_s3_bucket.bucket.id
  key    = "hello.txt"
  source = "/Users/vivekmodi/Desktop/AWS_ETL/hello.txt"
}