terraform {
  required_providers {
    yandex = {
      source = "terraform-providers/yandex"
    }
  }
}

provider "yandex" {
  token     = "<OAuth-token>" # get using yc iam access-key create --service-account-name service-account-for-cf 
  cloud_id  = "<CLOUD-ID>" # your public service account key
  folder_id = "<FOLDER-ID>" # your secret service account key
}

resource "yandex_storage_bucket" "bucket" {
  access_key = "<ACCESS-KEY>"
  secret_key = "<SECRET-KEY>"
  bucket = "alekseyen-bucket-for-trigger" # your bucket name
} 
