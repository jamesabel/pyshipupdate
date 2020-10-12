from dataclasses import dataclass
from pathlib import Path
from tempfile import mkdtemp
import shutil
from semver import VersionInfo
import time
from datetime import datetime
import json

from balsa import get_logger
from awsimple import S3Access

from pyshipupdate import Updater, __application_name__, version_from_clip_zip, CLIP_EXT

log = get_logger(__application_name__)


@dataclass
class UpdaterAwsS3(Updater, S3Access):
    """
    pyship updater via AWS S3
    """

    def __init__(self, target_app_name):
        S3Access.__init__(self, target_app_name)
        Updater.__init__(self, target_app_name)

    def get_available_versions(self):
        available_versions = []
        for s3_key in self.dir():
            version = version_from_clip_zip(self.target_app_name, s3_key)
            if version is not None:
                available_versions.append(version)
        available_versions.sort()
        return available_versions

    def install_clip(self, version: VersionInfo, destination_dir: Path) -> bool:
        return True

    def release(self, version: VersionInfo, clip_dir_path: Path):

        self.create_bucket()  # just in case the S3 bucket doesn't exist

        # zip the clip dir
        temp_dir = mkdtemp()
        zip_file_path = Path(shutil.make_archive(Path(temp_dir, clip_dir_path.name), "zip", str(clip_dir_path)))

        # make_archive uses a .zip file extension but we want .clip
        clip_file_path = Path(zip_file_path.parent, f"{zip_file_path.stem}.{CLIP_EXT}")
        shutil.move(zip_file_path, clip_file_path)

        self.upload(clip_file_path, clip_file_path.name)
        ts = time.time()
        app_info = {"app_name": self.target_app_name, "version": str(version), "release_timestamp": ts, "release_timestamp_human": datetime.fromtimestamp(ts).isoformat()}
        self.write_string(json.dumps(app_info), f"{self.target_app_name}.json")
