FSx Path Library
==============================================================================

**What is it?** ``fsxpathlib`` is the Python package that provides the Pythonic Objective Orirented programming (OOP) interface to allow developers to handle files and folders on Amazon `FSx (for Windows File Server)`_ storage services WITHOUT mounting Amazon FSx to local or on-line Windows machines. Amazon FSx for Windows File Server provides fully managed Microsoft Windows file servers, backed by a fully native Windows file system. With file storage on Amazon FSx and this Python package, the existing code, applications, and tools that Windows developers and administrators use today can be more easily migrated onto AWS. Also, the developers are more flexible to expand their code and applications for their business use cases with this Python package by removing the constraint of mounting Amazon FSx service.

**Why do you need it?** There is NO (OOP) Python library to allow developers to work on file level operations on Amazon FSx without mounting. The `boto3 FSx client APIs`_ only provides APIs to handle storage-volume-level operations (e.g., storage volume creation, volume deletion, etc.) but not file-level ones. This Python package is able to provide the APIs to do file or folder copy, read, delete, open, change, save, etc. on Amazon FSx service regardless those APIs are running in Linux, Mac or Windows environments. Moreover, it can handle file transfer between Amazon FSx and Amazon S3 storage services as well.

**How does it work?** This library requires `smbprotocol`_ library to be available as low-level APIs. The following shows highlighted attributes and methods avilable on this Python package:

**Highlighted Attributes**:

- **abspath**: return absolute path as a string for a given FSx path
- **dirpath**: return the directory info from a given FSx path
- **dirname**: return parent directory name for a given FSx path
- **basename**: return file name with extension (not included directories) for a given FSx path. If it is a directory, then return empty string.
- **fname**: return the file name without extension for a given FSx path
- **ext**: return the file extension for a given FSx path. If it is a directory, then return empty string.
- **size_for_human**: return human readble size info for a given FSx path

**Highlighted Methonds**:

- **copy_to()**: copy an existing FSx file or directory to a target location, which can be a FSx path, a local file or a S3 object or directory
- **copy_from()**: copy and save to a non-existing FSx file or directory from a source location, which can be a FSx path, a local file or a S3 objct or folder
- **change()**: change an existing FSx file or directory on path, name and extension
- **exist()**: return true if a FSx file or directory exists
- **is_file()**: return true if the given path is a file
- **is_dir()**: return true if the give path is a folder
- **mkdir_if_not_exists()**: create a new directory on FSx if it doesn't exist
- **read_bytes()**: read content as bytes from an existing FSx file
- **read_text()**: read content as (utf-8) text from an existing FSx file
- **remove_if_exists()**: delete a file or an entire directory on FSx if it exists
- **select_file()**: return the list of of files for a given FSx path
- **select_dir()**: return the list of directories for a given FSx path
- **select_by_ext()**: return the list of files filtered by the extension for a given FSx path
- **write_bytes()**: save content as bytes into a FSx file
- **write_text()**: save content as (utf-8) text into a FSx file

**Note: This library currently only supports operations within the same AWS region and doesn't support any cross-region operations yet.**

.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Features
------------------------------------------------------------------------------

APIs for manipulating files and folders on a FSx (for Windows File Server) storage volume.

Install
------------------------------------------------------------------------------

To install this library from a downloaded `wheel file`_, you can do it as an example below:

.. code-block:: console

    $ pip install fsxpathlib-0.0.1-py2.py3-none-any.whl

Quick Start
------------------------------------------------------------------------------

**Prerequisites**

- Please follow the `tutorial link`_ to setup a sample FSx (for Windows File Server) storage volume if you don't have any. Locate and remember the File System ID on the console like the screen shot below. Also, please remember user name, password and domain that you have established during FSx service setup.

.. image:: /images/fsx_systemid.png
    :width: 320

- Prepare an `AWS account`_ and an IAM user with **AdministratorAccess** permission. For sign up to AWS, please refer to this link_. For how to create an admin IAM user, please refer to this `AWS on-line document`_.

- Install and setup AWS Command Line Interface (CLI) at your local environment. For how to install and setup AWS CLI, please refer to this `on-line document`_.

- Install and setup `Python 3 virtual environment`_.

**Run Sample Code**

First, try out the following examples for path manipulating functions:

.. code-block:: python

    # import
    >>> from fsxpathlib.path import FsxPath

    # Establish a FSx path. For example:
    >>> p = FsxPath("server", "database", "table", "file.json")
    # Then display the path info:
    >>> print(f"Absolute path is: {p.abspath}")
    Absolute path is: server\database\table\file.json
    >>> print(p.dirpath)
    server\database\table
    >>> print(p.dirname)
    table
    >>> print(p.basename)
    file.json
    >>> print(p.fname)
    file
    >>> print(p.ext)
    .json

    # Let us now try some changes on the path:
    >>> p1 = p.change(new_ext=".txt")
    >>> print(p1.ext)
    .txt
    >>> print(p1.abspath)
    server\database\table\file.txt
    >>> p1 = p.change(new_fname="hello")
    >>> print(p1.abspath)
    server\database\table\hello.json

Second, establish a connection to the FSx storage service that you just setup by following the `tutorial link`_. The codes below show examples to transfer data among FSx, S3 and local storage. When you try yours, please remember to replace the fsx_file_system_id, username, and password variables with your own values. Also, make sure you have `pathlib_mate`, `s3pathlib` and `fsxpathlib` libraries installed.

