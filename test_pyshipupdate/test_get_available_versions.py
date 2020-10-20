from semver import VersionInfo


def test_get_available_versions(updater_fixture):

    buckets = updater_fixture.bucket_list()
    print(f"{buckets=}")
    available_versions = updater_fixture.get_available_versions()
    print(available_versions)
    assert VersionInfo.parse("0.0.1") in available_versions
