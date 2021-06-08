CLIP_EXT = "clip"  # zipped clip file extension

from .__version__ import __application_name__, __author__, __version__, __description__, __author_email__, __download_url__, __url__
from .bucket import create_bucket_name
from .exe_return_codes import ok_return_code, restart_return_code, error_return_code, can_not_find_file_return_code
from .os_util import is_windows, mkdirs, rmdir, copy_tree, get_target_os
from .version import version_from_clip_zip
from .updater import Updater
from .aws import UpdaterAwsS3
