"""Pytest configuration for test suite."""

import os
import sys
from pathlib import Path
import pytest

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv

    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    # python-dotenv not installed, continue without .env support
    pass

# Add project root to path for test imports (allows 'from src.module import')
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def pytest_addoption(parser):
    """Add custom command line options for pytest."""
    parser.addoption(
        "--force",
        action="store_true",
        default=False,
        help="Skip confirmation prompt and automatically accept test execution disclaimer",
    )


def pytest_configure(config):
    """Display warning and get user confirmation before running tests."""
    # Skip confirmation if --force flag is provided
    if config.getoption("--force"):
        return

    # Skip confirmation if running with --collect-only or other non-test-execution modes
    if config.getoption("--collect-only") or config.getoption(
        "--setup-only", default=False
    ):
        return

    # Skip confirmation if only running unit tests
    markexpr = config.getoption("-m", default="")
    if markexpr == "unit":
        return

    # Get QGM connection details
    qg_host = os.getenv("QG_MANAGER_HOST", "not-configured")
    qg_port = os.getenv("QG_MANAGER_PORT", "not-configured")
    qg_username = os.getenv("QG_MANAGER_USERNAME", "not-configured")
    qg_url = f"https://{qg_host}:{qg_port}"

    # Display warning message
    warning_message = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                           ⚠️  TEST EXECUTION WARNING                        ║
╚════════════════════════════════════════════════════════════════════════════╝

Running these tests will CREATE, MODIFY, and DELETE entities in the QueryGrid
Manager instance configured in your environment.

QueryGrid Manager Configuration:
  • URL:      {qg_url}
  • Host:     {qg_host}
  • Port:     {qg_port}
  • Username: {qg_username}

Test entities (datacenters, systems, connectors, bridges, fabrics, policies,
user mappings, etc.) will be created with names prefixed with 'test_' or
'pytest_'. These entities are automatically cleaned up after test execution.

Note: Tests will attempt to clean up created entities after execution, but
some entities may remain if tests are interrupted or fail during cleanup.

To skip this prompt in future runs, use: pytest --force

