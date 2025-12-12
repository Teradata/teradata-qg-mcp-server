# Configuration Management Guide

This document provides a comprehensive guide on how configuration is managed in the Teradata QueryGrid MCP Server, including the separation of concerns between `config.yaml`, `.env` files, and command-line arguments.

## Configuration Architecture

The server uses a **three-tier configuration hierarchy** with clear separation of concerns:

```
Priority: Command-Line Arguments > Environment Variables > config.yaml Defaults
```

### Decision Matrix

| Parameter Type | config.yaml | .env File | CLI Args | Rationale |
|----------------|-------------|-----------|----------|-----------|
| **Sensitive Credentials** | ❌ No | ✅ Yes | ✅ Yes (override) | Never commit secrets to version control |
| **Environment-Specific** | ❌ No | ✅ Yes | ✅ Yes (override) | Varies per deployment/environment |
| **Application Defaults** | ✅ Yes | ❌ No | ❌ No | Common defaults for all deployments |
| **Operational Settings** | ✅ Yes | ✅ Yes (override) | ✅ Yes (override) | May need runtime adjustment |
| **Runtime Flags** | ❌ No | ❌ No | ✅ Yes | Control execution behavior |

## Configuration Sources

### 1. config.yaml - Application Defaults

**Purpose**: Define sensible defaults that work across all environments

**Should Include**:
- ✅ Server defaults (host, port, timeouts)
- ✅ Logging configuration (rotation, retention, levels)
- ✅ QueryGrid behavior settings (timeouts, SSL verification defaults)
- ✅ Feature flags and limits

**Should NOT Include**:
- ❌ Credentials (usernames, passwords, API keys)
- ❌ Environment-specific hosts/ports
- ❌ Secrets or sensitive data

**Current Structure**:
```yaml
server:
  host: "0.0.0.0"              # Safe default - bind to all interfaces
  port: 8000                   # Standard development port
  health_check_timeout: 5      # Reasonable timeout for health checks

querygrid:
  request_timeout: 10          # Safe API timeout
  verify_ssl: true             # Secure by default

logging:
  max_file_size_mb: 100        # Reasonable rotation size
  retention_days: 30           # One month retention
  backup_count: 10             # Keep 10 backup files
  log_level: INFO              # Appropriate verbosity
  log_format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  date_format: "%Y-%m-%d %H:%M:%S"
```

### 2. .env File - Environment-Specific Configuration

**Purpose**: Store environment-specific and sensitive configuration

**Should Include**:
- ✅ QueryGrid Manager credentials (required)
- ✅ QueryGrid Manager connection details
- ✅ Environment-specific overrides
- ✅ SSL verification preferences per environment

**Should NOT Include**:
- ❌ Application logic defaults
- ❌ Logging format strings
- ❌ Business logic configuration

**Required Variables**:
```bash
# QueryGrid Manager Connection (REQUIRED)
QG_MANAGER_HOST=querygrid-manager.example.com
QG_MANAGER_PORT=9980
QG_MANAGER_USERNAME=admin
QG_MANAGER_PASSWORD=your_secure_password

# QueryGrid Manager SSL Verification (OPTIONAL)
# Override config.yaml default if needed for specific environment
QG_MANAGER_VERIFY_SSL=true
```

**Optional Override Variables**:
```bash
# Server Configuration Overrides
QG_MCP_SERVER_HOST=127.0.0.1    # Override for specific environment
QG_MCP_SERVER_PORT=8080         # Override for specific environment

# Logging Overrides
QG_MCP_SERVER_LOG_LEVEL=DEBUG   # Override for debugging
QG_MCP_SERVER_LOG_FILE=./logs/qg_server_20251211.log  # Override log path
```

### 3. Command-Line Arguments - Runtime Control

**Purpose**: Provide runtime flexibility and operational control

**Should Include**:
- ✅ Runtime behavior flags (--foreground, --reload)
- ✅ Temporary overrides (--log-level DEBUG for troubleshooting)
- ✅ Operational parameters (--log-dir for specific run)
- ✅ Emergency credential overrides
- ✅ Development/testing convenience options

**Available Arguments**:
```bash
# Server Control
--host TEXT                    # Override server host
--port INTEGER                 # Override server port
--foreground                   # Run in foreground (not daemon)
--reload                       # Enable hot reload (development)

# Logging
--log-dir PATH                 # Directory for log files (required)
--log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]  # Override log level

# QueryGrid Connection Overrides (for emergency or testing)
--qgm-host TEXT                # Override QueryGrid host
--qgm-port INTEGER             # Override QueryGrid port
--qgm-username TEXT            # Override QueryGrid username
--qgm-password TEXT            # Override QueryGrid password
--qgm-verify-ssl / --no-qgm-verify-ssl  # Override SSL verification

# Management Commands
start                          # Start server
stop                           # Stop server
status                         # Check server status
```

