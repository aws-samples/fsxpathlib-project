# -*- coding: utf-8 -*-

import pytest
import random
from pathlib import PureWindowsPath

import smbclient
from fsxpathlib.tests import fsx_client


class TestFSxClient:
    def test_session_context_manager(self):
        with fsx_client.session(connection_timeout=1):
            path = PureWindowsPath(
                fsx_client.fs.dns_name,
                "share", "TestFSxClient.test_session_context_manager.txt",
            )
            with smbclient.open_file(str(path), mode="w") as f:
                f.write(str(random.randint(1, 100)))


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
