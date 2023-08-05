from pathlib import Path
from sys import version_info
from tempfile import TemporaryDirectory as _TemporaryDirectory
from typing import Optional


if version_info >= (3, 10):  # pragma: lt310

    class TemporaryDirectory(_TemporaryDirectory):  # type: ignore
        """Sub-class of TemporaryDirectory whose"""

        name: Path

        def __init__(
            self,
            *,
            suffix: Optional[str] = None,
            prefix: Optional[str] = None,
            dir: Optional[str] = None,
            ignore_cleanup_errors: bool = False,
        ) -> None:
            super().__init__(  # type: ignore
                suffix=suffix,
                prefix=prefix,
                dir=dir,
                ignore_cleanup_errors=ignore_cleanup_errors,
            )
            self.name = Path(self.name)

else:  # pragma: ge310

    class TemporaryDirectory(_TemporaryDirectory):
        """Sub-class of TemporaryDirectory whose"""

        name: Path

        def __init__(
            self,
            *,
            suffix: Optional[str] = None,
            prefix: Optional[str] = None,
            dir: Optional[str] = None,
        ) -> None:
            super().__init__(suffix=suffix, prefix=prefix, dir=dir)
            self.name = Path(self.name)