"""

    # Import needed for capture suspension
    import sys
    from _pytest.capture import CaptureManager

    # Get the capture manager from config
    capmanager = config.pluginmanager.get_plugin("capturemanager")

    # Temporarily suspend output capturing
    if capmanager:
        capmanager.suspend_global_capture(in_=True)

    try:
        # Print warning directly to terminal
        print(warning_message, file=sys.stderr)
        sys.stderr.flush()

        # Get user confirmation
        try:
            print(
                "Do you want to continue? [y/N]: ", end="", file=sys.stderr, flush=True
            )
            response = sys.stdin.readline().strip().lower()

            if response not in ["y", "yes"]:
                print("\n❌ Test execution cancelled by user.\n", file=sys.stderr)
                pytest.exit("Test execution cancelled by user", returncode=1)
            print("\n✓ Test execution confirmed. Proceeding...\n", file=sys.stderr)
        except (KeyboardInterrupt, EOFError):
            print("\n\n❌ Test execution cancelled by user.\n", file=sys.stderr)
            pytest.exit("Test execution cancelled by user", returncode=1)
    finally:
        # Resume output capturing
        if capmanager:
            capmanager.resume_global_capture()


@pytest.fixture(scope="session")
def qg_manager():
    """
    Fixture to provide QueryGrid Manager instance for integration tests.

    QueryGridManager automatically reads configuration from environment variables:
    - QG_MANAGER_HOST
    - QG_MANAGER_PORT
    - QG_MANAGER_USERNAME
    - QG_MANAGER_PASSWORD
    - QG_MANAGER_VERIFY_SSL (optional, defaults to true)
    """
    import os
    from src.qgm.querygrid_manager import QueryGridManager

    # Verify required environment variables are set
    required_vars = [
        "QG_MANAGER_HOST",
        "QG_MANAGER_PORT",
        "QG_MANAGER_USERNAME",
        "QG_MANAGER_PASSWORD",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        pytest.skip(
            f"QueryGrid Manager credentials not configured. Missing: {', '.join(missing_vars)}"
        )

    # Read optional verify_ssl from environment
    verify_ssl_str = os.getenv("QG_MANAGER_VERIFY_SSL", "true")
    verify_ssl = verify_ssl_str.lower() in ("true", "1", "yes")

    # QueryGridManager reads host, port, username, password from environment variables
    # Pass verify_ssl explicitly since we read it here
    manager = QueryGridManager(verify_ssl=verify_ssl)
    yield manager
    manager.close()


def _get_or_create_datacenter(qg_manager):
    """Get existing or create new test datacenter."""
    existing_datacenters = qg_manager.datacenter_client.get_datacenters(
        filter_by_name="test_datacenter_pytest"
    )

    if isinstance(existing_datacenters, list) and len(existing_datacenters) > 0:
        datacenter_id = existing_datacenters[0].get("id")
        print(f"\n✓ Using existing test datacenter: {datacenter_id}")
        return datacenter_id

    # Create a test datacenter
    datacenter_result = qg_manager.datacenter_client.create_datacenter(
        name="test_datacenter_pytest",
        description="Test datacenter created by pytest for integration tests",
    )

    if isinstance(datacenter_result, dict) and datacenter_result.get("id"):
        datacenter_id = datacenter_result["id"]
        print(f"\n✓ Created test datacenter: {datacenter_id}")
        return datacenter_id

    print(f"\n⚠ Failed to create test datacenter: {datacenter_result}")
    return None


def _validate_software_packages(qg_manager):
    """Validate that all required software packages are present.

    Returns:
        dict: Contains 'node_version', 'fabric_version', 'connector_version'
    """
    software_list = qg_manager.software_client.get_software()

    if not isinstance(software_list, list) or len(software_list) == 0:
        _fail_with_no_software_error()
        return None

    # Look for required software types using 'type' field (not 'softwareType')
    node_software = [s for s in software_list if s.get("type") == "NODE"]
    fabric_software = [s for s in software_list if s.get("type") == "FABRIC"]
    connector_software = [s for s in software_list if s.get("type") == "CONNECTOR"]

    # Check what's missing
    missing_types = []
    if not node_software:
        missing_types.append("NODE")
    if not fabric_software:
        missing_types.append("FABRIC")
    if not connector_software:
        missing_types.append("CONNECTOR")

    if missing_types:
        _fail_with_missing_software_error(
            missing_types,
            software_list,
            node_software,
            fabric_software,
            connector_software,
        )
        return None

    # All required software found - return all versions
    node_version = node_software[0].get("version")
    fabric_version = fabric_software[0].get("version")
    connector_version = connector_software[0].get("version")

    print(f"✓ Using NODE software version: {node_version}")
    print(f"✓ Using FABRIC software version: {fabric_version}")
    print(f"✓ Using CONNECTOR software version: {connector_version}")

    return {
        "node_version": node_version,
        "fabric_version": fabric_version,
        "connector_version": connector_version,
    }


def _fail_with_no_software_error():
    """Fail tests with detailed error when no software packages are found."""
    qg_host = os.getenv("QG_MANAGER_HOST", "unknown")
    qg_port = os.getenv("QG_MANAGER_PORT", "unknown")
    qg_url = f"https://{qg_host}:{qg_port}"

    error_msg = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ NO SOFTWARE PACKAGES FOUND                                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

QueryGrid Manager has no software packages uploaded.

QueryGrid Manager Details:
  URL:      {qg_url}
  Host:     {qg_host}
  Port:     {qg_port}
  Username: {os.getenv("QG_MANAGER_USERNAME", "unknown")}

Required Software Packages:
  1. NODE software package (for QueryGrid nodes)
  2. FABRIC software package (for fabric connectivity)
  3. CONNECTOR software package (for Teradata system connectivity)

To upload software packages:
  1. Access the QueryGrid Manager UI at: {qg_url}
  2. Navigate to: Configuration > Software
  3. Click "Upload" or "Add Software"
  4. Upload the required software packages:
     - QueryGrid Node software (.tar.gz or .rpm)
     - QueryGrid Fabric software
     - Teradata Connector software

Tests cannot proceed without software packages. Please upload them first.
"""
    pytest.fail(error_msg)


def _fail_with_missing_software_error(
    missing_types, software_list, node_software, fabric_software, connector_software
):
    """Fail tests with detailed error when some required software is missing."""
    qg_host = os.getenv("QG_MANAGER_HOST", "unknown")
    qg_port = os.getenv("QG_MANAGER_PORT", "unknown")
    qg_url = f"https://{qg_host}:{qg_port}"

    available_types = [
        str(s.get("type")) for s in software_list if s.get("type") is not None
    ]
    available_str = ", ".join(available_types) if available_types else "None"

    # Show software names and versions for debugging
    software_info = []
    for s in software_list:
        name = s.get("name", "Unknown")
        version = s.get("version", "Unknown")
        sw_type = s.get("type", "Unknown")
        software_info.append(f"  - {name} v{version} (type: {sw_type})")
    software_details = "\n".join(software_info) if software_info else "  None"

    error_msg = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ MISSING REQUIRED SOFTWARE PACKAGES                                         ║