## Configuration Flow

### Startup Sequence

1. **Load config.yaml defaults**
   - Application reads default values from `config.yaml`
   - These serve as fallbacks if no other source provides values

2. **Load .env file (if present)**
   - `python-dotenv` loads environment variables from `.env`
   - These override config.yaml defaults

3. **Read environment variables**
   - System environment variables override .env values
   - Useful for containerized deployments

4. **Parse command-line arguments**
   - CLI arguments have highest priority
   - Override all previous sources

### Example Resolution

Given:
- config.yaml: `server.port: 8000`
- .env file: `QG_MCP_SERVER_PORT=8080`
- CLI: `--port 9000`

Result: **Server binds to port 9000** (CLI wins)

## Parameter Classification

### 🔒 Sensitive (Must be in .env, never in config.yaml)

| Parameter | Environment Variable | CLI Override | Description |
|-----------|---------------------|--------------|-------------|
| QG Manager Host | `QG_MANAGER_HOST` | `--qgm-host` | QueryGrid Manager hostname |
| QG Manager Port | `QG_MANAGER_PORT` | `--qgm-port` | QueryGrid Manager port |
| QG Manager Username | `QG_MANAGER_USERNAME` | `--qgm-username` | Authentication username |
| QG Manager Password | `QG_MANAGER_PASSWORD` | `--qgm-password` | Authentication password |

**Rationale**: These are credentials and environment-specific connection details that vary between dev/test/prod and should never be committed to version control.

### ⚙️ Operational (config.yaml defaults, .env/CLI override)

| Parameter | config.yaml | Environment Variable | CLI Override | Description |
|-----------|-------------|---------------------|--------------|-------------|
| Server Host | `server.host` | `QG_MCP_SERVER_HOST` | `--host` | MCP server bind address |
| Server Port | `server.port` | `QG_MCP_SERVER_PORT` | `--port` | MCP server bind port |
| Log Level | `logging.log_level` | `QG_MCP_SERVER_LOG_LEVEL` | `--log-level` | Logging verbosity |
| SSL Verification | `querygrid.verify_ssl` | `QG_MANAGER_VERIFY_SSL` | `--qgm-verify-ssl` | SSL certificate verification |

**Rationale**: These have sensible defaults in config.yaml but may need adjustment per environment (dev uses different ports) or at runtime (debugging requires DEBUG level).

### 📋 Application Defaults (config.yaml only)

| Parameter | config.yaml | Override? | Description |
|-----------|-------------|-----------|-------------|
| Health Check Timeout | `server.health_check_timeout` | No | Timeout for /health endpoint |
| Request Timeout | `querygrid.request_timeout` | No | API request timeout |
| Max Log File Size | `logging.max_file_size_mb` | No | Log rotation threshold |
| Log Retention Days | `logging.retention_days` | No | Log cleanup threshold |
| Backup Count | `logging.backup_count` | No | Number of backup log files |
| Log Format | `logging.log_format` | No | Log message format string |
| Date Format | `logging.date_format` | No | Timestamp format string |

**Rationale**: These are application constants that rarely change and don't need per-environment or runtime adjustment. They're in config.yaml for visibility and easy tuning if needed, but aren't exposed via .env or CLI.

### 🚀 Runtime Only (CLI only)

| Parameter | CLI Argument | Description |
|-----------|--------------|-------------|
| Foreground Mode | `--foreground` | Run server in foreground vs daemon |
| Hot Reload | `--reload` | Enable file watching and auto-reload |
| Log Directory | `--log-dir` | Directory for log file output |
| Command | `start\|stop\|status` | Server management action |

**Rationale**: These control how the server runs, not what configuration it uses. They're runtime decisions, not configuration.

## Best Practices

### For Developers

1. **Never commit .env files** - Add to `.gitignore`
2. **Provide .env.example** - Template for required variables
3. **Use config.yaml for defaults** - Safe, non-sensitive values only
4. **Document all parameters** - Include rationale in config.yaml comments
5. **Test with minimal .env** - Ensure defaults work

### For Operations

1. **Use .env for deployments** - One file per environment (dev.env, prod.env)
2. **Use environment variables in containers** - Don't mount .env in production
3. **Use CLI for troubleshooting** - Temporary overrides without changing files
4. **Rotate credentials regularly** - Update .env files, not config.yaml
5. **Monitor configuration drift** - Ensure environments stay in sync

### For Security

