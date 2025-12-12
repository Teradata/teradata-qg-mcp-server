# Teradata QueryGrid MCP Server

A Model Context Protocol (MCP) server built with FastMCP that provides comprehensive tools to interact with Teradata QueryGrid Manager. This server enables AI assistants and other MCP clients to manage QueryGrid resources programmatically using a standardized protocol.

## Features

- **Comprehensive QueryGrid Management**: 70+ tools covering all major QueryGrid operations
- **Secure Authentication**: Basic authentication support for QueryGrid Manager
- **RESTful API Integration**: Full CRUD operations for QueryGrid resources
- **Streamable HTTP Transport**: Efficient bidirectional communication using FastMCP
- **Type-Safe**: Fully type-annotated Python code with strict type checking
- **Production-Ready**: Runs on Uvicorn ASGI server for optimal performance
- **Flexible Deployment**: Background daemon or foreground modes with hot reloading
- **Comprehensive Logging**: Configurable logging levels and output destinations
- **Well-Tested**: Comprehensive unit test coverage

## Architecture

```
teradata-qg-mcp-server/
├── src/
│   ├── mcp_server.py          # FastMCP application and server initialization
│   ├── server.py              # Main server entry point
│   ├── utils.py               # Shared utilities and helpers
│   ├── qgm/                   # QueryGrid Manager API clients
│   │   ├── base.py            # Base HTTP client
│   │   ├── querygrid_manager.py  # Main manager class
│   │   ├── systems.py         # Systems API client
│   │   ├── connectors.py      # Connectors API client
│   │   ├── links.py           # Links API client
│   │   ├── fabrics.py         # Fabrics API client
│   │   └── ...                # Other resource clients
│   └── tools/                 # MCP tool implementations (21 modules)
│       ├── __init__.py        # Tool registration
│       ├── system_tools.py    # System management tools
│       ├── connector_tools.py # Connector management tools
│       ├── link_tools.py      # Link management tools
│       └── ...                # Other tool modules
├── tests/                     # Unit tests
├── scripts/                   # Server management scripts
├── docs/                      # Documentation
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   └── TESTING.md             # Testing guide
└── requirements.txt           # Python dependencies

```

## Requirements

- **Python**: 3.13+ (uses modern type annotations)
- **Platform**: Linux, macOS, and Windows
- **Dependencies**: fastmcp, requests, pytest, python-dotenv, fastapi, uvicorn

## Installation

### Quick Start

Follow these steps to get the server running:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Teradata/teradata-qg-mcp-server.git
   cd teradata-qg-mcp-server
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   
   This creates a new virtual environment in the `venv` directory.

3. **Activate the virtual environment:**
   
   **On Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   You should see `(venv)` appear at the beginning of your terminal prompt, indicating the virtual environment is active.

4. **Install dependencies:**
   
   **For production use:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **For development (includes testing and linting tools):**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Configure environment variables:**
   
   Create a `.env` file in the project root (see `.env.example` for reference):
   ```bash
   cp .env.example .env
   # Edit .env with your QueryGrid Manager credentials
   nano .env  # or use your preferred editor
   ```
   
   Required variables:
   ```env
   QG_MANAGER_HOST=your-querygrid-manager.com
   QG_MANAGER_PORT=9443
   QG_MANAGER_USERNAME=your-username
   QG_MANAGER_PASSWORD=your-password
   QG_MANAGER_VERIFY_SSL=false
   ```

6. **Start the server:**
   ```bash
   ./scripts/td-qg-mcp-server.py start
   ```
   
   The server will start in background mode. Check status with:
   ```bash
   ./scripts/td-qg-mcp-server.py status
   ```

### Virtual Environment Notes

- **Always activate the virtual environment** before running the server or any scripts
- If you close your terminal, you'll need to reactivate: `source venv/bin/activate`
- To deactivate the virtual environment: `deactivate`
- The virtual environment is local to your project and not committed to git

### Troubleshooting Installation

**"No module named uvicorn" error:**
- Make sure the virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**"Permission denied" when running scripts:**
- Make the script executable: `chmod +x scripts/td-qg-mcp-server.py`

**Import errors when running the server:**
- Ensure you're in the project root directory
- Verify virtual environment is activated
- Check all dependencies installed: `pip list`

## Configuration

The server uses a **three-tier configuration hierarchy** with clear separation of concerns:

```
Priority: CLI Arguments > Environment Variables > config.yaml
          (Highest)                                (Lowest)
```

### Configuration Hierarchy