╚════════════════════════════════════════════════════════════════════════════╝

Missing software package types: {', '.join(missing_types)}

QueryGrid Manager Details:
  URL:      {qg_url}
  Host:     {qg_host}
  Port:     {qg_port}
  Username: {os.getenv("QG_MANAGER_USERNAME", "unknown")}

Required Software Packages:
  1. NODE software package (for QueryGrid nodes) {'✓ Found' if node_software else '✗ MISSING'}
  2. FABRIC software package (for fabric connectivity) {'✓ Found' if fabric_software else '✗ MISSING'}
  3. CONNECTOR software package (for Teradata system connectivity) {'✗ MISSING' if not connector_software else '✓ Found'}

To upload software packages:
  1. Access the QueryGrid Manager UI at: {qg_url}
  2. Navigate to: Configuration > Software
  3. Click "Upload" or "Add Software"
  4. Upload the missing software packages:
     {'- QueryGrid Node software (.tar.gz or .rpm)' if not node_software else ''}
     {'- QueryGrid Fabric software' if not fabric_software else ''}
     {'- Teradata Connector software' if not connector_software else ''}

Available software types in QGM: {available_str}

Software packages found in QGM:
{software_details}

Tests cannot proceed without all required software packages.
"""
    pytest.fail(error_msg)


def _get_or_create_system(qg_manager, datacenter_id, node_version):
    """Get existing or create new test system.

    Args:
        qg_manager: QueryGrid Manager instance
        datacenter_id: ID of the datacenter
        node_version: NODE software version to use
    """
    existing_systems = qg_manager.system_client.get_systems(
        filter_by_name="test_system_pytest"
    )

    if isinstance(existing_systems, list) and len(existing_systems) > 0:
        system_id = existing_systems[0].get("id")
        print(f"✓ Using existing test system: {system_id}")
        return system_id

    try:
        system_result = qg_manager.system_client.create_system(
            name="test_system_pytest",
            system_type="TERADATA",
            platform_type="ON_PREM",
            description="Test system created by pytest for integration tests",
            data_center_id=datacenter_id,
            software_version=node_version,
            maximum_memory_per_node=1073741824,  # 1GB in bytes
        )

        if isinstance(system_result, dict) and system_result.get("id"):
            system_id = system_result["id"]
            print(f"✓ Created test system: {system_id}")
            return system_id

        print(f"⚠ Failed to create test system: {system_result}")
        return None

    except Exception as e:
        error_msg = str(e)
        if hasattr(e, "response") and e.response is not None:
            try:
                error_msg = f"{e}\nResponse: {e.response.text}"
            except Exception:
                pass
        print(f"⚠ Error creating test system: {error_msg}")
        return None


@pytest.fixture(scope="session")
def test_infrastructure(qg_manager):
    """
    Create test infrastructure (datacenter, software, system) for integration tests.

    This fixture creates a test datacenter and system that can be used across
    multiple test cases. The infrastructure is created once per test session
    and cleaned up (if supported by the API) when tests complete.

    Returns:
        dict: Contains 'datacenter_id', 'node_version', 'fabric_version',
              'connector_version', and 'system_id'
    """
    created_resources = {
        "datacenter_id": None,
        "node_version": None,
        "fabric_version": None,
        "connector_version": None,
        "system_id": None,
    }

    try:
        # Get or create datacenter
        created_resources["datacenter_id"] = _get_or_create_datacenter(qg_manager)

        # Validate required software packages
        try:
            software_versions = _validate_software_packages(qg_manager)
            if software_versions:
                created_resources["node_version"] = software_versions.get(
                    "node_version"
                )
                created_resources["fabric_version"] = software_versions.get(
                    "fabric_version"
                )
                created_resources["connector_version"] = software_versions.get(
                    "connector_version"
                )
        except Exception as e:
            qg_host = os.getenv("QG_MANAGER_HOST", "unknown")
            qg_port = os.getenv("QG_MANAGER_PORT", "unknown")

            error_msg = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ ERROR CHECKING SOFTWARE PACKAGES                                           ║
╚════════════════════════════════════════════════════════════════════════════╝

Failed to retrieve software packages from QueryGrid Manager.

QueryGrid Manager: https://{qg_host}:{qg_port}

Error: {e}

Please verify:
  1. QueryGrid Manager is accessible
  2. Credentials are correct
  3. User has permissions to view software
  4. Software packages are uploaded to the manager
"""
            pytest.fail(error_msg)

        # Create test system if we have datacenter and node software version
        if created_resources["datacenter_id"] and created_resources["node_version"]:
            created_resources["system_id"] = _get_or_create_system(
                qg_manager,
                created_resources["datacenter_id"],
                created_resources["node_version"],
            )

    except Exception as e:
        error_msg = str(e)
        if hasattr(e, "response") and e.response is not None:
            try:
                error_msg = f"{e}\nResponse: {e.response.text}"
            except Exception:
                pass
        print(f"\n⚠ Error during test infrastructure setup: {error_msg}")
        print("Tests will skip operations requiring test infrastructure")

    yield created_resources

    # Cleanup - Delete created resources in reverse order
    print("\n🗑️  Cleaning up test infrastructure...")

    # Delete system first (dependent on datacenter)
    if created_resources.get("system_id"):
        try:
            qg_manager.system_client.delete_system(created_resources["system_id"])
            print(f"✓ Deleted test system: {created_resources['system_id']}")
        except Exception as e:
            print(f"⚠ Failed to delete test system: {e}")

    # Delete datacenter last (parent resource)
    if created_resources.get("datacenter_id"):
        try:
            qg_manager.datacenter_client.delete_datacenter(
                created_resources["datacenter_id"]
            )
            print(f"✓ Deleted test datacenter: {created_resources['datacenter_id']}")
        except Exception as e:
            print(f"⚠ Failed to delete test datacenter: {e}")

    print("✓ Test infrastructure cleanup complete")


