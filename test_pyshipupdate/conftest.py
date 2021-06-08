import os
import pytest
from pathlib import Path
from tempfile import mkdtemp
import shutil

from awsimple import use_moto_mock_env_var

from pyshipupdate import UpdaterAwsS3, rmdir, __author__, CLIP_EXT

from test_pyshipupdate import TstDirs, test_name

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
    rmdir(TstDirs.app_dir)
    if is_mocked_flag:
        os.environ[use_moto_mock_env_var] = "1"
    updater = UpdaterAwsS3(test_name, __author__)
    updater.profile_name = "pyshiptest"
    updater.create_bucket()
    for version in ["0.0.1", "0.0.2"]:
        clip_name = f"{test_name}_{version}"
        clip_file_path = Path(TstDirs.app_dir, clip_name, f"{clip_name}.txt")  # just some file for now - not real clip contents to keep it small
        clip_file_path.parent.mkdir(parents=True, exist_ok=True)
        clip_file_path.write_text(version)

        # zip the clip dir
        temp_dir = mkdtemp()
        zip_file_path = Path(shutil.make_archive(Path(temp_dir, clip_file_path.parent.name), "zip", str(clip_file_path.parent)))

        # make_archive uses a .zip file extension but we want .clip
        clip_file_path = Path(zip_file_path.parent, f"{zip_file_path.stem}.{CLIP_EXT}")
        shutil.move(zip_file_path, clip_file_path)

        updater.upload(clip_file_path, clip_file_path.name)

    yield updater
    clear_mock_env_var()
