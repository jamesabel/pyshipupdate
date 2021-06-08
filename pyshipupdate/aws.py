from dataclasses import dataclass
from pathlib import Path
from tempfile import mkdtemp
import shutil
import os
from semver import VersionInfo
from typing import List
import zipfile

from balsa import get_logger
from awsimple import S3Access
from awsimple.s3 import BucketNotFound
from typeguard import typechecked

from pyshipupdate import Updater, __application_name__, version_from_clip_zip, CLIP_EXT, create_bucket_name

log = get_logger(__application_name__)


@dataclass
class UpdaterAwsS3(Updater, S3Access):
    """
    pyship updater via AWS S3
    """

    def __init__(self, target_app_name: str, target_app_author: str):
        Updater.__init__(self, target_app_name, target_app_author)
        S3Access.__init__(self, create_bucket_name(target_app_name, target_app_author))

    @typechecked
    def get_available_versions(self) -> List[VersionInfo]:
        available_versions = []
        try:
            bucket_dir = self.dir()
        except BucketNotFound as e:
            log.info(f"Bucket not found,{self.bucket_name=},{e}")  # may want to make this a warning
            bucket_dir = {}
        for s3_key in bucket_dir:
            version = version_from_clip_zip(self.target_app_name, s3_key)
            if version is not None:
                available_versions.append(version)
        available_versions.sort()
        return available_versions

    @typechecked
    def install_clip(self, version: VersionInfo, destination_dir: Path) -> bool:
        clip_name = f"{self.target_app_name}_{str(version)}"
        s3_key = f"{clip_name}.{CLIP_EXT}"
        download_path = Path(destination_dir, s3_key)
        extract_path = Path(destination_dir, clip_name)
        if self.object_exists(s3_key):
            self.download_cached(s3_key, download_path)
            log.info(f"extracting {download_path} ({download_path.absolute()}) to {extract_path} ({extract_path.absolute()})")
            with zipfile.ZipFile(download_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            log.info(f"removing {download_path} ({download_path.absolute()})")
            os.remove(download_path)
            install_success = True
        else:
            log.warning(f"{self.bucket_name}/{s3_key} not found")
            install_success = False
        return install_success
