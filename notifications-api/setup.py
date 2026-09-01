# Copyright © 2019 Province of British Columbia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Compatibility setup.py for legacy source-build flows."""

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup


def read_requirements(filename):
    """Return project requirements from a requirements file."""
    with open(filename, encoding="utf-8") as req:
        requirements = req.readlines()
    return [
        requirement.strip().rstrip("\\").strip()
        for requirement in requirements
        if requirement.strip()
        and not requirement.startswith("#")
        and not requirement.startswith(" ")
    ]


setup(
    name="notifications_api",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("*.py")],
    include_package_data=True,
    zip_safe=False,
    install_requires=read_requirements("requirements.txt"),
)