1. **config.yaml** (Application Defaults - Lowest Priority)
   - Contains sensible defaults for all settings
   - Includes server configuration, timeouts, and logging settings
   - Safe, non-sensitive values committed to version control
   - See `config.yaml` for all available options

2. **Environment Variables** (Per-Environment Overrides - Middle Priority)
   - Override config.yaml defaults
   - Used for environment-specific settings and sensitive data
   - Can be set via `.env` file or system environment

3. **CLI Arguments** (Runtime Overrides - Highest Priority)
   - Override both environment variables and config.yaml
   - Used for temporary changes and debugging
   - Passed to `td-qg-mcp-server.py` script

**Example:** If `config.yaml` sets `port: 8000`, `.env` sets `QG_MCP_SERVER_PORT=8080`, and you run with `--port 9000`, the server will use port **9000** (CLI wins).

For complete configuration documentation, see [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md).

### Environment Variables

#### QueryGrid Connection (Required)
- `QG_MANAGER_HOST`: QueryGrid Manager host
- `QG_MANAGER_PORT`: QueryGrid Manager port
- `QG_MANAGER_USERNAME`: QueryGrid Manager username
- `QG_MANAGER_PASSWORD`: QueryGrid Manager password
- `QG_MANAGER_VERIFY_SSL`: Whether to verify SSL certificates (default: from `config.yaml`)

#### Server Configuration (Optional - Override config.yaml)
- `QG_MCP_SERVER_HOST`: Host to bind the MCP server to (default: from `config.yaml`)
- `QG_MCP_SERVER_PORT`: Port to bind the MCP server to (default: from `config.yaml`)

#### Server Logging (Optional - Override config.yaml)
- `QG_MCP_SERVER_LOG_FILE`: Path to the log file (optional, if not set logs go to console)
- `QG_MCP_SERVER_LOG_LEVEL`: Logging level - `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (default: from `config.yaml`)

### Using .env Files

You can also use a `.env` file to set environment variables. Create a `.env` file in the project root (see `.env.example` for reference):

```bash
# .env
QG_MANAGER_HOST=your-querygrid-manager.com
QG_MANAGER_PORT=8080
QG_MANAGER_USERNAME=your-username
QG_MANAGER_PASSWORD=your-password
QG_MANAGER_VERIFY_SSL=false
QG_MCP_SERVER_HOST=0.0.0.0
QG_MCP_SERVER_PORT=8000
QG_MCP_SERVER_LOG_LEVEL=DEBUG
```

The server will automatically load the `.env` file if it exists (requires `python-dotenv` package).

### Configuration Files in config.yaml

The `config.yaml` file at the project root contains default settings for:
- **Server**: host, port, health check timeout
- **QueryGrid**: request timeout, SSL verification defaults  
- **Logging**: rotation, retention, formats, and levels

These values serve as sensible defaults and can be overridden by environment variables or CLI arguments.

Example configuration structure:
```yaml
server:
  host: "0.0.0.0"
  port: 8000
  health_check_timeout: 5

querygrid:
  request_timeout: 10
  verify_ssl: true

logging:
  max_file_size_mb: 100
  retention_days: 30
  backup_count: 10
  log_level: INFO
```

See [`config.yaml`](config.yaml) for complete configuration and [`docs/CONFIGURATION.md`](docs/CONFIGURATION.md) for detailed documentation.

## Logging Configuration

The server implements automatic log rotation and retention management.

### Log Rotation Settings

The `config.yaml` file contains the following logging settings:

```yaml
logging:
  # Maximum size of a single log file in megabytes before rotation
  max_file_size_mb: 100

  # Number of days to retain log files
  retention_days: 30

  # Number of backup log files to keep
  backup_count: 10

  # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  # Can be overridden by QG_MCP_SERVER_LOG_LEVEL environment variable
  log_level: INFO

  # Log format
  log_format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

  # Date format for log timestamps
  date_format: "%Y-%m-%d %H:%M:%S"
```

### Log Rotation Behavior

- **Daily Log Files**: The server creates one log file per day using the pattern `qg_server_YYYYMMDD.log` (e.g., `qg_server_20251211.log`). Multiple server restarts on the same day append to the same file.
- **Automatic Rotation**: When a log file reaches the configured size (`max_file_size_mb`), it is automatically rotated
- **Retention Policy**: Log files older than `retention_days` are automatically deleted on server startup
- **Backup Files**: Up to `backup_count` rotated log files are kept (e.g., `qg_server_20251211.log.1`, `qg_server_20251211.log.2`, etc.)
- **Default Values**: If `config.yaml` is not found, the server uses built-in defaults (100 MB, 30 days, 10 backups)

### Customizing Log Configuration

To customize logging behavior, edit the `config.yaml` file in the project root:

```bash
# Edit config.yaml
nano config.yaml