@pytest.fixture(scope="session")
def test_fabric(qg_manager, test_infrastructure):
    """
    Create or get a test fabric for integration tests.

    This fixture attempts to create a new fabric for testing. If fabric creation
    fails (which may occur due to QueryGrid Manager configuration requirements),
    it falls back to using an existing fabric.

    Note: Fabric creation may require additional QueryGrid Manager configuration
    such as network setup, which is why existing fabrics are used as fallback.

    Returns:
        dict: Fabric details including 'id', 'name', etc.
    """
    # Get fabric software version from test_infrastructure
    fabric_version = test_infrastructure.get("fabric_version")

    if not fabric_version:
        pytest.skip("No FABRIC software version available to create test fabric")

    # Attempt to create test fabric with required parameters
    try:
        fabric = qg_manager.fabric_client.create_fabric(
            name="test_fabric_pytest",
            port=10000,
            softwareVersion=fabric_version,
            authKeySize=2048,
            description="Test fabric created by pytest for integration tests",
        )
        print(f"\n✓ Created test fabric: {fabric.get('id')}")

        yield fabric

        # Cleanup - delete the test fabric
        print("\n🗑️  Cleaning up test fabric...")
        try:
            qg_manager.fabric_client.delete_fabric(fabric.get("id"))
            print(f"✓ Deleted test fabric: {fabric.get('id')}")
        except Exception as e:
            print(f"⚠ Failed to delete test fabric: {e}")
    except Exception as e:
        # If creation fails, use existing fabric as fallback
        # Fabric creation may require additional QGM configuration (networks, etc.)
        print(f"\n⚠ Failed to create test fabric: {e}")
        print(
            "→ Using existing fabric as fallback (fabric creation requires additional QGM setup)"
        )
        try:
            existing_fabrics = qg_manager.fabric_client.get_fabrics()
            if isinstance(existing_fabrics, list) and len(existing_fabrics) > 0:
                fabric = existing_fabrics[0]
                print(
                    f"✓ Using existing fabric: {fabric.get('id')} ({fabric.get('name')})"
                )
                yield fabric
                return
        except Exception as fallback_error:
            print(f"⚠ Could not get existing fabrics: {fallback_error}")
        pytest.skip(
            f"Failed to create test fabric and no existing fabrics available: {e}"
        )


