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


class TestFsxPathCopyFromS3Path(FsxPathBaseTest):
    def test_copy_from_path(self):
        # before state
        fpath_root = FsxPath(fpath_prefix, "copy_from_s3path")
        fpath_root.remove_if_exists()
        fpath_root.mkdir_if_not_exists()

        s3path_prefix.delete_if_exists()
        s3path_datalake = S3Path(s3path_prefix, "copy_from_s3_path", "datalake").to_dir()
        s3path_datalake.upload_dir(dir_datalake.abspath)

        s3path_log_txt = S3Path(s3path_prefix, "copy_from_s3_path", "log.txt")
        s3path_log_txt.upload_file(path_log_txt.abspath)

        # copy file
        fpath = FsxPath(fpath_root, s3path_log_txt.basename)
        assert fpath.exists() is False

        fpath.copy_from(s3path_log_txt)

        self.assert_fsxpath_equal_to_s3path(fpath, s3path_log_txt)

        # copy dir
        fpath = FsxPath(fpath_root, "datalake")
        assert fpath.exists() is False

        fpath.copy_from(s3path_datalake)

        self.assert_fsxpath_equal_to_s3path(fpath, s3path_datalake)

        
if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
