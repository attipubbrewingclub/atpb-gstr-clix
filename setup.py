"""Write build-time metadata into the package when building wheels/sdists."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    def run(self) -> None:
        super().run()
        pkg_dir = Path(self.build_lib) / "atpb_gstr_clix"
        pkg_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        (pkg_dir / "_build_time.py").write_text(
            f"BUILD_TIMESTAMP = {ts!r}\n",
            encoding="utf-8",
        )


setup(cmdclass={"build_py": build_py})
