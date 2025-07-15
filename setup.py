import glob
import os
import sys

from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

class CustomBuildExt(_build_ext):
    def run(self):
        import compile_numba
        compile_numba.build_numba_extensions()

        for so_file in glob.glob("*.so") + glob.glob("*.pyd"):
            target = os.path.join("pyquartic", os.path.basename(so_file))
            os.rename(so_file, target)

        super().run()

setup(
    name="pyquartic",
    packages=["pyquartic"],
    cmdclass={"build_ext": CustomBuildExt},
)
