from dataclasses import dataclass
from pathlib import Path

test_name = "testpyshipupdate"


@dataclass
class TestDirs:
    data_dir = Path("data")
    clips = Path(data_dir, "clips")