.. code-block:: python

    # import python libraries
    >>> import getpass
    >>> from s3pathlib import S3Path
    >>> from fsxpathlib import FSxClient
    >>> from fsxpathlib import FsxPath
    >>> from pathlib_mate import Path
    >>> import os

    # Establish a connection session to the FSx service. 
    # Replace fsx_filesystemid, username and password variables with your own values.
    >>> password = getpass.getpass(prompt='What is the password for accessing FSx?')
    >>> fsx = FSxClient(fsx_file_system_id='fs-054a31b0ff86de2b0',
            ad_username='admin',
            ad_password=password)
    What is the password for accessing FSx?········
    >>> if fsx:
        print("Connect to the FSx server successfully")
    Connect to the FSx server successfully
    >>> fsx_sess = fsx.create_session()

Then, try out the following examples to copy a text file among FSx, S3 and local storage:

.. code-block:: python

    # create a FSx path including server, folders and file name
    >>> p = FsxPath(fsx.server, "share", "test", "input.csv")
    # display the absolute path
    >>> print(p.abspath)
    amznfsx3sh9aujr.corp.fsxvpc.com\share\test\input.csv
    # remove the file if it exists on FSx.
    >>> p.remove_if_exists()

    # check if a file exists or not
    >>> p.exists()
    False
    # create another FSx path
    >>> p = FsxPath(fsx.server, "share", "test", "new.csv")

    # upload a file from local to a FSx server
    >>> p.copy_from(Path('./input.csv'))
    copy from /Users/cheyaohu/WorkDocs/Open_Source/fsxpathlib-project/examples/input.csv to amznfsx3sh9aujr.corp.fsxvpc.com\share\test\new.csv
      done
    True

    # copy a file from FSx into a local folder
    >>> p.copy_to(Path('./new.csv'))
    copy from amznfsx3sh9aujr.corp.fsxvpc.com\share\test\new.csv to /Users/cheyaohu/WorkDocs/Open_Source/fsxpathlib-project/examples/new.csv
    True
    # check if the local file exists
    >>> file_exists = os.path.exists('new.csv')
    >>> print(file_exists)
    True

    # print out the content of a file in a FSx folder
    >>> print(p.read_text())
    name, id
    ivan, 1
    chen, 2

    # copy a file from FSx into S3 bucket
    >>> s3path_prefix = S3Path("fsx-cheyaohu", "demo", "input.csv")
    >>> p.copy_to(s3path_prefix)
    copy from amznfsx3sh9aujr.corp.fsxvpc.com\share\test\new.csv to s3://fsx-cheyaohu/demo/input.csv
      done
    True

Dev Runbook
------------------------------------------------------------------------------

1. Setup Virtualenv:

.. code-block:: bash

    # Create a Python virtual environment for dev / test
    $ virtualenv -p python3.8 venv

    # Enter virtualenv
    $ source ./venv/bin/activate

    # pip install this library and dependencies
    $ pip install -e .

2. Run Tests:

.. code-block:: bash

    # pip install test dependencies
    # NOTE YOU MAY NEED TO RE-ENTER virtualenv
    $ pip install -r requirements-test.txt

    # run unit test and code coverage test
    $ pytest tests -s --cov=fsxpathlib --cov-report term-missing --cov-report "annotate:fsxpathlib/.coverage.annotate"

3. Package and Publish:

.. code-block:: bash

    # pip install development dependencies
    # NOTE YOU MAY NEED TO RE-ENTER virtualenv
    $ pip install -r requirements-dev.txt

    # build artifacts locally
    $ bash ./bin/build.sh

    # publish to https://pypi.org
    $ bash ./bin/publish.sh

1. Then create a release branch ``release/x.y.z`` that match the version.
2. Tag the repo from this branch using naming convention ``x.y.z``.
3. Create a GitHub Release that name matching this version using naming convention ``x.y.z``, and upload the ``.whl`` file to the Release.

Contributing
------------

Please see the `Contribution Guidelines`_.


Copyright
---------

fsxpathlib is an open source project. See the license_ file for more information.

.. _license: LICENSE
.. _`Python 3 virtual environment`: https://docs.python.org/3/library/venv.html
.. _`on-line document`: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
.. _`AWS on-line document`: https://docs.aws.amazon.com/mediapackage/latest/ug/setting-up-create-iam-user.html
.. _link: https://portal.aws.amazon.com/billing/signup
.. _`AWS account`: https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fportal.aws.amazon.com%2Fbilling%2Fsignup%2Fresume&client_id=signup
.. _Release: https://gitlab.aws.dev/aws-data-lab/bookmark-utils/uploads/1e568881ada0ecc8e50d044f962f62f4/bookmark_utils-1.0.0-py2.py3-none-any.whl
.. _`smbprotocol`: https://pypi.org/project/smbprotocol/
.. _`Contribution Guidelines`: CONTRIBUTING.md
.. _`boto3 FSx client APIs`: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#client
.. _`FSx (for Windows File Server)`: https://aws.amazon.com/fsx/
.. _`tutorial link`: https://aws.amazon.com/blogs/storage/accessing-smb-file-shares-remotely-with-amazon-fsx-for-windows-file-server/
.. _`wheel file`: https://gitlab.aws.dev/aws-data-lab/fsxpathlib-project/uploads/13fd6b7cac83cfdc666f6abb8f0e983b/fsxpathlib-0.0.1-py2.py3-none-any.whl