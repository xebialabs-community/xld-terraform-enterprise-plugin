output "bucket_id" {
  value = "${aws_s3_bucket.bucket.id}"
}

output "bucket_backup_id" {
  value = "${aws_s3_bucket.bucket_backup.id}"
}
