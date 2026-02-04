from typing import Union
from semver import VersionInfo

from typeguard import typechecked
from balsa import get_logger

from pyshipupdate import CLIP_EXT, __application_name__

log = get_logger(__application_name__)


@typechecked
def version_from_clip_zip(target_app_name: str, candidate_clip_zip: str) -> Union[VersionInfo, None]:
    """
    Tests if a string is a clip zip string.  If so, extract the version from a clip zip string.  If the string is not a valid clip zip string, return None.
    Example: a clip zip string of "abc_1.2.3.zip" for app "abc" returns VersionInfo of 1.2.3.
    :param target_app_name: target app name
    :param candidate_clip_zip: candidate clip app zip string to try to get the version from
    :return: version or None if not a successful parse for a clip zip string
    """
    version = None
    extension = f".{CLIP_EXT}"
    if candidate_clip_zip.startswith(target_app_name):
        version_string = candidate_clip_zip[len(target_app_name) :]
        if version is None and version_string.endswith(extension):
            version_string = version_string[: -len(extension)]  # remove extension
            if version_string.startswith("_"):
                try:
                    version = VersionInfo.parse(version_string[1:])  # pass over the "_"
                except IndexError as e:
                    log.debug(e)
                except TypeError as e:
                    log.debug(e)
                except ValueError as e:
                    log.debug(e)
    return version
