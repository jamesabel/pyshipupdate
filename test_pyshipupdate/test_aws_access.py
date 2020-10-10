import os

from awsimple import S3Access, use_moto_mock_env_var

from pyshipupdate import __application_name__


def test_aws_access(is_mocked):

    # test basic AWS access

    bucket_name = __application_name__
    s3_key = "test.txt"
    s3_value = "hi"

    s3_access = S3Access(bucket_name)
    assert s3_access.is_mocked() == is_mocked
    s3_access.create_bucket()  # when mocking always have to create the bucket
    s3_access.write_string(s3_value, s3_key)
    assert s3_access.read_string(s3_key) == s3_value
