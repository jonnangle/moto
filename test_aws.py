import boto3

"""
How do we test this code?
"""
def list_zip_files(bucket='mybucket'):
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(bucket)
    zips = [f for f in s3bucket.objects.all() if f.key.endswith('zip')]
    return zips