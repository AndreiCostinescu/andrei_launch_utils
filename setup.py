"""Setup.py file for installing the python-related parts of the andrei_launch_utils package."""

import os

from setuptools import find_packages, setup


def collect_files_in_directory(collection: list, dir_name: str):
    """Return a tuple with the install path and a list of files in a given directory or the empty list if the directory does not exist or is empty."""
    files = (
        [os.path.join(dir_name, f) for f in os.listdir(dir_name)] if os.path.isdir(dir_name) else []
    )
    if files:
        install_dir = os.path.join("share", package_name, dir_name)
        collection.append((install_dir, files))


def collect_files_with_structure_in_directory(collection: list, dir_name: str):
    """Return a list of tuple of files and their place in the installation directory."""
    collected_files = []
    for root, _, files in os.walk(dir_name):
        for file in files:
            # Destination path preserves subdirectories, but is under share/<package_name>/<dir_name>
            destination_dir = os.path.relpath(root, dir_name)
            install_dir = os.path.join("share", package_name, dir_name, destination_dir)
            source_file = os.path.join(root, file)
            collected_files.append((install_dir, [source_file]))
    if collected_files:
        collection += collected_files


package_name = "andrei_launch_utils"
data_files = [
    ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    ("share/" + package_name, ["package.xml"]),
]
collect_files_in_directory(data_files, "launch")
collect_files_in_directory(data_files, "action")
collect_files_in_directory(data_files, "msg")
# Recursively collect all config files, preserving subdirectory structure
collect_files_with_structure_in_directory(data_files, "config")

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Andrei Costinescu",
    maintainer_email="AndreiCostinescu96@gmail.com",
    description="Package with python utilities for launch files",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [],
    },
)
