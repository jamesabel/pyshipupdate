from dataclasses import dataclass
from pathlib import Path

import test_pyshipupdate

test_name = "testpyshipupdate"


@dataclass
class TestDirs:
    data_dir = Path(test_pyshipupdate.name, "data")
    app_dir = Path(data_dir, "app")
