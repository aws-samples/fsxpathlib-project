.. _release_history:

Release and Version History
==============================================================================


0.0.2 (Planned)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.1 (working)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release with basic features and APIs
- Supported attributes:
    - :attr:`~fsxpathlib.path.FsxPath.abspath`
    - :attr:`~fsxpathlib.path.FsxPath.dirpath`
    - :attr:`~fsxpathlib.path.FsxPath.dirname`
    - :attr:`~fsxpathlib.path.FsxPath.basename`
    - :attr:`~fsxpathlib.path.FsxPath.fname`
    - :attr:`~fsxpathlib.path.FsxPath.ext`
    - :attr:`~fsxpathlib.path.FsxPath.size`
    - :attr:`~fsxpathlib.path.FsxPath.size_for_human`
    - :attr:`~fsxpathlib.path.FsxPath.atime`
    - :attr:`~fsxpathlib.path.FsxPath.mtime`
    - :attr:`~fsxpathlib.path.FsxPath.ctime`
    - :attr:`~fsxpathlib.path.FsxPath.chgtime`
    - :attr:`~fsxpathlib.path.FsxPath.atime_ns`
    - :attr:`~fsxpathlib.path.FsxPath.mtime_ns`
    - :attr:`~fsxpathlib.path.FsxPath.ctime_ns`
    - :attr:`~fsxpathlib.path.FsxPath.chgtime_ns`
    - :attr:`~fsxpathlib.path.FsxPath.st_dev`
    - :attr:`~fsxpathlib.path.FsxPath.md5`
    - :attr:`~fsxpathlib.path.FsxPath.sha256`
    - :attr:`~fsxpathlib.path.FsxPath.sha512`
- Supported methods:
    - :meth:`~fsxpathlib.path.FsxPath.is_absolute`
    - :meth:`~fsxpathlib.path.FsxPath.absolute`
    - :meth:`~fsxpathlib.path.FsxPath.relative_to`
    - :meth:`~fsxpathlib.path.FsxPath.change`
    - :meth:`~fsxpathlib.path.FsxPath.open`
    - :meth:`~fsxpathlib.path.FsxPath.write_bytes`
    - :meth:`~fsxpathlib.path.FsxPath.read_bytes`
    - :meth:`~fsxpathlib.path.FsxPath.write_text`
    - :meth:`~fsxpathlib.path.FsxPath.read_text`
    - :meth:`~fsxpathlib.path.FsxPath.assert_is_file_and_exists`
    - :meth:`~fsxpathlib.path.FsxPath.assert_is_dir_and_exists`
    - :meth:`~fsxpathlib.path.FsxPath.select`
    - :meth:`~fsxpathlib.path.FsxPath.select_file`
    - :meth:`~fsxpathlib.path.FsxPath.select_dir`
    - :meth:`~fsxpathlib.path.FsxPath.select_by_ext`
    - :meth:`~fsxpathlib.path.FsxPath.mkdir`
    - :meth:`~fsxpathlib.path.FsxPath.mkdir_if_not_exists`
    - :meth:`~fsxpathlib.path.FsxPath.exists`
    - :meth:`~fsxpathlib.path.FsxPath.is_file`
    - :meth:`~fsxpathlib.path.FsxPath.is_dir`
    - :meth:`~fsxpathlib.path.FsxPath.is_link`
    - :meth:`~fsxpathlib.path.FsxPath.remove`
    - :meth:`~fsxpathlib.path.FsxPath.rmdir`
    - :meth:`~fsxpathlib.path.FsxPath.rmtree`
    - :meth:`~fsxpathlib.path.FsxPath.remove_if_exists`
    - :meth:`~fsxpathlib.path.FsxPath.copy_from`
    - :meth:`~fsxpathlib.path.FsxPath.copy_to`

**Minor Improvements**

**Bugfixes**

**Miscellaneous**
