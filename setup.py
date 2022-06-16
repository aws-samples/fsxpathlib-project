# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
import fsxpathlib as package


def read_requirements_file(path):
    """
    Read requirements.txt, ignore comments
    """
    requires = list()
    f = open(path, "r")
    for line in f.read().split("\n"):
        line = line.strip()
        if "#" in line:
            line = line[:line.find("#")].strip()
        if line:
            requires.append(line)
    return requires


dir_here = os.path.dirname(os.path.abspath(__file__))

package_name = package.__name__
long_description = open(os.path.join(dir_here, "README.rst"), "r").read()
download_url = "https://pypi.python.org/pypi/{}/{}#downloads".format(
    package.__name__, package.__version__
)
install_requires = read_requirements_file(os.path.join(dir_here, "requirements.txt"))
extras_require = {
    "tests": read_requirements_file(os.path.join(dir_here, "requirements-test.txt"))
}
packages = [package_name, ] + [
    "{}.{}".format(package_name, file)
    for file in find_packages(package_name)
]
include_package_data = True
package_data = {
    "": ["*.*"],
}

setup(
    name=package_name,
    version=package.__version__,
    description=package.__short_description__,
    long_description=long_description,
    author=package.__author__,
    author_email=package.__author_email__,
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=packages,
    include_package_data=include_package_data,
    package_data=package_data,
    download_url=download_url,
    python_requires=">=3.6, <4",
    install_requires=install_requires,
    extras_require=extras_require,
)
