# -*- coding: utf-8 -*-

import os
import sys
import json

import smbclient
from pathlib_mate import Path
from s3pathlib import S3Path
from boto_session_manager import BotoSesManager

from fsxpathlib.client import FSxClient
from fsxpathlib.path import FsxPath
from fsxpathlib.logger import logger
from fsxpathlib.hashes import get_hash

logger.disable("fsxpathlib")

IS_LOCAL = False
IS_CI = False

if "CI" in os.environ:
    IS_CI = True
    RUNTIME = "ci"
else:
    IS_LOCAL = True
    RUNTIME = "local"

dir_here = Path.dir_here(__file__)
dir_project_root = Path(dir_here).parent.parent

if IS_LOCAL:
    path_credentials_json = Path(dir_project_root, "test_credentials.json")
    credentials_data = json.loads(path_credentials_json.read_text())
    fsx_file_system_id = credentials_data["fsx_file_system_id"]
    ad_username = credentials_data["ad_username"]
    ad_password = credentials_data["ad_password"]
    bsm = BotoSesManager(profile_name="fsxpathlib_dev")
    boto_ses = bsm.boto_ses
elif IS_CI:
    fsx_file_system_id = os.environ["FSXPATHLIB_FSX_FILE_SYSTEM_ID"]
    ad_username = os.environ["FSXPATHLIB_TEST_AD_USERNAME"]
    ad_password = os.environ["FSXPATHLIB_TEST_AD_PASSWORD"]
    bsm = BotoSesManager()
    boto_ses = bsm.boto_ses
else:
    raise NotImplementedError

# A fsx client for unit test
fsx_client = FSxClient(
    fsx_file_system_id=fsx_file_system_id,
    ad_username=ad_username,
    ad_password=ad_password,
)

# A fsx path for unit test
fpath_prefix = FsxPath(
    fsx_client.server,
    "share",
    "fsxpathlib",
    "unittest",
    RUNTIME,
    sys.platform,
    f"py{sys.version_info.major}.{sys.version_info.minor}",
)

# A s3 path for unit test
s3path_prefix = S3Path(
    "aws-data-lab-sanhe-for-opensource",
    "unittest",
    "fsxpathlib",
    RUNTIME,
    sys.platform,
    f"py{sys.version_info.major}.{sys.version_info.minor}",
).to_dir()

# A local path for unit test
_dir_here = Path.dir_here(__file__)
_dir_project_root = _dir_here.parent.parent
dir_tests = Path(_dir_project_root, "tests")

# dummy data dir
dir_datalake = Path(_dir_here, "datalake")

# dummy file path
path_log_txt = Path(_dir_here, "log.txt")


class FsxPathBaseTest:
    @classmethod
    def setup_class(cls):
        fsx_client.create_session(connection_timeout=3)

    @classmethod
    def teardown_class(cls):
        smbclient.delete_session(fsx_client.server)

    def assert_fsxpath_equal_to_path(
        self,
        fpath: FsxPath,
        path: Path,
    ):
        if fpath.is_file():
            assert fpath.basename == path.basename
            assert fpath.md5 == path.md5
        elif fpath.is_dir():
            fpath_dct = dict()
            for p in fpath.select():
                key = "/".join(p.relative_to(fpath).parts)
                if p.is_file():
                    fpath_dct[key] = p.md5
                elif p.is_dir():
                    fpath_dct[key] = ""
                else:  # pragma: no cover
                    raise NotImplementedError
            path_dct = dict()
            for p in path.select():
                key = "/".join(p.relative_to(path).parts)
                if p.is_file():
                    path_dct[key] = p.md5
                elif p.is_dir():
                    path_dct[key] = ""
                else:  # pragma: no cover
                    raise NotImplementedError
            assert fpath_dct == path_dct
        else:  # pragma: no cover
            raise NotImplementedError

    def assert_fsxpath_equal_to_s3path(
        self,
        fpath: FsxPath,
        s3path: S3Path,
    ):
        if fpath.is_file():
            assert fpath.basename == s3path.basename
            assert fpath.md5 == get_hash(s3path)
        elif fpath.is_dir():
            fpath_dct = dict()
            for p in fpath.select_file():
                key = "/".join(p.relative_to(fpath).parts)
                fpath_dct[key] = p.md5

            s3path_dct = dict()
            for p in s3path.iter_objects():
                key = "/".join(p.relative_to(s3path).parts)
                s3path_dct[key] = get_hash(p)

            assert fpath_dct == s3path_dct
        else:
            raise NotImplementedError

    def assert_fsxpath_equal_to_fsxpath(
        self,
        fpath1: FsxPath,
        fpath2: FsxPath,
    ):
        if fpath1.is_file():
            assert fpath1.basename == fpath1.basename
            assert fpath2.md5 == fpath2.md5
        elif fpath1.is_dir():
            fpath1_dct = dict()
            for p in fpath1.select_file():
                key = "/".join(p.relative_to(fpath1).parts)
                fpath1_dct[key] = p.md5

            fpath2_dct = dict()
            for p in fpath2.select_file():
                key = "/".join(p.relative_to(fpath2).parts)
                fpath2_dct[key] = p.md5
            assert fpath1_dct == fpath2_dct
        else:
            raise NotImplementedError
