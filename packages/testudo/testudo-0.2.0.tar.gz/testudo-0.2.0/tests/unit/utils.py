from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

@contextmanager
def tempdir() -> Generator[Path, None, None]:
    with TemporaryDirectory() as tmp:
        yield Path(tmp)