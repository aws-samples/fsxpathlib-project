# -*- coding: utf-8 -*-

"""
Objective Oriented Interface for AWS FSx, similar to pathlib.
"""


from ._version import __version__

__short_description__ = "Objective Oriented Interface for AWS FSx, similar to boto3 APIs for s3."
__license__ = "MIT"
__author__ = "Ivan Chen"
__author_email__ = "chen115yaohua@gmail.com"
__github_username__ = "chen115y"

try:
    from .client import FSxClient
    from .path import FsxPath
except ImportError: # pragma: no cover
    pass
except: # pragma: no cover
    raise