@pytest.fixture(scope="session")
def test_connector(qg_manager, test_infrastructure, test_fabric):
    """
    Create a test connector for integration tests.

    This fixture always creates a new connector for testing.
    The connector is automatically cleaned up after the test session.

    Returns:
        dict: Connector details including 'id', 'name', etc.
    """
    system_id = test_infrastructure.get("system_id")
    fabric_id = test_fabric.get("id")

    if not system_id or not fabric_id:
        pytest.skip(
            "Test infrastructure or fabric not available for connector creation"
        )

    # Get connector software version from test_infrastructure
    connector_version = test_infrastructure.get("connector_version")

    if not connector_version:
        pytest.skip("No CONNECTOR software version available to create test connector")

    # Get connector software name (we still need the name)
    softwares = qg_manager.software_client.get_software()
    connector_software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            connector_software_name = sw.get("name")
            break

    if not connector_software_name:
        pytest.skip(
            f"Could not find CONNECTOR software name for version {connector_version}"
        )

    # Create test connector
    try:
        connector = qg_manager.connector_client.create_connector(
            name="test_connector_pytest",
            software_name=connector_software_name,
            software_version=connector_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description="Test connector created by pytest for integration tests",
        )
        print(f"\n✓ Created test connector: {connector.get('id')}")

        yield connector

        # Cleanup - delete the test connector
        print("\n🗑️  Cleaning up test connector...")
        try:
            qg_manager.connector_client.delete_connector(connector.get("id"))
            print(f"✓ Deleted test connector: {connector.get('id')}")
        except Exception as e:
            print(f"⚠ Failed to delete test connector: {e}")
    except Exception as e:
        pytest.skip(f"Failed to create test connector: {e}")


@pytest.fixture(scope="session")
def test_comm_policy(qg_manager):
    """
    Get or create a test communication policy for integration tests.

    This fixture tries to find an existing comm policy first, and only creates one if needed.
    The policy is automatically cleaned up after the test session if it was created.

    Returns:
        dict: Communication policy details including 'id', 'name', etc.
    """
    # Try to get any existing comm policy first
    try:
        existing_policies = qg_manager.comm_policy_client.get_comm_policies()
        if isinstance(existing_policies, list) and len(existing_policies) > 0:
            policy = existing_policies[0]
            print(
                f"\n✓ Using existing comm policy: {policy.get('id')} ({policy.get('name')})"
            )
            # Don't cleanup since we didn't create it
            yield policy
            return
    except Exception as e:
        print(f"\n⚠ Could not get existing comm policies: {e}")

    # Create test comm policy
    try:
        policy = qg_manager.comm_policy_client.create_comm_policy(
            name="test_comm_policy_pytest",
            transfer_concurrency=4,
            description="Test communication policy created by pytest for integration tests",
        )
        print(f"\n✓ Created test comm policy: {policy.get('id')}")

        yield policy

        # Cleanup - delete the test comm policy
        print("\n🗑️  Cleaning up test comm policy...")
        try:
            qg_manager.comm_policy_client.delete_comm_policy(policy.get("id"))
            print(f"✓ Deleted test comm policy: {policy.get('id')}")
        except Exception as e:
            print(f"⚠ Failed to delete test comm policy: {e}")
    except Exception as e:
        pytest.skip(f"Failed to create test comm policy: {e}")


