# -*- coding: utf-8 -*-

import pytest

from fsxpathlib.path import FsxPath
from fsxpathlib.tests import (
    FsxPathBaseTest,
    fpath_prefix,
    dir_datalake,
    path_log_txt,
)


class TestFsxPathCopyFromLocal(FsxPathBaseTest):
    def test_copy_from_path(self):
        # before state
        fpath_root = FsxPath(fpath_prefix, "copy_from_path")
        fpath_root.remove_if_exists()
        fpath_root.mkdir_if_not_exists()

        # copy file
        fpath = FsxPath(fpath_root, path_log_txt.basename)
        assert fpath.exists() is False

        fpath.copy_from(path_log_txt)

        self.assert_fsxpath_equal_to_path(fpath=fpath, path=path_log_txt)

        # copy dir
        fpath = FsxPath(fpath_root, "datalake")
        assert fpath.exists() is False

        fpath.copy_from(dir_datalake)

        # self.assert_fsxpath_equal_to_path(fpath=fpath, path=dir_datalake)

    # def test_copy_to_path(self):
    #     # before state
    #     fpath_root = FsxPath(fpath_prefix, "copy_to_path")
    #     fpath_root.remove_if_exists()
    #     fpath_root.mkdir_if_not_exists()
    #
    #     # copy file
    #     p = Path(__file__)
    #     fpath = FsxPath(fpath_root, p.basename)
    #     assert fpath.exists() is False
    #     fpath.copy_from(p)
    #     assert fpath.exists() is True
    #
    #     # copy dir
    #     p = dir_datalake
    #     fpath = FsxPath(fpath_root, "datalake")
    #     assert fpath.exists() is False
    #     fpath.copy_from(p)
    #
    #     assert FsxPath(fpath).exists()
    #     assert FsxPath(fpath).is_dir()
    #
    #     assert FsxPath(fpath, "README.rst").exists()
    #     assert FsxPath(fpath, "README.rst").is_file()
    #
    #     assert FsxPath(fpath, "db_amazon").exists()
    #     assert FsxPath(fpath, "db_amazon").is_dir()
    #
    #     assert FsxPath(fpath, "db_amazon", "images", "product_apple.img").exists()
    #     assert FsxPath(fpath, "db_amazon", "images", "product_apple.img").is_file()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
