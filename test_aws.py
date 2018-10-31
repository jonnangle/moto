import boto3

def list_zip_files(bucket='mybucket'):
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(bucket)
    zips = [f for f in s3bucket.objects.all() if f.key.endswith('zip')]
    return zips

from mock import patch, Mock

@patch('boto3.resource')
def test_list_keys_with_default_bucket(mock):
    mock.return_value.Bucket.return_value.objects.all.return_value = [Mock(key='file1.zip'), Mock(key='file2.zip'), Mock(key='file3.zip')]

    ziplist = list_zip_files()
    mock.assert_called_with('s3')
    mock().Bucket.assert_called_with('mybucket')
    assert len(ziplist) == 3

@patch('boto3.resource')
def test_list_keys_with_default_bucket_finds_zipfiles(mock):
    mock.return_value.Bucket.return_value.objects.all.return_value = [Mock(key='file1.txt'), Mock(key='file2.png'), Mock(key='file3.zip')]

    ziplist = list_zip_files()
    mock.assert_called_with('s3')
    mock().Bucket.assert_called_with('mybucket')
    assert len(ziplist) == 1

@patch('boto3.resource')
def test_list_keys_with_bucket_name_calls_correct_bucket(mock):

    ziplist = list_zip_files(bucket='someotherbucket')

    mock.assert_called_with('s3')
    mock().Bucket.assert_called_with('someotherbucket')