@pytest.fixture(scope="session")
def test_link(
    qg_manager, test_infrastructure, test_fabric, test_connector, test_comm_policy
):
    """
    Create a test link for integration tests.

    This fixture always creates a new link with two connectors (initiator and target).
    It requires fabric, connectors, and communication policy to exist.
    The link is automatically cleaned up after the test session.

    Returns:
        dict: Link details including 'id', 'name', 'initiatorConnectorId', 'targetConnectorId', etc.
    """
    system_id = test_infrastructure.get("system_id")
    fabric_id = test_fabric.get("id")

    if not system_id or not fabric_id:
        pytest.skip("Test infrastructure or fabric not available for link creation")

    # Get connector software version from test_infrastructure
    connector_version = test_infrastructure.get("connector_version")

    if not connector_version:
        pytest.skip(
            "No CONNECTOR software version available to create second connector for link"
        )

    # Get connector software name (we still need the name)
    softwares = qg_manager.software_client.get_software()
    connector_software_name = None
    for sw in softwares:
        if sw.get("type") == "CONNECTOR" and sw.get("version") == connector_version:
            connector_software_name = sw.get("name")
            break

    if not connector_software_name:
        pytest.skip(
            f"Could not find CONNECTOR software name for version {connector_version}"
        )

    # Create second test connector (target)
    second_connector = None
    try:
        second_connector = qg_manager.connector_client.create_connector(
            name="test_connector_target_pytest",
            software_name=connector_software_name,
            software_version=connector_version,
            fabric_id=fabric_id,
            system_id=system_id,
            description="Test target connector created by pytest for link tests",
        )
        print(
            f"\n✓ Created second test connector (target): {second_connector.get('id')}"
        )
    except Exception as e:
        pytest.skip(f"Failed to create second connector for link: {e}")

    # Create test link
    link = None
    try:
        link = qg_manager.link_client.create_link(
            name="test_link_pytest",
            fabricId=fabric_id,
            initiatorConnectorId=test_connector.get("id"),
            targetConnectorId=second_connector.get("id"),
            commPolicyId=test_comm_policy.get("id"),
            initiatorThreadsPerQuery=4,
            targetThreadsPerQuery=4,
            description="Test link created by pytest for integration tests",
        )
        print(f"\n✓ Created test link: {link.get('id')}")

        yield link

        # Cleanup - delete the test link first, then second connector
        print("\n🗑️  Cleaning up test link...")
        try:
            qg_manager.link_client.delete_link(link.get("id"))
            print(f"✓ Deleted test link: {link.get('id')}")
        except Exception as e:
            print(f"⚠ Failed to delete test link: {e}")

        print("🗑️  Cleaning up second test connector...")
        try:
            qg_manager.connector_client.delete_connector(second_connector.get("id"))
            print(f"✓ Deleted second test connector: {second_connector.get('id')}")
        except Exception as e:
            print(f"⚠ Failed to delete second test connector: {e}")

    except Exception as e:
        # If link creation failed, cleanup the second connector
        error_msg = str(e)
        if hasattr(e, "response") and e.response is not None:
            try:
                error_msg = f"{e}\nResponse: {e.response.text}"
            except Exception:
                pass
        print(f"\n⚠ Failed to create test link: {error_msg}")

        if second_connector:
            try:
                qg_manager.connector_client.delete_connector(second_connector.get("id"))
                print(
                    f"✓ Deleted second test connector after failed link creation: {second_connector.get('id')}"
                )
            except Exception as cleanup_error:
                print(f"⚠ Failed to delete second test connector: {cleanup_error}")
        pytest.skip(f"Failed to create test link: {error_msg}")


def _get_or_create_network(qg_manager):
    """Get existing or create new test network."""
    existing_networks = qg_manager.network_client.get_networks(
        filter_by_name="test_network_pytest"
    )

    if isinstance(existing_networks, list) and len(existing_networks) > 0:
        network_id = existing_networks[0].get("id")
        print(f"\n✓ Using existing test network: {network_id}")
        return existing_networks[0]

    # Create a test network
    network_result = qg_manager.network_client.create_network(
        name="test_network_pytest",
        connection_type="STANDARD",
        description="Test network created by pytest for integration tests",
        matching_rules=[{"type": "CIDR_NOTATION", "value": "0.0.0.0/0"}],
        tags={"environment": "test", "created_by": "pytest"},
    )

    if isinstance(network_result, dict) and network_result.get("id"):
        network_id = network_result["id"]
        print(f"\n✓ Created test network: {network_id}")
        return network_result

    print(f"\n⚠ Failed to create test network: {network_result}")
    return None


@pytest.fixture(scope="session")
def test_network(qg_manager):
    """
    Fixture to provide a test network for integration tests.

    This fixture ensures a test network exists before running network-related tests.
    The network is created with name 'test_network_pytest' and persists across
    the test session to avoid recreation overhead.

    Returns:
        dict: Network object containing 'id', 'name', and other network properties.
    """
    network = _get_or_create_network(qg_manager)

    if network is None:
        pytest.skip("Failed to create or retrieve test network")

    yield network

    # Note: Network is not deleted to allow reuse across test sessions
    # Manual cleanup required if needed


@pytest.fixture
async def mcp_client(qg_manager):
    """
    Create an MCP client fixture for testing MCP tools.

    This fixture provides a FastMCP Client instance that can be used to test
    MCP tools via the call_tool() method. The QueryGrid Manager instance is
    automatically injected into the tools module.

    Usage:
        @pytest.mark.integration
        async def test_my_tool(mcp_client):
            result = await mcp_client.call_tool("tool_name", arguments={})
            assert result.data is not None
    """
    from fastmcp.client import Client
    from src.mcp_server import qg_mcp_server as mcp
    from src import tools

    # Inject the manager instance
    tools.set_qg_manager(qg_manager)

    async with Client(mcp) as client:
        yield client

    # Cleanup
    tools.set_qg_manager(None)
