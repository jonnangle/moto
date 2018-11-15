import boto3
import requests

BUCKETNAME='jon-my-bucket-s3'

def populate_fastly_acl_s3_object(url='https://api.fastly.com/public-ip-list', bucket=BUCKETNAME, object="fastly-public-ip-list.txt"):
  s3 = boto3.resource('s3')
  s3bucket = s3.Bucket(bucket)

  json = requests.get(url).json()
  body = "\n".join(json["addresses"])

  s3bucket.put_object(
    Key=object,
    Body=body,
  )