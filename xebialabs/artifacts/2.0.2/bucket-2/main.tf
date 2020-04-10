terraform {
  required_version = ">= 0.11.0"
}

provider "aws" {
  region = "${var.aws_region}"
}

resource "aws_s3_bucket" "bucket_backup" {
  bucket = "${var.bucket_name}-backup"
  acl    = "public-read"

  tags = {
    Name        = "${var.bucket_name}-backup"    
  }
}

