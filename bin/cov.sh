#!/bin/bash

# Run coverage test

dir_here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
dir_project_root="$(dirname "${dir_here}")"
bin_pytests="${dir_project_root}/venv/bin/pytest"
dir_tests="${dir_project_root}/tests"
dir_coverage_annotate="${dir_project_root}/.coverage.annotate"

rm -r "${dir_coverage_annotate}"

${bin_pytests} "${dir_tests}" -s --cov=fsxclient_utils --cov-report "term-missing" --cov-report "annotate:${dir_coverage_annotate}"
