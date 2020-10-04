import os

import pytest
from moto import mock_s3
from awsimple import S3Access

from pyshipupdate import __application_name__


@mock_s3
@pytest.fixture(scope="session", autouse=True)
def init_s3():
    s3_key = "test.txt"
    s3 = S3Access(__application_name__)
    account_id = s3.get_account_id()
    print(f"{account_id=}")
    created = s3.create_bucket()
    print(f"{created=}")
    s3.write_string("hi", s3_key)
    read_string = s3.read_string(s3_key)
    print(f"{read_string=}")


@pytest.fixture(scope='function', autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
