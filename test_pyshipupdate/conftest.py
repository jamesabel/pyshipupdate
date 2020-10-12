import os
import pytest
from pathlib import Path
from semver import VersionInfo

from awsimple import use_moto_mock_env_var

from pyshipupdate import UpdaterAwsS3, rmdir

from test_pyshipupdate import TestDirs, test_name

is_mocked_flag = True  # set to True to tell awsimple to use moto mock

print(f"{is_mocked_flag=}")


@pytest.fixture(scope="session", autouse=True)
def options():
    print(f"{is_mocked_flag=}")


@pytest.fixture(autouse=True)
def updater_fixture():

    def clear_mock_env_var():
        try:
            del os.environ[use_moto_mock_env_var]
        except KeyError:
            pass

    # make and upload fake test clips (not real clip contents)
    rmdir(TestDirs.clips)
    if is_mocked_flag:
        os.environ[use_moto_mock_env_var] = "1"
    updater = UpdaterAwsS3(test_name)
    updater.create_bucket()
    for version in ["0.0.1", "0.0.2"]:
        clip_name = f"{test_name}_{version}"
        clip_file_path = Path(TestDirs.clips, clip_name, f"{clip_name}.txt")  # just some file for now - not real clip contents to keep it small
        clip_file_path.parent.mkdir(parents=True, exist_ok=True)
        clip_file_path.write_text(version)
        updater.release(VersionInfo.parse(version), clip_file_path.parent)

    yield updater
    clear_mock_env_var()
