// Create a variable for our domain name because we'll be using it a lot.
variable "www_domain_name" {
  default = "www.runatlantis.io"
}

// We'll also need the root domain (also known as zone apex or naked domain).
variable "root_domain_name" {
  default = "runatlantis.io"
}

// We'll also need the root domain (also known as zone apex or naked domain).
variable "aws_region" {
  default = "paris"
}