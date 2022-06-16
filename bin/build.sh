#!/bin/bash
# Build distribution and wheel files at ``dist/`` directory

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$(dirname "${dir_here}")"

# Clean up existing files
rm -r "${dir_project_root}/dist"
cd "${dir_project_root}"

# build distribution and wheel files
${dir_project_root}/venv/bin/python setup.py sdist bdist_wheel --universal
