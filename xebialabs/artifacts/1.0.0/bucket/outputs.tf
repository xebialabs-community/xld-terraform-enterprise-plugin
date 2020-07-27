output "bucket_id" {
  value = "${aws_s3_bucket.bucket.id}"
}

output "bucket_arn" {
  value = "${aws_s3_bucket.bucket.arn}"
}

output "db_password" {
  value       = "AZERTYUIOP"
  description = "The password for logging in to the database."
  sensitive   = true
}
