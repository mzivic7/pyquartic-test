import glob
import os
import sys

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

class CustomBuildPy(_build_py):
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
    cmdclass={
        "build_py": CustomBuildPy,
        "bdist_wheel": bdist_wheel,
        },
)
