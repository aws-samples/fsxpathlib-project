# -*- coding: utf-8 -*-

"""
This module implements the Fsx authentication client.
"""

# built-in library comes first
from typing import List
from contextlib import contextmanager

# then third party library
import boto3
from boto_session_manager import BotoSesManager, AwsServiceEnum
import smbclient
from smbprotocol.session import Session

# then relative import
from . import exc


class FileSystem:
    """
    Represent an instance of AWS File System. Just a data class.

    .. versionadded:: 0.0.1
    """

    class TypeEnum:
        WINDOWS = "WINDOWS"
        LUSTRE = "LUSTRE"
        ONTAP = "ONTAP"
        OPENZFS = "OPENZFS"

    class StorageTypeEnum:
        SSD = "SSD"
        HHD = "HHD"

    def __init__(
        self,
        arn: str,
        dns_name: str,
        owner_id: str,
        type: str,
        storage_capacity: int,
        storage_type: str,
        vpc_id: str,
        subnets: List[str],
        active_directory_id: str,
        preferred_subnet: str,
        preferred_file_server_ip: str,
    ):
        self.arn = arn
        self.dns_name = dns_name
        self.owner_id = owner_id
        self.type = type
        self.storage_capacity = storage_capacity
        self.storage_type = storage_type
        self.vpc_id = vpc_id
        self.subnets = subnets
        self.active_directory_id = active_directory_id
        self.preferred_subnet = preferred_subnet
        self.preferred_file_server_ip = preferred_file_server_ip


class FSxClient:
    """
    Initialize a connection and session to the FSx (for Windows File Server) service

    :param fsx_file_system_id: FSx File System Id, you can find it in AWS Console
        https://console.aws.amazon.com/fsx/home#file-systems
    :param ad_username: the Active Directory username you use for authentication
    :param ad_password: the Active Directory password you use for authentication
    :param ad_domain: the Active Directory domain name. For example, ``corp.fsxvpc.com``
    :param auth_protocol: authorization protocol. Defaults to ``negotiate``.
    :param require_secure_negotiate: if need a secure negotiation. Defaults to True.
    :param encrypt: is need to encrypt connection. Defaults to False.
    :param require_signing: is need signing. Defaults to True.
    :param root_directory:
    :param boto_ses:

    .. versionadded:: 0.0.1
    """

    def __init__(
        self,
        fsx_file_system_id: str,
        ad_username: str,
        ad_password: str,
        auth_protocol: str = "negotiate",
        require_secure_negotiate: bool = True,
        encrypt: bool = False,
        require_signing: bool = True,
        root_directory: str = "share",
        boto_session_manager: BotoSesManager = None,
    ):
        self.fsx_file_system_id = fsx_file_system_id
        self.ad_username = ad_username
        self.ad_password = ad_password
        self.auth_protocol = auth_protocol
        self.require_secure_negotiate = require_secure_negotiate
        self.encrypt = encrypt
        self.require_signing = require_signing
        self.root_directory = root_directory
        if boto_session_manager is None:
            self.bsm = BotoSesManager()
        else:  # pragma: no cover
            self.bsm = boto_session_manager

        try:
            response = self.bsm.get_client(AwsServiceEnum.FSx).describe_file_systems(
                FileSystemIds=[fsx_file_system_id, ],
                MaxResults=2
            )
            n_fs = len(response.get("FileSystems", list()))
            if n_fs != 1:  # pragma: no cover
                raise exc.FsxError(
                    f"Found {n_fs} filesystems with FileSystemId {fsx_file_system_id!r}!"
                )
            fs_dct = response["FileSystems"][0]
            self.fs: FileSystem = FileSystem(
                arn=fs_dct["ResourceARN"],
                dns_name=fs_dct["DNSName"],
                owner_id=fs_dct["OwnerId"],
                type=fs_dct["FileSystemType"],
                storage_capacity=fs_dct["StorageCapacity"],
                storage_type=fs_dct["StorageType"],
                vpc_id=fs_dct["VpcId"],
                subnets=fs_dct["SubnetIds"],
                active_directory_id=fs_dct["WindowsConfiguration"]["ActiveDirectoryId"],
                preferred_subnet=fs_dct["WindowsConfiguration"]["PreferredSubnetId"],
                preferred_file_server_ip=fs_dct["WindowsConfiguration"]["PreferredFileServerIp"],
            )
        except Exception as e:  # pragma: no cover
            raise exc.FsxError(f"Failed to get info from the FXs server. Error details: {e}")

    def create_session(
        self,
        connection_timeout: int = 60,
    ) -> Session:
        """
        Create SMB session.

        .. versionadded:: 0.0.1
        """
        return smbclient.register_session(
            server=self.fs.dns_name,
            username=self.ad_username,
            password=self.ad_password,
            connection_timeout=connection_timeout,
            encrypt=self.encrypt,
            auth_protocol=self.auth_protocol,
            require_signing=self.require_signing
        )

    @contextmanager
    def session(
        self,
        connection_timeout: int = 60,
    ) -> Session:
        """
        Use context manager syntax to wrap a code block. SMB Session will be
        automatically closed when leaving the code block.

        .. versionadded:: 0.0.1
        """
        try:
            self._session = self.create_session(connection_timeout)
            yield self._session
        finally:
            smbclient.delete_session(server=self.fs.dns_name)

    @property
    def server(self) -> str:
        """
        Return file system server name.

        Example:: amznfsx1a2b3c4d.corp.fsxvpc.com

        .. versionadded:: 0.0.1
        """
        return self.fs.dns_name
