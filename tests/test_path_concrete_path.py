# -*- coding: utf-8 -*-

import pytest
import smbclient
from datetime import datetime, timezone
from fsxpathlib.path import FsxPath
from fsxpathlib.tests import fsx_client, FsxPathBaseTest, fpath_prefix


class TestFsxPathAsConcretePath(FsxPathBaseTest):
    def test_attribute_accessor(self):
        p = FsxPath(fsx_client.server, "share", "file.txt")
        mtime = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
        s = "Hello World!"
        p.write_text(s)
        assert p.read_text() == s

        assert p.size == 12
        assert p.size_for_human == "12 B"
        assert len(p.md5) == 32

        assert abs(p.mtime - mtime) <= 10  # latency <= 10 sec

        _ = p.atime
        _ = p.mtime
        _ = p.ctime
        _ = p.chgtime
        _ = p.atime_ns
        _ = p.mtime_ns
        _ = p.ctime_ns
        _ = p.chgtime_ns

        p = FsxPath(fsx_client.server, "share", "file.dat")
        b = "BigBinary".encode("utf-8")
        p.write_bytes(b)
        assert p.read_bytes() == b

    def test_bool_test_methods(self):
        dir_prefix = FsxPath(fsx_client.server, "share", "bool_test_methods")
        path_readme = FsxPath(dir_prefix, "readme.txt")
        dir_folder = FsxPath(dir_prefix, "folder")
        path_file = FsxPath(dir_prefix, "folder", "file.txt")

        # prepare, clean up all files
        dir_prefix.remove_if_exists()

        assert dir_prefix.exists() is False
        assert dir_folder.exists() is False
        assert path_readme.exists() is False
        assert path_file.exists() is False

        # create files
        dir_prefix.mkdir(parents=True, exist_ok=True)
        dir_folder.mkdir(exist_ok=True)
        path_readme.write_text("readme")
        path_file.write_text("file")

        dir_folder.assert_is_dir_and_exists()
        with pytest.raises(Exception):
            dir_folder.assert_is_file_and_exists()

        path_file.assert_is_file_and_exists()
        with pytest.raises(Exception):
            path_file.assert_is_dir_and_exists()

        # test with bool test methods
        assert dir_prefix.exists() is True
        assert dir_folder.exists() is True
        assert path_readme.exists() is True
        assert path_file.exists() is True

        assert dir_prefix.is_file() is False
        assert dir_folder.is_file() is False
        assert path_readme.is_file() is True
        assert path_file.is_file() is True

        assert dir_prefix.is_dir() is True
        assert dir_folder.is_dir() is True
        assert path_readme.is_dir() is False
        assert path_file.is_dir() is False

        assert dir_prefix.is_link() is False
        assert dir_folder.is_link() is False
        assert path_readme.is_link() is False
        assert path_file.is_link() is False

        assert dir_prefix.is_link() is False
        assert dir_folder.is_link() is False
        assert path_readme.is_link() is False
        assert path_file.is_link() is False

        # clean up files slowly
        with pytest.raises(Exception):  # cannot remove non-empty file
            dir_folder.rmdir()

        with pytest.raises(Exception):  # cannot use remove() with dir
            dir_folder.remove()

        with pytest.raises(Exception):  # cannot use rmdir() with file
            path_readme.rmdir()

        with pytest.raises(Exception):  # cannot use rmtree() with file
            path_readme.rmtree()

        path_readme.remove()
        path_file.remove()
        dir_folder.rmdir()
        dir_prefix.rmdir()

        assert dir_prefix.exists() is False
        assert dir_folder.exists() is False
        assert path_readme.exists() is False
        assert path_file.exists() is False

        with pytest.raises(Exception):
            dir_folder.assert_is_file_and_exists()
        with pytest.raises(Exception):
            dir_folder.assert_is_dir_and_exists()
        with pytest.raises(Exception):
            path_file.assert_is_file_and_exists()
        with pytest.raises(Exception):
            path_file.assert_is_dir_and_exists()

    def test_select(self):
        fpath_root = FsxPath(fpath_prefix, "select")

        fpath_root.mkdir_if_not_exists()
        FsxPath(fpath_root, "log.txt").write_text("log file")
        FsxPath(fpath_root, "small-file.txt").write_text("small file")
        FsxPath(fpath_root, "large-file.txt").write_text("large file\n" * 1000)
        FsxPath(fpath_root, "readme.md").write_text("readme file")
        FsxPath(fpath_root, "image.jpg").write_text("dummy image")

        FsxPath(fpath_root, "folder").mkdir_if_not_exists()
        FsxPath(fpath_root, "folder", "log.txt").write_text("log file")
        FsxPath(fpath_root, "folder", "small-file.txt").write_text("small file")
        FsxPath(fpath_root, "folder", "large-file.txt").write_text("large file\n" * 1000)
        FsxPath(fpath_root, "folder", "readme.md").write_text("readme file")
        FsxPath(fpath_root, "folder", "image.jpg").write_text("dummy image")

        FsxPath(fpath_root, "folder", "subfolder").mkdir_if_not_exists()
        FsxPath(fpath_root, "folder", "subfolder", "log.txt").write_text("log file")
        FsxPath(fpath_root, "folder", "subfolder", "small-file.txt").write_text("small file")
        FsxPath(fpath_root, "folder", "subfolder", "large-file.txt").write_text("large file\n" * 1000)
        FsxPath(fpath_root, "folder", "subfolder", "readme.md").write_text("readme file")
        FsxPath(fpath_root, "folder", "subfolder", "image.jpg").write_text("dummy image")

        assert len(fpath_root.select().all()) == 17
        assert len(fpath_root.select_file().all()) == 15
        assert len(fpath_root.select_dir().all()) == 2
        assert len(fpath_root.select_by_ext([".txt"]).all()) == 9
        assert len(fpath_root.select_by_ext([".jpg"]).all()) == 3
        assert len(fpath_root.select(recursive=False).all()) == 6


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
