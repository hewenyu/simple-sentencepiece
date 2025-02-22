#!/usr/bin/env python3
#
# Copyright (c)  2024  Xiaomi Corporation (author: Wei Kang)

import glob
import os
import platform
import re
import shutil
import sys

import setuptools
from setuptools.command.build_ext import build_ext

cur_dir = os.path.dirname(os.path.abspath(__file__))


def is_windows():
    return platform.system() == "Windows"


def cmake_extension(name, *args, **kwargs) -> setuptools.Extension:
    kwargs["language"] = "c++"
    sources = []
    return setuptools.Extension(name, sources, *args, **kwargs)


class BuildExtension(build_ext):
    def build_extension(self, ext: setuptools.extension.Extension):
        # build/temp.linux-x86_64-3.8
        build_dir = self.build_temp
        os.makedirs(build_dir, exist_ok=True)

        # build/lib.linux-x86_64-3.8
        os.makedirs(self.build_lib, exist_ok=True)

        # ss is short for simple sentencepiece
        ss_dir = os.path.dirname(os.path.abspath(__file__))

        cmake_args = os.environ.get("SS_CMAKE_ARGS", "")
        make_args = os.environ.get("SS_MAKE_ARGS", "")
        system_make_args = os.environ.get("MAKEFLAGS", "")

        if cmake_args == "":
            cmake_args = "-DCMAKE_BUILD_TYPE=Release -DSBPE_ENABLE_TESTS=OFF"
            cmake_args += f" -DCMAKE_INSTALL_PREFIX={self.build_lib} "

        if make_args == "" and system_make_args == "":
            make_args = " -j "

        if "PYTHON_EXECUTABLE" not in cmake_args:
            print(f"Setting PYTHON_EXECUTABLE to {sys.executable}")
            cmake_args += f" -DPYTHON_EXECUTABLE={sys.executable}"


        if is_windows():
            build_cmd = f"""
         cmake {cmake_args} -B {self.build_temp} -S {ss_dir}
         cmake --build {self.build_temp} --target install --config Release
            """
            print(f"build command is:\n{build_cmd}")
            ret = os.system(
                f"cmake {cmake_args} -B {self.build_temp} -S {ss_dir}"
            )
            if ret != 0:
                raise Exception("Failed to configure simple sentencepiece")

            ret = os.system(
                f"cmake --build {self.build_temp} --target install --config Release"
            )
            if ret != 0:
                raise Exception("Failed to build and install simple sentencepiece")
        else:
            build_cmd = f"""
                cd {self.build_temp}

                cmake {cmake_args} {ss_dir}

                make {make_args} install/strip
            """
            print(f"build command is:\n{build_cmd}")

            ret = os.system(build_cmd)
            if ret != 0:
                raise Exception(
                    "\nBuild ssentencepiece failed. Please check the error "
                    "message.\n"
                    "You can ask for help by creating an issue on GitHub.\n"
                    "\nClick:\n"
                    "\thttps://github.com/pkufool/simple-sentencepiece/issues/new\n"  # noqa
                )

        lib_so = glob.glob(f"{build_dir}/lib/*.so*")
        for so in lib_so:
            print(f"Copying {so} to {self.build_lib}/")
            shutil.copy(f"{so}", f"{self.build_lib}/")

        # macos
        lib_so = glob.glob(f"{build_dir}/lib/*.dylib*")
        for so in lib_so:
            print(f"Copying {so} to {self.build_lib}/")
            shutil.copy(f"{so}", f"{self.build_lib}/")


def get_package_version():
    with open("CMakeLists.txt", encoding='utf-8') as f:
        content = f.read()

    latest_version = re.search(r"set\(SBPE_VERSION (.*)\)", content).group(1)
    latest_version = latest_version.strip('"')
    return latest_version


setuptools.setup(
    package_dir={
        "ssentencepiece": "ssentencepiece/python/ssentencepiece",
    },
    packages=["ssentencepiece"],
    ext_modules=[cmake_extension("_ssentencepiece")],
    cmdclass={"build_ext": BuildExtension},
)

with open("ssentencepiece/python/ssentencepiece/__init__.py", "a", encoding='utf-8') as f:
    f.write(f"__version__ = '{get_package_version()}'\n")

with open("ssentencepiece/python/ssentencepiece/__init__.py", "r", encoding='utf-8') as f:
    lines = f.readlines()

with open("ssentencepiece/python/ssentencepiece/__init__.py", "w", encoding='utf-8') as f:
    for line in lines:
        if "__version__" in line:
            f.write(line)
            break
        f.write(line)

