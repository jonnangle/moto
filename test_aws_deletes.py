import boto3

def delete_zip_files(bucket='mybucket'):
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(bucket)
    for f in s3bucket.objects.all():
      if f.key.endswith('.zip'):
        f.remove()

from moto import mock_s3

@mock_s3
def test_delete_zip_files():
  # Set up our pre-requisites - a bucket, and some files
  BUCKET='my-test-bucket'
  s3 = boto3.resource('s3')
  s3.create_bucket(Bucket=BUCKET)

  for filename in ['file1.zip', 'file2.zip', 'file3.gif']:
    s3_object = s3.Object(BUCKET, filename)
    s3_object.put(Body="")

  # We really do have 3 files in the mocked bucket now!
  s3bucket = s3.Bucket(BUCKET)
  assert len(list(s3bucket.objects.all())) == 3

  # Run our function under test to delete the .zip files
  delete_zip_files(bucket=BUCKET)

  # Now see what things look like now!
  remaining_files = list(s3bucket.objects.all())
  assert len(remaining_files) == 1
  assert remaining_files[0].key == "file3.gif"