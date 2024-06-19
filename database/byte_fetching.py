#!/usr/bin/env python3

import boto3


s3 = boto4.client("s3")
bucket = ""
kwy = ""

brange = ["bytes=0-99", "bytes=100-199", "bytes=200-299"]

parts = []

for byte_range in byte_ranges:

    response = s3.get_object(Bucket=bucket, Key=key, Range=brange)
    parts.append(response["Body"].read())

complete_file = b"".join(parts)

with open("output_file", "wb") as f:
    f.write(complete_file)
