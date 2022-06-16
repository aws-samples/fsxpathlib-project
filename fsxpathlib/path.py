# -*- coding: utf-8 -*-

from typing import (
    TYPE_CHECKING,
    List, Set, Union, Iterable,
)
import hashlib

import smbclient
import smbclient.shutil

from pathlib import PureWindowsPath

from pathlib_mate import Path
from s3pathlib import S3Path

from .helper import repr_data_size
from .hashes import get_hash
from .logger import logger, TAB1, TAB2, TAB3
from .vendors.iterproxy import IterProxy

if TYPE_CHECKING:  # pragma: no cover
    from pathlib_mate import Path
    from s3pathlib import S3Path


class FsxPathIterProxy(IterProxy):  # pragma: no cover
    """
    An iterator proxy utility class provide client side in-memory filter.
    It is highly inspired by sqlalchemy Result Proxy that depends on SQL server
    side filter.

    Allow client side in-memory filtering for iterator object that yield
    :class:`FsxPath`.
    """

    def __next__(self) -> 'FsxPath':
        return super(FsxPathIterProxy, self).__next__()

    def one(self) -> 'FsxPath':
        return super(FsxPathIterProxy, self).one()

    def one_or_none(self) -> Union['FsxPath', None]:
        return super(FsxPathIterProxy, self).one_or_none()

    def many(self, k: int) -> List['FsxPath']:
        return super(FsxPathIterProxy, self).many(k)

    def all(self) -> List['FsxPath']:
        return super(FsxPathIterProxy, self).all()

    def filter_by_ext(self, *exts: str) -> 'FsxPathIterProxy':
        n = len(exts)
        if n == 0:
            raise ValueError
        elif n == 1:
            ext = exts[0].lower()

            def f(p: FsxPath) -> bool:
                return p.ext.lower() == ext

            return self.filter(f)
        else:
            valid_exts = set([ext.lower() for ext in exts])

            def f(p: FsxPath) -> bool:
                return p.ext.lower() in valid_exts

            return self.filter(f)


SERVER = r"\\"


