from semver import VersionInfo
from pathlib import Path

from test_pyshipupdate import TstDirs


def test_update_not_new(updater_fixture):
    current_version = "0.0.2"  # 0.0.2 is the most recent, so no update will occur
    updater_success = updater_fixture.update(VersionInfo.parse(current_version))
    assert not updater_success  # no update


def test_update_new(updater_fixture):
    current_version = "0.0.1"  # we'll have 0.0.1 and 0.0.2 available, so we'll have a new version
    s3_objects = updater_fixture.dir()
    print(s3_objects)
    updater_success = updater_fixture.update(VersionInfo.parse(current_version), TstDirs.app_dir)
    assert updater_success  # did update
    updated_clip = "testpyshipupdate_0.0.2"
    assert Path(TstDirs.app_dir, updated_clip, f"{updated_clip}.txt").exists()  # ensure we put the contents in the correct place
    assert not Path(TstDirs.app_dir, f"{updated_clip}.clip").exists()  # ensure we deleted the clip after it was unzipped
