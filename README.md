<h1 align="center">甘い Status</h1>

<div align="center">
     <strong>Service Monitoring API</strong>
</div>

<div align="center">
    A FastAPI-based backend for monitoring and displaying service health status
</div>

<br />

<div align="center">
    <!-- Framework -->
    <a href="https://fastapi.tiangolo.com/">
        <img src="https://img.shields.io/badge/framework-FastAPI-009485.svg?style=for-the-badge"
        alt="Framework" />
    </a>
    <!-- Language -->
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/language-Python-3776ab.svg?style=for-the-badge"
        alt="Language" />
    </a>
    <!-- Python Version -->
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-%3E%3D3.10-blue.svg?style=for-the-badge"
        alt="Python Version" />
    </a>
    <!-- License -->
    <a href="./LICENSE">
        <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge"
        alt="License" />
    </a>
</div>

<div align="center">
    <h3>
        <a href="#features">
        Features
        </a>
        <span> | </span>
        <a href="#quick-start">
        Quick Start
        </a>
        <span> | </span>
        <a href="#contributing">
        Contributing
        </a>
    </h3>
</div>

<div align="center">
    <h4>
        <a href="https://github.com/Rystal-Team/amai-status-frontend">
            Frontend Repository
        </a>
    </h4>
</div>

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Development](#development)
- [Contributing](#contributing)

## Features

- **Service Monitoring:** Periodically checks configured service endpoints and records their status
- **Uptime Statistics:** Computes and stores uptime percentages and downtime metrics for monitored services
- **SQLite Database:** Stores all monitoring data with automatic schema migrations on startup
- **YAML Configuration:** Configuration stored in human-readable YAML format with server binding options
- **CORS Enabled:** API configured to accept cross-origin requests from different domains
- **Heartbeat History:** Maintains historical records of service status checks over configurable time ranges

## Quick Start

### Prerequisites

- Python >= 3.10
- pip or poetry for package management

### Installation

```bash
# Navigate to backend directory
cd amai-status

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Development with hot reload
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8182

# Production
python -m uvicorn main:app --host 0.0.0.0 --port 8182 --workers 4
```

The API will be available at `http://localhost:8182`

API documentation available at `http://localhost:8182/docs` (Swagger UI)

## Configuration

### config.yaml

The application is configured via `config.yaml`:

```yaml
server:
  host: 0.0.0.0
  port: 8182

site:
  title: "Service Status"
  subtitle: "Real-time monitoring dashboard"
  accent_color: "#6366f1"

monitors:
  - name: "API Server"
    url: "https://api.example.com/health"
    interval: 60

  - name: "Database"
    url: "https://db.example.com/health"
    interval: 30

cache:
  duration: 604800 # 7 days in seconds
```

### Configuration Options

- **site.title:** Page title shown in browser
- **site.subtitle:** Subtitle/description
- **site.accent_color:** Primary accent color (RGB format)
- **monitors:** List of services to monitor
- **monitors[].name:** Display name for service
- **monitors[].url:** Health check endpoint
- **monitors[].interval:** Check interval in seconds

## Development

### Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

### Installing Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Add new dependency
pip install package_name
pip freeze > requirements.txt
```

### Running in Development

```bash
# With auto-reload
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8182

# With debug logging
python -m uvicorn main:app --reload --log-level debug
```

### Testing

```bash
# Test API endpoints with curl
curl http://localhost:8182/api/config

curl http://localhost:8182/api/status

curl http://localhost:8182/health
```

### Interactive API Documentation

Visit `http://localhost:8182/docs` for Swagger UI or `http://localhost:8182/redoc` for ReDoc.

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

### Local Development Setup

```bash
# Clone the repository
git clone <repository-url>

# Setup virtual environment
cd amai-status
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload
```

## License

MIT - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