1. **Credentials only in .env** - Never in config.yaml or command history
2. **Use secret management** - Consider Vault, AWS Secrets Manager, etc.
3. **Restrict .env file permissions** - `chmod 600 .env` on Unix systems
4. **Audit configuration access** - Track who modifies .env files
5. **Validate at startup** - Fail fast if required credentials are missing

## Examples

### Development Setup

```bash
# config.yaml (committed)
server:
  host: "0.0.0.0"
  port: 8000

# .env (not committed)
QG_MANAGER_HOST=localhost
QG_MANAGER_PORT=9980
QG_MANAGER_USERNAME=dev_user
QG_MANAGER_PASSWORD=dev_pass
QG_MCP_SERVER_LOG_LEVEL=DEBUG

# Run with hot reload
python scripts/td-qg-mcp-server.py start --foreground --reload --log-dir ./logs
```

### Production Setup

```bash
# config.yaml (committed, same as dev)
server:
  host: "0.0.0.0"
  port: 8000

# prod.env (not committed, deployed securely)
QG_MANAGER_HOST=querygrid-prod.company.com
QG_MANAGER_PORT=9980
QG_MANAGER_USERNAME=prod_service_account
QG_MANAGER_PASSWORD=secure_prod_password
QG_MCP_SERVER_LOG_LEVEL=INFO

# Run as daemon
source prod.env
python scripts/td-qg-mcp-server.py start --log-dir /var/log/qg-mcp-server
```

### Temporary Debugging

```bash
# Don't modify .env or config.yaml
# Use CLI overrides for temporary changes
python scripts/td-qg-mcp-server.py start \
  --foreground \
  --log-level DEBUG \
  --log-dir ./debug-logs \
  --port 8888
```

## Migration Guide

### ✅ Migration Complete

All hardcoded values have been successfully migrated to config.yaml:

| File | Previous | Current Status |
|------|----------|----------------|
| `src/qgm/base.py` | `self._timeout = 10` | ✅ Now accepts timeout parameter from config |
| `scripts/td-qg-mcp-server.py` | `timeout=5` | ✅ Loads from `config.yaml:server.health_check_timeout` |
| `src/server.py` | `host="0.0.0.0", port=8000` | ✅ Reads from config with env var overrides |
| `src/qgm/querygrid_manager.py` | Used env vars only | ✅ Now loads defaults from config.yaml |

### Implementation Details

1. **✅ Config loader utility created**
   ```python
   def load_config() -> dict[str, Any]:
       """Load complete configuration from config.yaml with defaults"""
       # Returns merged config with defaults for missing values
   ```
   - Located in `src/utils.py`
   - Loads all sections: server, querygrid, logging
   - Merges with defaults to ensure all keys exist
   - Handles missing config.yaml gracefully

2. **✅ Modules updated to use config**
   - `BaseClient.__init__()` accepts optional `timeout` parameter
   - `QueryGridManager.__init__()` loads config and passes timeout to all clients
   - Health check in CLI reads timeout from config.yaml
   - `server.py` reads host/port from config with env var fallback
   - All 21+ resource clients receive configured timeout

3. **✅ Configuration hierarchy implemented**
   - Command-line arguments override environment variables
   - Environment variables override config.yaml
   - config.yaml provides sensible defaults
   - Falls back to hardcoded defaults if config.yaml missing

### Verification

Run the integration test to verify configuration is working:

```bash
python test_config_integration.py
```

Expected output:
```
✅ All configuration values loaded correctly from config.yaml
✅ Environment variables correctly override config.yaml values
✅ BaseClient correctly accepts and uses timeout parameter
✅ Configuration hierarchy working as expected
```

### Future Enhancements

1. **Configuration validation** (optional improvement)
   - Add schema validation using pydantic or similar
   - Validate required .env variables at startup
   - Provide helpful error messages for missing/invalid config

2. **Configuration documentation** (optional improvement)
   - Auto-generate configuration reference from config.yaml comments
   - Add configuration examples for common deployment scenarios

3. **Configuration hot-reload** (optional improvement)
   - Watch config.yaml for changes
   - Reload configuration without restarting server
   - Useful for runtime adjustments in production

## Summary

| Configuration Type | Storage Location | Override Method | Use Case |
|-------------------|------------------|-----------------|----------|
| **Sensitive Credentials** | `.env` file | Environment variables, CLI | Secrets, per-environment |
| **Environment-Specific** | `.env` file | Environment variables, CLI | Hosts, ports, per-env settings |
| **Application Defaults** | `config.yaml` | .env, environment vars, CLI | Safe defaults for all envs |
| **Runtime Behavior** | CLI only | N/A | Development, debugging, ops |

This separation ensures:
- ✅ Secrets never committed to version control
- ✅ Easy environment-specific configuration
- ✅ Clear, documented defaults
- ✅ Flexible runtime control
- ✅ Security best practices