class FsxPath(PureWindowsPath):
    """

    FsxPath only support absolute path and relative path, it doesn't support
    partial path that depends on user's current working directory.
    """
    __slots__ = ("_stat_cache", "_is_relpath")

    def _init(self):
        super(FsxPath, self)._init()
        self._stat_cache = None
        self._is_relpath = False

    def is_absolute(self) -> bool:
        """
        """
        return not self._is_relpath

    def absolute(self) -> 'FsxPath':
        """
        """
        return self.__class__(self.__str__())

    __PURE_PATH_ATTR_START_HERE = None  # Just for visual divider and navigator

    @property
    def abspath(self) -> str:
        r"""
        Return absolute path as a string.
        
        Example: ``drive\admin\readme.txt`` for ``FsxPath(drive\admin\readme.txt)``
        """
        return self.__str__()

    @property
    def dirpath(self) -> str:
        r"""
        Example: ``drive\admin`` for ``FsxPath(drive\admin\readme.txt)``
        """
        return self.parent.abspath

    @property
    def dirname(self) -> str:
        r"""
        Parent dir name.

        Example: ``admin`` for ``FsxPath(drive\admin\readme.txt)``
        """
        return self.parent.name

    @property
    def basename(self) -> str:
        r"""
        File name with extension, path is not included.

        Example: ``readme.txt`` for ``FsxPath(drive\admin\readme.txt)``
        """
        return self.name

    @property
    def fname(self) -> str:
        r"""
        File name without extension.

        Example: ``readme`` for ``FsxPath(drive\admin\readme.txt)``
        """
        return self.stem

    @property
    def ext(self) -> str:
        r"""
        File extension. If it's a dir, then return empty str.
        :type self: Path
        :rtype: str
        Example: ``.txt`` for ``drive\admin\readme.txt``
        """
        return self.suffix

    __PURE_PATH_METH_START_HERE = None  # Just for visual divider and navigator

    def relative_to(self, *other) -> 'FsxPath':
        """
        """
        path = FsxPath(*super(FsxPath, self).relative_to(*other).parts)
        path._is_relpath = True
        return path

    def change(
        self,
        new_abspath=None,
        new_dirpath=None,
        new_dirname=None,
        new_basename=None,
        new_fname=None,
        new_ext=None,
    ) -> 'FsxPath':
        """
        Return a new :class:`FsxPath` object with updated data.

        Example::
        
            >>> FsxPath("drive/alice/test.py").change(new_fname="test1")
            drive/alice/test1.py

            >>> FsxPath("drive/alice/test.py").change(new_ext=".txt")
            drive/alice/test.txt

            >>> FsxPath("drive/alice/test.py").change(new_dirname="bob")
            drive/bob/test.py

            >>> FsxPath("drive/alice/test.py").change(new_dirpath="tmp")
            tmp/test.py
        """
        if new_abspath is not None:
            p = self.__class__(new_abspath)
            return p

        if (new_dirpath is None) and (new_dirname is not None):
            new_dirpath = f"{self.parent.dirpath}\\{new_dirname}"

        elif (new_dirpath is not None) and (new_dirname is None):
            new_dirpath = new_dirpath

        elif (new_dirpath is None) and (new_dirname is None):
            new_dirpath = self.dirpath

        elif (new_dirpath is not None) and (new_dirname is not None):
            raise ValueError("Cannot having both new_dirpath and new_dirname!")

        if new_basename is None:
            if new_fname is None:
                new_fname = self.fname
            if new_ext is None:
                new_ext = self.ext
            new_basename = new_fname + new_ext
        else:
            if new_fname is not None or new_ext is not None:
                raise ValueError(
                    "Cannot having both new_basename, new_fname, new_ext!"
                )

        return self.__class__(new_dirpath, new_basename)

    __CONCRETE_PATH_ATTR_START_HERE = None  # Just for visual divider and navigator

    def _stat(self) -> smbclient.SMBStatResult:
        if self._stat_cache is None:
            self._stat_cache = smbclient.stat(self.abspath)
        return self._stat_cache

    @property
    def size(self) -> int:
        """
        """
        return self._stat().st_size

    @property
    def size_for_human(self) -> str:
        """
        """
        return repr_data_size(self.size)

    @property
    def atime(self) -> float:
        """
        """
        return self._stat().st_atime

    @property
    def mtime(self) -> float:
        """
        """
        return self._stat().st_mtime

    @property
    def ctime(self) -> float:
        """
        """
        return self._stat().st_ctime

    @property
    def chgtime(self) -> float:
        """
        """
        return self._stat().st_chgtime

    @property
    def atime_ns(self) -> int:
        """
        """
        return self._stat().st_atime_ns

    @property
    def mtime_ns(self) -> int:
        """
        """
        return self._stat().st_mtime_ns

    @property
    def ctime_ns(self) -> int:
        """
        """
        return self._stat().st_ctime_ns

    @property
    def chgtime_ns(self) -> int:
        """
        """
        return self._stat().st_chgtime_ns

    @property
    def st_dev(self) -> int:
        """
        """
        return self._stat().st_dev

    @property
    def md5(self) -> str:
        """
        """
        return get_hash(file_obj=self, hash_meth=hashlib.md5)

    @property
    def sha256(self) -> str:  # pragma: no cover
        """
        """
        return get_hash(file_obj=self, hash_meth=hashlib.sha256)

    @property
    def sha512(self) -> str:  # pragma: no cover
        """
        """
        return get_hash(file_obj=self, hash_meth=hashlib.sha512)

    __CONCRETE_PATH_METH_START_HERE = None  # Just for visual divider and navigator

    def open(
        self,
        mode='r',
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        share_access=None,
        desired_access=None,
        file_attributes=None,
        file_type="file",
        **kwargs
    ):
        """
        File object liked protocol.
        """
        return smbclient.open_file(
            path=self.abspath,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            share_access=share_access,
            desired_access=desired_access,
            file_attributes=file_attributes,
            file_type=file_type,
            **kwargs
        )

    def write_bytes(self, data: bytes):
        """
        """
        with self.open(mode="wb") as f:
            return f.write(data)

    def read_bytes(self) -> bytes:
        """
        """
        with self.open(mode="rb") as f:
            return f.read()

    def write_text(
        self,
        data: str,
        encoding: str = "utf-8",
        errors=None,
    ):
        """
        """
        with self.open(
            mode="w", encoding=encoding, errors=errors
        ) as f:
            return f.write(data)

    def read_text(
        self,
        encoding: str = "utf-8",
        errors=None,
    ) -> str:
        """
        """
        with self.open(
            mode="r", encoding=encoding, errors=errors
        ) as f:
            return f.read()

    def assert_is_file_and_exists(self):
        """
        Assert it is a file and exists in FSX file system.
        """
        if not self.is_file():
            msg = "'%s' is not a file or doesn't exists!" % self
            raise EnvironmentError(msg)

    def assert_is_dir_and_exists(self):
        """
        Assert it is a directory and exists in FSX file system.
        """
        if not self.is_dir():
            msg = "'%s' is not a file or doesn't exists!" % self
            raise EnvironmentError(msg)

    def _select(
        self,
        include_dirs: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> Iterable['FsxPath']:
        self.assert_is_dir_and_exists()
        if recursive:
            for cwd, dirs, files in smbclient.walk(self.abspath):
                if include_dirs:
                    for name in dirs:
                        yield FsxPath(cwd, name)
                if include_files:
                    for name in files:
                        yield FsxPath(cwd, name)
        else:
            for name in smbclient.listdir(self):
                fpath = FsxPath(self, name)
                if include_dirs and include_files:
                    yield fpath
                else:
                    if fpath.is_file():
                        if include_files:
                            yield fpath
                    elif fpath.is_dir():
                        if include_dirs:
                            yield fpath
                    else:
                        raise NotImplementedError

    def select(
        self,
        include_dirs: bool = True,
        include_files: bool = True,
        recursive: bool = True,
    ) -> FsxPathIterProxy:
        """
        """
        return FsxPathIterProxy(
            iterable=self._select(
                include_dirs=include_dirs,
                include_files=include_files,
                recursive=recursive,
            )
        )

    def select_file(
        self,
        recursive: bool = True,
    ) -> FsxPathIterProxy:
        """
        """
        return self.select(include_dirs=False, recursive=recursive)

    def select_dir(
        self,
        recursive: bool = True,
    ) -> FsxPathIterProxy:
        """
        """
        return self.select(include_files=False, recursive=recursive)

    def select_by_ext(
        self,
        exts: List[str],
        recursive=True,
    ) -> FsxPathIterProxy:
        """
        """
        return self.select_file(
            recursive=recursive,
        ).filter_by_ext(*exts)

    __CONCRETE_PATH_BOOL_TEST_METH_START_HERE = None  # Just for visual divider and navigator

    def mkdir(
        self,
        parents=False,
        exist_ok=False,
        **kwargs
    ):
        """
        """
        if parents:
            return smbclient.makedirs(self.abspath, exist_ok=exist_ok, **kwargs)
        else:
            if exist_ok:
                if not smbclient.path.exists(self.abspath):
                    return smbclient.mkdir(self.abspath)
            else:
                return smbclient.mkdir(self.abspath)

    def mkdir_if_not_exists(self):
        """
        """
        return self.mkdir(parents=True, exist_ok=True)

    def exists(self) -> bool:
        """
        """
        return smbclient.path.exists(self.abspath)

    def is_file(self) -> bool:
        """
        """
        return smbclient.path.isfile(self.abspath)

    def is_dir(self) -> bool:
        """
        """
        return smbclient.path.isdir(self.abspath)

    def is_link(self) -> bool:
        """
        """
        return smbclient.path.islink(self.abspath)

    def remove(self):
        """
        """
        return smbclient.remove(self.abspath)

    def rmdir(self):
        """
        """
        return smbclient.rmdir(self.abspath)

    def rmtree(self):
        """
        """
        return smbclient.shutil.rmtree(self.abspath)

    def remove_if_exists(self):
        """
        """
        if self.exists():
            if self.is_file():
                return self.remove()
            elif self.is_dir():
                return self.rmtree()
            else:
                raise NotImplementedError

    __CONCRETE_PATH_WITH_LOCAL_FS = None  # Just for visual divider and navigator

    def _copy_from_fsxpath(
        self,
        fpath: 'FsxPath',
    ):
        logger.info(f"copy from {fpath.abspath} to {self.abspath}")
        if fpath.is_file():
            smbclient.copyfile(
                src=SERVER + fpath.abspath,
                dst=SERVER + self.abspath,
            )
        elif fpath.is_dir():
            dir_list: List[FsxPath] = list()
            file_list: List[FsxPath] = list()
            for cwd, dirs, files in smbclient.walk(fpath.abspath):
                for name in dirs:
                    p = FsxPath(cwd, name)
                    dir_list.append(p)
                for name in files:
                    p = FsxPath(cwd, name)
                    file_list.append(p)

            self.mkdir_if_not_exists()

            for p_dir_src in dir_list:
                p_dir_dst = self.__class__(self, *p_dir_src.relative_to(fpath).parts)
                p_dir_dst.mkdir_if_not_exists()

            for p_file_src in file_list:
                p_file_dst = self.__class__(self, *p_file_src.relative_to(fpath).parts)
                logger.info(f"{TAB1}copy from {p_file_src.abspath} to {p_file_dst.abspath}")
                smbclient.copyfile(
                    src=SERVER + p_file_src.abspath,
                    dst=SERVER + p_file_dst.abspath,
                )
        else:  # pragma: no cover
            raise NotImplementedError

        logger.info(f"{TAB1}done")

        return True

    def _copy_from_path(
        self,
        path: 'Path',
    ):
        logger.info(f"copy from {path.abspath} to {self.abspath}")
        if path.is_file():
            with self.open(mode="wb") as f_out:
                with path.open(mode="rb") as f_in:
                    f_out.write(f_in.read())
        elif path.is_dir():
            dir_list: List[Path] = list()
            file_list: List[Path] = list()
            for p in path.glob("**/*"):
                if p.is_dir():
                    dir_list.append(p)
                elif p.is_file():
                    file_list.append(p)
                else:
                    raise NotImplementedError

            self.mkdir_if_not_exists()
            for p_dir in dir_list:
                fpath = self.__class__(self, *p_dir.relative_to(path).parts)
                fpath.mkdir()

            for p_file in file_list:
                fpath = self.__class__(self, *p_file.relative_to(path).parts)
                logger.info(f"{TAB1}copy from {p_file.abspath} to {fpath.abspath}")
                with fpath.open(mode="wb") as f_out:
                    with p_file.open(mode="rb") as f_in:
                        f_out.write(f_in.read())

        else:  # pragma: no cover
            raise NotImplementedError

        logger.info(f"{TAB1}done")

        return True

    def _copy_from_s3path(
        self,
        s3path: 'S3Path',
    ):
        logger.info(f"copy from {s3path.uri} to {self.abspath}")
        if s3path.is_file():
            with self.open(mode="wb") as f_out:
                with s3path.open(mode="rb") as f_in:
                    f_out.write(f_in.read())
        elif s3path.is_dir():
            dir_set: Set[str] = set()
            file_list: List[S3Path] = list()
            for p in s3path.iter_objects(
                recursive=True,
                include_folder=True,
            ):
                dir_set.add(p.parent.uri)
                file_list.append(p)

            self.mkdir_if_not_exists()
            for p_dir in dir_set:
                p_dir = S3Path.from_s3_uri(p_dir).to_dir()
                fpath = self.__class__(self, *p_dir.relative_to(s3path).parts)
                fpath.mkdir_if_not_exists()

            for p_file in file_list:
                fpath = self.__class__(self, *p_file.relative_to(s3path).parts)
                logger.info(f"{TAB1}copy from {p_file.uri} to {fpath.abspath}")
                with fpath.open(mode="wb") as f_out:
                    with p_file.open(mode="rb") as f_in:
                        f_out.write(f_in.read())

        else:  # pragma: no cover
            raise NotImplementedError

        logger.info(f"{TAB1}done")

        return True

    def copy_from(
        self,
        file_obj: Union[str, 'FsxPath', Path, S3Path],
    ) -> bool:
        """
        Copy content for a not existing Fsx file / directory from
        source location. Source location can be:

        1. another :class`FsxPath`
        2. ``pathlib_mate.Path`` that represent an local file.
        3. ``s3pathlib.S3Path`` that represent an S3 object or folder.

        TODO: add conflict option, allow "ignore", "overwrite", "stop"

        .. versionadded:: 0.0.1
        """
        if isinstance(file_obj, str):  # pragma: no cover
            if file_obj.startswith("s3"):
                return self._copy_from_s3path(S3Path.from_s3_uri(file_obj))
            elif file_obj.startswith(r"\\"):
                return self._copy_from_fsxpath(FsxPath(file_obj))
            else:
                return self._copy_from_path(Path(file_obj))
        elif isinstance(file_obj, FsxPath):
            return self._copy_from_fsxpath(file_obj)
        elif isinstance(file_obj, Path):
            return self._copy_from_path(file_obj)
        elif isinstance(file_obj, S3Path):
            return self._copy_from_s3path(file_obj)
        else:  # pragma: no cover
            raise NotImplementedError

    def _copy_to_fsxpath(
        self,
        fpath: 'FsxPath',
    ):
        logger.info(f"copy from {self.abspath} to {fpath.abspath}")
        if self.is_file():
            smbclient.copyfile(
                src=SERVER + self.abspath,
                dst=SERVER + fpath.abspath,
            )
        elif self.is_dir():
            dir_list: List[FsxPath] = list()
            file_list: List[FsxPath] = list()
            for cwd, dirs, files in smbclient.walk(self.abspath):
                for name in dirs:
                    p = FsxPath(cwd, name)
                    dir_list.append(p)
                for name in files:
                    p = FsxPath(cwd, name)
                    file_list.append(p)

            fpath.mkdir_if_not_exists()

            for p_dir_src in dir_list:
                p_dir_dst = fpath.__class__(fpath, *p_dir_src.relative_to(self).parts)
                p_dir_dst.mkdir_if_not_exists()

            for p_file_src in file_list:
                p_file_dst = fpath.__class__(fpath, *p_file_src.relative_to(self).parts)
                logger.info(f"{TAB1}copy from {p_file_src.abspath} to {p_file_dst.abspath}")
                smbclient.copyfile(
                    src=SERVER + p_file_src.abspath,
                    dst=SERVER + p_file_dst.abspath,
                )
        else:  # pragma: no cover
            raise NotImplementedError

        logger.info(f"{TAB1}done")

        return True

    def _copy_to_path(
        self,
        path: Path,
    ):
        logger.info(f"copy from {self.abspath} to {path.abspath}")
        if self.is_file():
            with self.open(mode="rb") as f_src:
                with path.open(mode="wb") as f_dst:
                    f_dst.write(f_src.read())
        elif self.is_dir():
            dir_list: List[FsxPath] = list()
            file_list: List[FsxPath] = list()
            for cwd, dirs, files in smbclient.walk(self.abspath):
                for name in dirs:
                    p = FsxPath(cwd, name)
                    dir_list.append(p)
                for name in files:
                    p = FsxPath(cwd, name)
                    file_list.append(p)

            path.mkdir_if_not_exists()

            for p_dir_src in dir_list:
                p_dir_dst = Path(path, *p_dir_src.relative_to(self).parts)
                p_dir_dst.mkdir_if_not_exists()

            for p_file_src in file_list:
                p_file_dst = Path(path, *p_file_src.relative_to(self).parts)
                logger.info(f"{TAB1}copy from {p_file_src.abspath} to {p_file_dst.abspath}")
                with p_file_src.open(mode="rb") as f_src:
                    with p_file_dst.open(mode="wb") as f_dst:
                        f_dst.write(f_src.read())
        else:  # pragma: no cover
            raise NotImplementedError

        return True

    def _copy_to_s3path(
        self,
        s3path: S3Path,
    ) -> bool:
        logger.info(f"copy from {self.abspath} to {s3path.uri}")

        if self.is_file():
            with self.open(mode="rb") as f_src:
                with s3path.open(mode="wb") as f_dst:
                    f_dst.write(f_src.read())
        elif self.is_dir():
            for fpath_src in self.select_file():
                s3path_dst = S3Path(
                    s3path,
                    *fpath_src.relative_to(self).parts
                )
                logger.info(f"{TAB1}copy from {fpath_src.abspath} to {s3path_dst.uri}")
                with fpath_src.open(mode="rb") as f_src:
                    with s3path_dst.open(mode="wb") as f_dst:
                        f_dst.write(f_src.read())
        else:  # pragma: no cover
            raise NotImplementedError

        logger.info(f"{TAB1}done")

        return True

    def copy_to(
        self,
        file_obj: Union[str, 'FsxPath', Path, S3Path],
    ) -> bool:
        """
        Copy an existing Fsx file / directory to target location. Target
        location can be:

        1. another :class`FsxPath`
        2. ``pathlib_mate.Path`` that represent an local file.
        3. ``s3pathlib.S3Path`` that represent an S3 object or folder.

        .. versionadded:: 0.0.1

        TODO: add conflict option, allow "ignore", "overwrite", "stop"
        """
        if isinstance(file_obj, str):  # pragma: no cover
            if file_obj.startswith("s3"):
                return self._copy_to_s3path(S3Path.from_s3_uri(file_obj))
            elif file_obj.startswith(r"\\"):
                return self._copy_to_fsxpath(FsxPath(file_obj))
            else:
                return self._copy_to_path(Path(file_obj))
        elif isinstance(file_obj, FsxPath):
            return self._copy_to_fsxpath(file_obj)
        elif isinstance(file_obj, Path):
            return self._copy_to_path(file_obj)
        elif isinstance(file_obj, S3Path):
            return self._copy_to_s3path(file_obj)
        else:  # pragma: no cover
            raise NotImplementedError
