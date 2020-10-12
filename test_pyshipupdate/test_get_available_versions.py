
from awsimple import S3Access

from pyshipupdate import UpdaterAwsS3

from test_pyshipupdate import test_name


def test_get_available_versions(updater_fixture):

    # todo: add list_buckets to AWSimple
    buckets = updater_fixture.bucket_list()
    print(f"{buckets=}")
    available_versions = updater_fixture.get_available_versions()
    print(available_versions)
