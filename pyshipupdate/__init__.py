
CLIP_EXT = "clip"  # zipped clip file extension

from .__version__ import __application_name__, __author__, __version__, __description__, __author_email__, __download_url__, __url__
from .os_util import is_windows, mkdirs, rmdir, copy_tree, get_target_os
from .version import version_from_clip_zip
from .updater import Updater
from .aws import UpdaterAwsS3
