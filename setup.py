"""Setup.py file for installing the python-related parts of the andrei_launch_utils package."""

import os

from setuptools import find_packages, setup

package_name = "andrei_launch_utils"
launch_files = [os.path.join("launch", f) for f in os.listdir("launch")] if os.path.isdir("launch") else []
action_files = [os.path.join("action", f) for f in os.listdir("action")] if os.path.isdir("action") else []
message_files = [os.path.join("msg", f) for f in os.listdir("msg")] if os.path.isdir("msg") else []

# Recursively collect all config files, preserving subdirectory structure
config_files = []
config_dir = "config"
for root, _dirs, files in os.walk(config_dir):
    for file in files:
        # Destination path preserves subdirectories, but is under share/<package_name>/config
        destination_dir = os.path.relpath(root, config_dir)
        install_dir = os.path.join("share", package_name, "config", destination_dir)
        source_file = os.path.join(root, file)
        config_files.append((install_dir, [source_file]))

data_files = [
    ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    ("share/" + package_name, ["package.xml"]),
]
if config_files:
    data_files += config_files
if launch_files:
    data_files.append(("share/" + package_name + "/launch", launch_files))
if action_files:
    data_files.append(("share/" + package_name + "/action", action_files))
if message_files:
    data_files.append(("share/" + package_name + "/msg", message_files))

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
