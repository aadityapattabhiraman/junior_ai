#!/usr/bin/env python3

import boto3


s3 = boto3.client("s3")
file = ""
bucket = ""
key = ""

s3.upload_file(file, bucket, key)
