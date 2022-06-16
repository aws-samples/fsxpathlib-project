# -*- coding: utf-8 -*-

import pytest
from fsxpathlib.path import FsxPath

server = "drive"


class TestFsxPathAsPurePath:
    def test_attribute_accessor(self):
        p = FsxPath(server, "database", "table", "file.json")
        assert p.is_absolute() == True
        assert str(p) == str(p.absolute())
        assert str(p) == p.abspath

        assert p.abspath == r"drive\database\table\file.json"
        assert p.dirpath == r"drive\database\table"
        assert p.dirname == r"table"
        assert p.basename == "file.json"
        assert p.fname == r"file"
        assert p.ext == r".json"

    def test_relative_path(self):
        p1 = FsxPath(server, "database", "table", "file.json")
        p2 = FsxPath(server, "database")
        rp = p1.relative_to(p2)
        assert str(rp) == r"table\file.json"
        with pytest.raises(ValueError):
            p2.relative_to(p1)

    def test_change(self):
        p = FsxPath(server, "database", "table", "file.json")

        p1 = p.change(new_ext=".txt")
        assert p1.ext == ".txt"
        assert p1.fname == p.fname
        assert p1.dirname == p.dirname
        assert p1.dirpath == p.dirpath

        p1 = p.change(new_fname="hello")
        assert p1.ext == p.ext
        assert p1.fname == "hello"
        assert p1.dirname == p.dirname
        assert p1.dirpath == p.dirpath

        p1 = p.change(new_fname="hello", new_ext=".txt")
        assert p1.ext == ".txt"
        assert p1.fname == "hello"
        assert p1.dirname == p.dirname
        assert p1.dirpath == p.dirpath

        p1 = p.change(new_basename="hello.txt")
        assert p1.ext == ".txt"
        assert p1.fname == "hello"
        assert p1.dirname == p.dirname
        assert p1.dirpath == p.dirpath

        p1 = p.change(new_dirname="folder")
        assert p1.ext == p.ext
        assert p1.fname == p.fname
        assert p1.dirname == "folder"
        assert p1.dirpath.endswith("folder")

        p1 = p.change(new_dirpath="drive\\tmp")
        assert p1.ext == p.ext
        assert p1.fname == p.fname
        assert p1.dirname == "tmp"
        assert p1.dirpath.endswith("tmp")
        assert p1.abspath == "drive\\tmp\\file.json"

        p1 = p.change(new_abspath="disk\\tmp\\hello.txt")
        assert p1.ext == ".txt"
        assert p1.fname == "hello"
        assert p1.basename == "hello.txt"
        assert p1.dirname == "tmp"
        assert p1.dirpath == "disk\\tmp"
        assert p1.abspath == "disk\\tmp\\hello.txt"

        with pytest.raises(ValueError):
            p.change(new_dirpath="new_dirpath", new_dirname="folder")

        with pytest.raises(ValueError):
            p.change(new_basename="hello.txt", new_fname="hello")

        with pytest.raises(ValueError):
            p.change(new_basename="hello.txt", new_ext="hello")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
