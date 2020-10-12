from semver import VersionInfo


def test_update_not_new(updater_fixture):
    current_version = "0.0.2"  # 0.0.2 is the most recent, so no update will occur
    updater_success = updater_fixture.update(VersionInfo.parse(current_version))
    assert not updater_success  # no update


def test_update_new(updater_fixture):
    current_version = "0.0.1"  # we'll have 0.0.1 and 0.0.2 available, so we'll have a new version
    s3_objects = updater_fixture.dir()
    print(s3_objects)
    updater_success = updater_fixture.update(VersionInfo.parse(current_version))
    assert updater_success  # update
