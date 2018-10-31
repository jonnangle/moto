import boto3

"""
What about this one, how should we test this?
"""
def delete_zip_files(bucket='mybucket'):
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(bucket)
    for f in s3bucket.objects.all():
      if f.key.endswith('.zip'):
        f.remove()