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
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: Unix",
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

"""
Appendix
--------
Frequent used classifiers List::

    [
        "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 6 - Mature",
        "Development Status :: 7 - Inactive",
    
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Religion",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
    
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ]
"""
