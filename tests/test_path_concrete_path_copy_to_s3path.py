# -*- coding: utf-8 -*-

import pytest

from s3pathlib import S3Path
from fsxpathlib.path import FsxPath
from fsxpathlib.tests import (
    FsxPathBaseTest,
    fpath_prefix,
    dir_datalake,
    path_log_txt,
    s3path_prefix,
)


class TestFsxPathCopyToS3Path(FsxPathBaseTest):
    def test_copy_to_s3path(self):
        # before state
        fpath_root = FsxPath(fpath_prefix, "copy_to_s3path")
        fpath_root.remove_if_exists()
        fpath_root.mkdir_if_not_exists()

        fpath_datalake = FsxPath(fpath_root, dir_datalake.basename)
        fpath_log_txt = FsxPath(fpath_root, path_log_txt.basename)

        fpath_datalake.copy_from(dir_datalake)
        fpath_log_txt.copy_from(path_log_txt)

        s3path_root = S3Path(s3path_prefix, "copy_to_s3path").to_dir()
        s3path_root.delete_if_exists()

        s3path_datalake = S3Path(s3path_root, dir_datalake.basename).to_dir()
        s3path_log_txt = S3Path(s3path_root, path_log_txt.basename)

        # copy file
        assert s3path_log_txt.exists() is False

        fpath_log_txt.copy_to(s3path_log_txt)

        self.assert_fsxpath_equal_to_s3path(fpath_log_txt, s3path_log_txt)

        # copy dir
        assert s3path_datalake.exists() is False

        fpath_datalake.copy_to(s3path_datalake)

        self.assert_fsxpath_equal_to_s3path(fpath_datalake, s3path_datalake)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
