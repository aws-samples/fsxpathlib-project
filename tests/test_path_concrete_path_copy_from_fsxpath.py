# -*- coding: utf-8 -*-

import pytest

from fsxpathlib.path import FsxPath
from fsxpathlib.tests import (
    FsxPathBaseTest,
    fpath_prefix,
    dir_datalake,
    path_log_txt,
)


class TestFsxPathCopyFromFsxPath(FsxPathBaseTest):
    def test_copy_from_path(self):
        # before state
        fpath_dir_source = FsxPath(fpath_prefix, "copy_from_fsxpath", "source")
        fpath_dir_target = FsxPath(fpath_prefix, "copy_from_fsxpath", "target")

        fpath_dir_source.remove_if_exists()
        fpath_dir_target.remove_if_exists()

        fpath_dir_source.mkdir_if_not_exists()
        fpath_dir_target.mkdir_if_not_exists()

        fpath_dir_source_datalake = FsxPath(fpath_dir_source, "datalake")
        fpath_dir_target_datalake = FsxPath(fpath_dir_target, "datalake")

        fpath_dir_source_datalake.copy_from(dir_datalake)

        fpath_file_source_log_txt = FsxPath(fpath_dir_source, path_log_txt.basename)
        fpath_file_target_log_txt = FsxPath(fpath_dir_target, path_log_txt.basename)

        fpath_file_source_log_txt.copy_from(path_log_txt)

        # copy file
        assert fpath_file_target_log_txt.exists() is False

        fpath_file_target_log_txt.copy_from(fpath_file_source_log_txt)

        self.assert_fsxpath_equal_to_fsxpath(fpath_file_source_log_txt, fpath_file_target_log_txt)

        # copy dir
        assert fpath_dir_target_datalake.exists() is False

        fpath_dir_target_datalake.copy_from(fpath_dir_source_datalake)

        self.assert_fsxpath_equal_to_fsxpath(fpath_dir_source_datalake, fpath_dir_target_datalake)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
