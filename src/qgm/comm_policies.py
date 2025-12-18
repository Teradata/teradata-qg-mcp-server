"""
Manager for QueryGrid communication policies.
"""

from __future__ import annotations

from typing import Any

from .base import BaseClient


class CommPolicyClient(BaseClient):
    """Manager for QueryGrid communication policies."""

    BASE_ENDPOINT = "/api/config/comm-policies"

    def get_comm_policies(
        self,
        flatten: bool = False,
        extra_info: bool = False,
        filter_by_name: str | None = None,
        filter_by_tag: str | None = None,
    ) -> Any:
        """
        Retrieve the list of QueryGrid communication policy objects from the API.

        Args:
            flatten (bool): Flatten versions into array elements. Defaults to False.
            extra_info (bool): Include extra details. Defaults to False.
            filter_by_name (str | None): Filter by name.
            filter_by_tag (str | None): Filter by tag (comma-separated key:value pairs).

        Returns:
            dict[str, Any]: A dictionary containing the list of communication policies.
        """
        api_endpoint = self.BASE_ENDPOINT
        params: dict[str, Any] = {}
        if flatten:
            params["flatten"] = flatten
        if extra_info:
            params["extraInfo"] = extra_info
        if self._is_valid_param(filter_by_name):
            params["filterByName"] = filter_by_name
        if self._is_valid_param(filter_by_tag):
            params["filterByTag"] = filter_by_tag
        return self._request("GET", api_endpoint, params=params)

    def get_comm_policy_by_id(self, id: str, extra_info: bool = False) -> Any:
        """
        Retrieve a specific communication policy by ID.

        Args:
            id (str): The policy ID.
            extra_info (bool): Include extra details.

        Returns:
            dict[str, Any]: The communication policy details.
        """
        params = {}
        if extra_info:
            params["extraInfo"] = extra_info
        return self._request("GET", f"{self.BASE_ENDPOINT}/{id}", params=params)

    def get_comm_policy_active(self, id: str) -> Any:
        """Get the active version of a communication policy."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/active"
        return self._request("GET", api_endpoint)

    def get_comm_policy_pending(self, id: str) -> Any:
        """Get the pending version of a communication policy."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/pending"
        return self._request("GET", api_endpoint)

    def get_comm_policy_previous(self, id: str) -> Any:
        """Get the previous version of a communication policy."""
        api_endpoint = f"{self.BASE_ENDPOINT}/{id}/previous"
        return self._request("GET", api_endpoint)

    def delete_comm_policy(self, id: str) -> Any:
        """Delete a communication policy by ID.

        Args:
            id: The ID of the communication policy to delete.

        Returns:
            The API response.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}")

    def create_comm_policy(
        self,
        name: str,
        transfer_concurrency: int,
        description: str | None = None,
        security_option: str = "INTEGRITY_SECURE_ENCRYPTION_ALL",
        security_algorithm: str = "AES_GCM",
        integrity_headers_only: bool = False,
        authentication_key_size: int = 1536,
        encryption_key_size: int = 128,
        compression_algorithm: str | None = None,
        policy_version: int = 2,
        tags: dict[str, str] | None = None,
    ) -> Any:
        """
        Create a new communication policy in QueryGrid Manager.

        Args:
            name (str): The name of the communication policy.
            transfer_concurrency (int): The number of streams to use for communication between node pairs
                for transferring data.
            description (str | None): Optional description of the communication policy.
            security_option (str): Optional type of security mechanisms to enable for communication.
                Valid options:
                - INTEGRITY_NONE_ENCRYPTION_NONE: IP-based Authentication, no integrity check, no encryption
                - INTEGRITY_CHECKSUM_ENCRYPTION_NONE: IP-based authentication, checksum integrity check,
                    no encryption
                - INTEGRITY_SECURE_ENCRYPTION_CREDENTIALS_ONLY: Key-based authentication, secure Integrity
                    checks, encrypt credentials
                - INTEGRITY_SECURE_ENCRYPTION_ALL: Key-based authentication, secure Integrity checks,
                    encrypt all data (default)
            security_algorithm (str): The algorithm to use for integrity checks and encryption.
                Defaults to "AES_GCM". Valid options: AES_CRC32C, AES_GCM, AES_SHA256, AES_SHA512
            integrity_headers_only (bool): Only perform integrity checks on message headers. Defaults to False.
            authentication_key_size (int): The size of the authentication key. Defaults to 1536.
            encryption_key_size (int): The size of the encryption key. Defaults to 128.
            compression_algorithm (str | None): Optional compression algorithm to use.
                Defaults to "NONE" when not provided. Valid options: NONE, ZSTD
            policy_version (int): The version of comm-policy. Defaults to 2.
                Valid options: 1, 2
            tags (dict[str, str] | None): Optional string key/value pairs for associating some context
                with the communication policy.

        Returns:
            dict[str, Any]: The response from the API.
        """
        api_endpoint = self.BASE_ENDPOINT
        data: dict[str, Any] = {
            "name": name,
            "transferConcurrency": transfer_concurrency,
            "description": description,
            "securityOption": security_option,
            "securityAlgorithm": security_algorithm,
            "integrityHeadersOnly": integrity_headers_only,
            "authenticationKeySize": authentication_key_size,
            "encryptionKeySize": encryption_key_size,
            "compressionAlgorithm": compression_algorithm,
            "policyVersion": policy_version,
            "tags": tags,
        }
        return self._request("POST", api_endpoint, json=data)

    def update_comm_policy(
        self,
        id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> Any:
        """
        Update a communication policy using PATCH (partial update).

        Args:
            id (str): The ID of the communication policy to update.
            name (str | None): The name of the communication policy.
            description (str | None): Description of the communication policy.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {}
        if self._is_valid_param(name):
            data["name"] = name
        if self._is_valid_param(description):
            data["description"] = description

        return self._request("PATCH", f"{self.BASE_ENDPOINT}/{id}", json=data)

    def update_comm_policy_active(
        self,
        id: str,
        version_id: str,
    ) -> Any:
        """
        Activate a specific version (pending or previous) of a communication policy using PATCH.

        NOTE FOR LLMs: When a comm-policy is created, the response contains:
        - 'id': The policy wrapper ID (remains constant across versions)
        - 'versionId': The specific version ID (unique for each active/pending/previous version)

        To activate a pending or previous version:
        1. Get the pending/previous version using get_comm_policy_pending() or get_comm_policy_previous()
        2. Extract the 'versionId' from that response
        3. Call this method with the policy 'id' and the 'versionId' to activate

        Args:
            id (str): The policy wrapper ID (constant across all versions).
            version_id (str): The specific version ID to activate (from pending or previous version).

        Returns:
            dict[str, Any]: The response from the API.
        """
        return self._request(
            "PATCH", f"{self.BASE_ENDPOINT}/{id}/active", data=version_id
        )

    def put_comm_policy_active(
        self,
        id: str,
        name: str,
        transfer_concurrency: int,
        description: str | None = None,
        security_option: str = "INTEGRITY_SECURE_ENCRYPTION_ALL",
        security_algorithm: str = "AES_GCM",
        integrity_headers_only: bool = False,
        authentication_key_size: int = 1536,
        encryption_key_size: int = 128,
        compression_algorithm: str | None = None,
        policy_version: int = 2,
        tags: dict[str, str] | None = None,
    ) -> Any:
        """
        Update the active version of a communication policy using PUT (full replacement).

        Args:
            id (str): The ID of the communication policy.
            name (str): The name of the communication policy.
            transfer_concurrency (int): The number of streams to use for communication.
            description (str | None): Description of the communication policy.
            security_option (str): Type of security mechanisms to enable.
            security_algorithm (str): The algorithm to use for integrity checks and encryption.
            integrity_headers_only (bool): Only perform integrity checks on message headers.
            authentication_key_size (int): The size of the authentication key.
            encryption_key_size (int): The size of the encryption key.
            compression_algorithm (str | None): Compression algorithm to use.
            policy_version (int): The version of comm-policy.
            tags (dict[str, str] | None): String key/value pairs for context.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {
            "name": name,
            "transferConcurrency": transfer_concurrency,
            "description": description,
            "securityOption": security_option,
            "securityAlgorithm": security_algorithm,
            "integrityHeadersOnly": integrity_headers_only,
            "authenticationKeySize": authentication_key_size,
            "encryptionKeySize": encryption_key_size,
            "compressionAlgorithm": compression_algorithm,
            "policyVersion": policy_version,
            "tags": tags,
        }
        return self._request("PUT", f"{self.BASE_ENDPOINT}/{id}/active", json=data)

    def put_comm_policy_pending(
        self,
        id: str,
        transfer_concurrency: int,
        description: str | None = None,
        security_option: str = "INTEGRITY_SECURE_ENCRYPTION_ALL",
        security_algorithm: str = "AES_GCM",
        integrity_headers_only: bool = False,
        authentication_key_size: int = 1536,
        encryption_key_size: int = 128,
        compression_algorithm: str | None = None,
        policy_version: int = 2,
        tags: dict[str, str] | None = None,
    ) -> Any:
        """
        Create or replace the pending version of a communication policy using PUT.

        Args:
            id (str): The ID of the communication policy.
            transfer_concurrency (int): The number of streams to use for communication.
            description (str | None): Description of the communication policy.
            security_option (str): Type of security mechanisms to enable.
            security_algorithm (str): The algorithm to use for integrity checks and encryption.
            integrity_headers_only (bool): Only perform integrity checks on message headers.
            authentication_key_size (int): The size of the authentication key.
            encryption_key_size (int): The size of the encryption key.
            compression_algorithm (str | None): Compression algorithm to use.
            policy_version (int): The version of comm-policy.
            tags (dict[str, str] | None): String key/value pairs for context.

        Returns:
            dict[str, Any]: The response from the API.
        """
        data: dict[str, Any] = {
            "transferConcurrency": transfer_concurrency,
            "description": description,
            "securityOption": security_option,
            "securityAlgorithm": security_algorithm,
            "integrityHeadersOnly": integrity_headers_only,
            "authenticationKeySize": authentication_key_size,
            "encryptionKeySize": encryption_key_size,
            "compressionAlgorithm": compression_algorithm,
            "policyVersion": policy_version,
            "tags": tags,
        }
        return self._request("PUT", f"{self.BASE_ENDPOINT}/{id}/pending", json=data)

    def delete_comm_policy_pending(self, id: str) -> Any:
        """
        Delete the pending version of a communication policy.

        Args:
            id (str): The ID of the communication policy.

        Returns:
            dict[str, Any]: The response from the API.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}/pending")

    def delete_comm_policy_previous(self, id: str) -> Any:
        """
        Delete the previous version of a communication policy.

        Args:
            id (str): The ID of the communication policy.

        Returns:
            dict[str, Any]: The response from the API.
        """
        return self._request("DELETE", f"{self.BASE_ENDPOINT}/{id}/previous")
