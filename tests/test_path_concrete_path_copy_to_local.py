# -*- coding: utf-8 -*-

import pytest

from pathlib_mate import Path
from fsxpathlib.path import FsxPath
from fsxpathlib.tests import (
    FsxPathBaseTest,
    fpath_prefix,
    dir_datalake,
    path_log_txt,
    s3path_prefix,
)

dir_here = Path.dir_here(__file__)


class TestFsxPathCopyToLocal(FsxPathBaseTest):
    def test_copy_to_local(self):
        # before state
        fpath_root = FsxPath(fpath_prefix, "copy_to_local")
        fpath_root.remove_if_exists()
        fpath_root.mkdir_if_not_exists()

        fpath_datalake = FsxPath(fpath_root, dir_datalake.basename)
        fpath_log_txt = FsxPath(fpath_root, path_log_txt.basename)

        fpath_datalake.copy_from(dir_datalake)
        fpath_log_txt.copy_from(path_log_txt)

        dir_datalake_dst = Path(dir_here, dir_datalake.basename)
        path_log_txt_dst = Path(dir_here, path_log_txt.basename)

        dir_datalake_dst.remove_if_exists()
        path_log_txt_dst.remove_if_exists()

        # copy file
        assert path_log_txt_dst.exists() is False

        fpath_log_txt.copy_to(path_log_txt_dst)

        self.assert_fsxpath_equal_to_path(fpath_log_txt, path_log_txt_dst)

        # copy dir
        assert dir_datalake_dst.exists() is False

        fpath_datalake.copy_to(dir_datalake_dst)

        self.assert_fsxpath_equal_to_path(fpath_datalake, dir_datalake_dst)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