# Restart the server for changes to take effect
./scripts/td-qg-mcp-server.py stop
./scripts/td-qg-mcp-server.py start
```

**Note**: Environment variables (`QG_MCP_SERVER_LOG_LEVEL`) and command-line arguments (`--log-level`) override the `log_level` setting in `config.yaml`.

## Running the Server

### Important: Virtual Environment Requirement

**The server must be run from within the activated virtual environment** to ensure all dependencies (including uvicorn) are available:

```bash
# Activate the virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Then run the server
./scripts/td-qg-mcp-server.py start
```

### Server Management

The server provides three operational modes:

#### 1. Background Mode (Production - Default)

Runs the server as a detached background process with all output redirected to log files:

```bash
# Start server in background
source venv/bin/activate
./scripts/td-qg-mcp-server.py start

# Check server status
./scripts/td-qg-mcp-server.py status

# Stop server
./scripts/td-qg-mcp-server.py stop
```

**Background mode features:**
- Server detaches from terminal immediately
- All logs written to `logs/qg_server_YYYYMMDD.log`
- No console output or Ctrl+C option
- PID file created at `run/server.pid` for process tracking
- Graceful shutdown with process tree cleanup (handles reload mode child processes)
- Survives terminal closure

#### 2. Foreground Mode (Development)

Runs the server in the current terminal for debugging:

```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --foreground --log-level DEBUG
```

**Foreground mode features:**
- Console output for immediate feedback
- Can be stopped with Ctrl+C
- PID file created at `run/server.pid`
- Signal handlers kill entire process tree on shutdown

#### 3. Foreground with Hot Reload (Active Development)

Automatically restarts server when code changes are detected:

```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --foreground --reload --log-level DEBUG
```

**Hot reload features:**
- Watches `src/` directory for changes
- Automatic restart on file modifications
- Spawns child processes for reloading
- Process tree cleanup ensures no orphaned processes

### Starting the Server

**Basic usage:**
```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start
```

**Custom host and port:**
```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --host 127.0.0.1 --port 8080
```

**Custom QueryGrid Manager connection:**
```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --qgm-host your-manager.com --qgm-port 8080 --qgm-username admin --qgm-password secret --qgm-verify-ssl false
```

**Custom logging:**
```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py start --log-dir ./my-logs --log-level DEBUG
```

### Stopping the Server

The stop command handles complex process trees (including reload mode child processes):

```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py stop
```

**Stop behavior:**
1. Reads PID from `run/server.pid`
2. Verifies the process is the correct server instance
3. Finds and terminates all child processes (using `pgrep -P`)
4. Terminates parent process
5. Cleans up PID file
6. Handles stale processes gracefully

**Fallback:** If PID file is missing, searches for running `src.server:app` processes and terminates their process trees.

### Checking Server Status

```bash
source venv/bin/activate
./scripts/td-qg-mcp-server.py status
```

**Status output includes:**
- Process ID (PID)
- Health check results (application and QueryGrid connectivity)
- QueryGrid Manager version (if connected)

### Process Management Features

**Signal Handling:**
- Custom SIGINT (Ctrl+C) and SIGTERM handlers
- Process tree detection with `pgrep -P <pid>`
- Kills all child processes before parent
- Immediate termination with `os._exit(0)`
- PID file cleanup on shutdown

**Multi-Instance Safety:**
- Only kills processes associated with the specific PID file
- Verifies process command contains `src.server:app` before killing
- Won't affect other servers running on the same machine

**Cross-Platform Support:**
- Unix/Linux/macOS: Uses `pgrep` and `kill` commands
- Windows: Uses `taskkill /F /T /PID` for process tree termination

### Available Command Line Options

**Server Configuration:**
- `--host HOST`: Host to bind the server to (default: `0.0.0.0`, or `QG_MCP_SERVER_HOST` env var)
- `--port PORT`: Port to bind the server to (default: `8000`, or `QG_MCP_SERVER_PORT` env var)
- `--foreground`: Run server in foreground mode for development/debugging
- `--reload`: Enable hot reloading (automatically restart on code changes) - requires `--foreground`

**Logging:**
- `--log-dir LOG_DIR`: Directory to write server logs to (default: `./logs`)
- `--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}`: Logging level (default: `INFO`)

**QueryGrid Manager Connection:**
- `--qgm-host QGM_HOST`: QueryGrid Manager host
- `--qgm-port QGM_PORT`: QueryGrid Manager port
- `--qgm-username QGM_USERNAME`: QueryGrid Manager username
- `--qgm-password QGM_PASSWORD`: QueryGrid Manager password
- `--qgm-verify-ssl QGM_VERIFY_SSL`: Verify SSL certificates (accepts: `true`, `1`, `yes` for enabled; `false`, `0`, `no` for disabled)

For complete help:
```bash
./scripts/td-qg-mcp-server.py -h
```

## MCP Client Configuration

To connect an MCP client to this server using the **streamable-http** transport protocol, first start the MCP server, then add the following configuration to your MCP client's configuration file (typically `claude_desktop_config.json` or `mcp.json`):

### JSON Configuration for Streamable-HTTP

```json
{
  "mcpServers": {
    "teradata-querygrid": {
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

### Setup Steps

1. **Start the MCP server**: Run `./scripts/td-qg-mcp-server.py start` with the required environment variables set (see [Environment Variables](#environment-variables) section)
2. **Configure your MCP client**: Add the JSON configuration above to your client's config file
3. **Connect**: The MCP client will connect to the running server via the specified URL

**Note:** The `env` section in the JSON configuration should contain the same environment variables described in the [Environment Variables](#environment-variables) section above.

### Transport Protocol

This configuration uses the **streamable-http** transport protocol for efficient bidirectional communication between the MCP client and server. The FastMCP framework automatically handles the HTTP streaming connection.

### Security Notes

- **Never commit sensitive credentials** to version control. Use environment variables or secure credential management.
- **Use HTTPS** for production QueryGrid Manager connections when possible.
- **Restrict file permissions** on configuration files containing credentials.

## Available Tools

The server provides **70+ tools** organized by QueryGrid resource type. All tools follow consistent patterns and return formatted responses with operation results and metadata.

### Core Management Tools

#### API Information
- `qg_get_api_info()`: Get QueryGrid Manager API version and information

#### Manager Tools
- `qg_get_managers(extra_info, filter_by_name)`: Get all QueryGrid managers
- `qg_get_manager_by_id(id, extra_info)`: Get specific manager details

#### Datacenter Tools
- `qg_get_datacenters()`: Get all datacenters
- `qg_get_datacenter_by_id(id)`: Get specific datacenter
- `qg_create_datacenter(name, description, tags)`: Create new datacenter

### System Management

#### System Tools
- `qg_get_systems(extra_info, filter_by_name)`: Get all systems with filtering
- `qg_get_system_by_id(id, extra_info)`: Get specific system details
- `qg_create_system(name, system_type, platform_type, ...)`: Create new system

#### Node Tools
- `qg_get_nodes(...)`: Get nodes with extensive filtering options
- `qg_get_node_by_id(id, extra_info)`: Get specific node details
- `qg_get_node_heartbeat_by_id(id)`: Get node heartbeat status

#### Node Virtual IP Tools
- `qg_get_node_virtual_ips()`: Get all node virtual IPs
- `qg_get_node_virtual_ip_by_id(id)`: Get specific virtual IP

### Connectivity

#### Connector Tools
- `qg_get_connectors(extra_info, filter_by_name)`: Get all connectors
- `qg_get_connector_by_id(id, extra_info)`: Get specific connector
- `qg_get_connector_active(id)`: Get active connector configuration
- `qg_get_connector_pending(id)`: Get pending configuration
- `qg_get_connector_previous(id)`: Get previous configuration
- `qg_get_connector_drivers(id)`: Get connector driver information
- `qg_create_connector(name, connector_type, ...)`: Create new connector

#### Link Tools
- `qg_get_links(extra_info, filter_by_name)`: Get all links
- `qg_get_link_by_id(id, extra_info)`: Get specific link
- `qg_get_link_active(id)`: Get active link configuration
- `qg_get_link_pending(id)`: Get pending configuration
- `qg_get_link_previous(id)`: Get previous configuration
- `qg_create_link(name, initiator_id, target_id, ...)`: Create new link

#### Fabric Tools
- `qg_get_fabrics(extra_info, filter_by_name)`: Get all fabrics
- `qg_get_fabric_by_id(id, extra_info)`: Get specific fabric
- `qg_get_fabric_active(id)`: Get active fabric configuration
- `qg_get_fabric_pending(id)`: Get pending configuration
- `qg_get_fabric_previous(id)`: Get previous configuration
- `qg_create_fabric(name, datacenter_id, ...)`: Create new fabric

#### Bridge Tools
- `qg_get_bridges(extra_info, filter_by_name)`: Get all bridges
- `qg_get_bridge_by_id(id, extra_info)`: Get specific bridge
- `qg_create_bridge(name, ...)`: Create new bridge

#### Network Tools
- `qg_get_networks(extra_info, filter_by_name)`: Get all networks
- `qg_get_network_by_id(id, extra_info)`: Get specific network
- `qg_get_network_active(id)`: Get active network configuration
- `qg_get_network_pending(id)`: Get pending configuration
- `qg_get_network_previous(id)`: Get previous configuration

### Security & Access

#### User Tools
- `qg_get_users()`: Get all users
- `qg_get_user_by_id(id)`: Get specific user
- `qg_create_user(name, password, ...)`: Create new user

#### User Mapping Tools
- `qg_get_user_mappings(filter_by_name)`: Get all user mappings
- `qg_get_user_mapping_by_id(id)`: Get specific user mapping
- `qg_create_user_mapping(name, ...)`: Create new user mapping

#### Communication Policy Tools
- `qg_get_comm_policies()`: Get all communication policies
- `qg_get_comm_policy_by_id(id, extra_info)`: Get specific policy
- `qg_get_comm_policy_active(id)`: Get active policy configuration
- `qg_get_comm_policy_pending(id)`: Get pending configuration
- `qg_get_comm_policy_previous(id)`: Get previous configuration
- `qg_create_comm_policy(name, ...)`: Create new communication policy

### Operations & Monitoring

#### Query Tools
- `qg_get_queries(...)`: Get queries with filtering by state, system, user
- `qg_get_query_by_id(id)`: Get specific query details
- `qg_cancel_query(id)`: Cancel running query

#### Operation Tools
- `qg_get_operations(...)`: Get operations with filtering
- `qg_get_operation_by_id(id)`: Get specific operation
- `qg_run_operation(operation_id, operation_type, ...)`: Execute operation
- `qg_apply_operation(id)`: Apply pending operation
- `qg_revert_operation(id)`: Revert operation

#### Issue Tools
- `qg_get_issues()`: Get all issues
- `qg_get_issue_by_id(id)`: Get specific issue details

#### Diagnostic Tools
- `qg_run_diagnostic_check(type, ...)`: Run diagnostic check
- `qg_get_diagnostic_check_status(id)`: Get diagnostic check status

### Software & Configuration

#### Software Tools
- `qg_get_software(filter_by_name)`: Get all software packages
- `qg_get_software_by_id(id)`: Get specific software
- `qg_get_software_jdbc_driver()`: Get all JDBC drivers
- `qg_get_software_jdbc_driver_by_name(jdbc_driver_name)`: Get specific JDBC driver

#### Foreign Server Tools
- `qg_get_create_foreign_server_script(...)`: Generate foreign server creation script
- `qg_get_create_foreign_server_template()`: Get foreign server template

#### Utilities
- `qg_get_shared_memory_estimator(...)`: Estimate shared memory requirements

## Testing

The project includes comprehensive unit and integration tests. For detailed information on:
- Running tests (unit, integration, or all)
- Writing new tests
- Test configuration and fixtures
- Troubleshooting test issues

See the [Testing Guide](docs/TESTING.md).

### ⚠️ Important: Test Execution Warning

**Integration tests will CREATE, MODIFY, and DELETE entities** in your configured QueryGrid Manager instance. Before running tests, you will see a confirmation prompt showing:
- The QueryGrid Manager connection details
- Information about test entities that will be created
- Cleanup behavior

**Quick start:**
```bash
# Run all tests (requires confirmation)
pytest -v

# Skip confirmation prompt with --force flag
pytest -v --force

# Run only unit tests (no external dependencies, no confirmation needed)
pytest -v -m unit

# Run only integration tests (requires QueryGrid Manager and confirmation)
pytest -v -m integration
```

**Test Entities:**
Integration tests create various entities (datacenters, systems, connectors, bridges, fabrics, policies, user mappings, etc.) in QueryGrid Manager. Test entities are typically named with prefixes like `test_` or `pytest_` for easy identification.

Tests will attempt to clean up all created entities after execution. However, if tests are interrupted or fail during cleanup, some entities may remain in your QueryGrid Manager.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details on:
- Code style and standards
- Development workflow
- Testing requirements
- Pull request process

**Important**: Please create a GitHub issue before starting work on a pull request.

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions, please use the GitHub issue tracker.