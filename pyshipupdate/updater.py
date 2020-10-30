from abc import ABC, abstractmethod
from pathlib import Path
from enum import Enum
from typing import List

from semver import VersionInfo
from appdirs import user_data_dir
from typeguard import typechecked
from balsa import get_logger

from pyshipupdate import __application_name__

log = get_logger(__application_name__)


class PreReleaseTypes(Enum):
    test = "test"
    dev = "dev"
    alpha = "alpha"
    beta = "beta"


class Updater(ABC):
    """
    pyship updater
    Updates a pyship app to its latest released version.  Instantiated and called by a running pyship app.
    """

    def __init__(self, target_app_name: str, target_app_author: str, allowed_pre_release: List[PreReleaseTypes] = None):
        self.target_app_name = target_app_name
        self.target_app_author = target_app_author
        self.allowed_pre_release = allowed_pre_release  # test, dev, beta, etc.

    @abstractmethod
    def get_available_versions(self) -> List[VersionInfo]:
        """
        get available versions
        """
        ...

    @abstractmethod
    def install_clip(self, version: VersionInfo, destination_dir: Path) -> bool:
        """
        put a clip into a destination dir
        :param version: version of clip to get
        :param destination_dir: dir to put the clip
        :return: True if were able to get the clip, False otherwise
        """
        ...

    @typechecked(always=True)
    def get_greatest_version(self) -> (VersionInfo, None):
        """
        determine the greatest version and return it
        :return: the greatest version, or None if no versions available
        """
        available_versions = self.get_available_versions()
        log.debug(f"{available_versions=}")
        if len(available_versions) == 0:
            greatest_version = None
        else:
            greatest_version = sorted(available_versions)[-1]
        log.info(f"{greatest_version=}")
        return greatest_version

    @typechecked(always=True)
    def update(self, current_version: (str, VersionInfo), app_dir: Path = None) -> bool:
        """
        update this (the target) application (clip dir)
        :param current_version: current version of the running app (both string and VersionInfo allowed)
        :param app_dir: destination directory or None to use the user data area
        """

        if app_dir is None:
            app_dir = Path(user_data_dir(self.target_app_name, self.target_app_author))

        did_update = False
        if isinstance(current_version, str):
            current_version = VersionInfo.parse(current_version)
        log.info(f"{current_version=}")
        greatest_version = self.get_greatest_version()
        log.info(f"{greatest_version=}")
        if greatest_version is not None and greatest_version > current_version:
            app_dir.mkdir(parents=True, exist_ok=True)
            did_update = self.install_clip(greatest_version, app_dir)
        return did_update

    @abstractmethod
    def release(self, version: VersionInfo, clip_dir_path: Path):
        """
        Release a new app version.  Uploads the clip file to the cloud and sets the new app version file.
        :param version: new app version
        :param clip_dir_path: path to clip file ("zipped" clip directory)
        """
        ...
