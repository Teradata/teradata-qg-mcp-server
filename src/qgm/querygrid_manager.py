"""
QueryGrid Manager API client.
"""

from __future__ import annotations

import logging
import os

import requests

from .connectors import ConnectorClient
from .datacenters import DataCenterClient
from .diagnostic_check import DiagnosticCheckClient
from .fabrics import FabricClient
from .issues import IssueClient
from .links import LinkClient
from .managers import ManagerClient
from .networks import NetworkClient
from .node_virtual_ips import NodeVirtualIPClient
from .nodes import NodeClient
from .create_foreign_server import CreateForeignServerClient
from .datasource_registration import DatasourceRegistrationClient
from .operations import OperationsClient
from .privatelink_template import PrivatelinkTemplateClient
from .queries import QueryClient
from .shared_memory_estimator import SharedMemoryEstimatorClient
from .softwares import SoftwareClient
from .systems import SystemClient
from .user_mappings import UserMappingClient
from .users import UserClient
from .support_archive import SupportArchiveClient
from .bridges import BridgeClient
from .comm_policies import CommPolicyClient
from .api_info import ApiInfoClient

logger = logging.getLogger(__name__)


class QueryGridManager:
    """Client for interacting with QueryGrid Manager API."""

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        verify_ssl: bool | None = None,
        request_timeout: int | None = None,
    ):
        """
        Initialize the QueryGrid client.

        Args:
            username: Username for authentication (optional, can be set via QG_MANAGER_USERNAME env var)
            password: Password for authentication (optional, can be set via QG_MANAGER_PASSWORD env var)
            verify_ssl: Whether to verify SSL certificates (optional, can be set via QG_MANAGER_VERIFY_SSL env var)
            request_timeout: Timeout for API requests in seconds (optional, defaults from config.yaml)
        """
        # Load configuration from config.yaml
        try:
            from src.utils import load_config
            config = load_config()
            default_timeout = config.get("querygrid", {}).get("request_timeout", 10)
            default_verify_ssl = config.get("querygrid", {}).get("verify_ssl", True)
        except Exception:
            default_timeout = 10
            default_verify_ssl = True

        # Construct base_url from environment variables
        host = os.getenv("QG_MANAGER_HOST")
        port = os.getenv("QG_MANAGER_PORT")
        if not host or not port:
            raise ValueError("Both QG_MANAGER_HOST and QG_MANAGER_PORT environment variables must be set")

        self.base_url = f"https://{host}:{port}"
        self.username = username or os.getenv("QG_MANAGER_USERNAME")
        self.password = password or os.getenv("QG_MANAGER_PASSWORD")
        if not self.username or not self.password:
            raise ValueError(
                "Both username and password must be provided via arguments or environment "
                "variables QG_MANAGER_USERNAME and QG_MANAGER_PASSWORD"
            )
        
        # Set timeout from parameter, or fall back to config default
        self.request_timeout = request_timeout if request_timeout is not None else default_timeout
        
        if verify_ssl is not None:
            self.verify_ssl = verify_ssl
        else:
            # Check environment variable, then fall back to config default
            env_verify = os.getenv("QG_MANAGER_VERIFY_SSL")
            if env_verify is not None:
                self.verify_ssl = env_verify.lower() in ("true", "1", "yes")
            else:
                self.verify_ssl = default_verify_ssl
        
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.verify = self.verify_ssl

        # Initialize resource managers
        self.manager_client = ManagerClient(self.session, self.base_url)
        self.node_client = NodeClient(self.session, self.base_url)
        self.issue_client = IssueClient(self.session, self.base_url)
        self.system_client = SystemClient(self.session, self.base_url)
        self.connector_client = ConnectorClient(self.session, self.base_url)
        self.link_client = LinkClient(self.session, self.base_url)
        self.fabric_client = FabricClient(self.session, self.base_url)
        self.software_client = SoftwareClient(self.session, self.base_url)
        self.query_client = QueryClient(self.session, self.base_url)
        self.diagnostic_check_client = DiagnosticCheckClient(self.session, self.base_url)
        self.datacenter_client = DataCenterClient(self.session, self.base_url)
        self.bridge_client = BridgeClient(self.session, self.base_url)
        self.comm_policy_client = CommPolicyClient(self.session, self.base_url)
        self.network_client = NetworkClient(self.session, self.base_url)
        self.user_mapping_client = UserMappingClient(self.session, self.base_url)
        self.node_virtual_ip_client = NodeVirtualIPClient(self.session, self.base_url)
        self.user_client = UserClient(self.session, self.base_url)
        self.support_archive_client = SupportArchiveClient(self.session, self.base_url)
        self.api_info_client = ApiInfoClient(self.session, self.base_url)
        self.create_foreign_server_client = CreateForeignServerClient(self.session, self.base_url)
        self.datasource_registration_client = DatasourceRegistrationClient(self.session, self.base_url)
        self.privatelink_template_client = PrivatelinkTemplateClient(self.session, self.base_url)
        self.operations_client = OperationsClient(self.session, self.base_url)
        self.shared_memory_estimator_client = SharedMemoryEstimatorClient(self.session, self.base_url)

        logger.info("Initialized QueryGrid client for %s", self.base_url)

    def close(self) -> None:
        """Close the underlying session."""
        logger.info("Closing QueryGrid Manager session")
        self.session.close()
