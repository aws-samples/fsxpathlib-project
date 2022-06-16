#!/bin/bash
# Publish this library to pypi

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$(dirname "${dir_here}")"

# Build distribution
rm -r "${dir_project_root}/dist"
cd "${dir_project_root}" || return
${dir_project_root}/venv/bin/python setup.py sdist bdist_wheel --universal

# Upload to PyPI.org
${dir_project_root}/venv/bin/twine upload "${dir_project_root}/dist/*"
