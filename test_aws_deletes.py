import boto3

def delete_zip_files(bucket='mybucket'):
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(bucket)
    for f in s3bucket.objects.all():
      if f.key.endswith('.zip'):
        f.remove()

from mock import patch, Mock

@patch('boto3.resource')
def test_delete_zip_files(mock):
  # Create three mocks - two zipfiles, one non-zipfile
  zipfile1mock = Mock(key='file1.zip')
  zipfile2mock = Mock(key='file2.zip')
  nonzipfilemock = Mock(key='file3.gif')

  s3_bucket_files = [zipfile1mock, zipfile2mock, nonzipfilemock]
  mock.return_value.Bucket.return_value.objects.all.return_value = s3_bucket_files

  delete_zip_files()

  # we want to delete these
  zipfile1mock.remove.assert_called()
  zipfile2mock.remove.assert_called()

  # we DON'T want to delete this one!
  nonzipfilemock.remove.assert_not_called()