# AegisCI Inventory Management REST API (`aegisci-python-inventoryss`)

[![CI Pipeline](https://github.com/aegisci/aegisci-python-inventory/actions/workflows/ci.yml/badge.svg)](https://github.com/aegisci/aegisci-python-inventory/actions)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![FastAPI Version](https://img.shields.io/badge/FastAPI-0.110%2B-009688)
![SQLAlchemy Version](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![License](https://img.shields.io/badge/license-MIT-green)

A production-ready, clean-architecture backend application for inventory management built with **Python 3.10+**, **FastAPI**, **SQLAlchemy 2.0 Async**, **Pydantic v2**, **Docker**, and **GitHub Actions**.

---

## 🏗️ Architecture & Project Structure

The project strictly follows **Clean Architecture** principles, segregating data models, repository access layers, business logic services, and API presentation handlers.

```text
aegisci-python-inventory/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI matrix workflow
├── src/
│   └── aegisci_inventory/
│       ├── api/                 # FastAPI routers & endpoints (v1)
│       │   ├── v1/
│       │   │   ├── categories.py # Category management endpoints
│       │   │   ├── health.py     # System health and readiness probes
│       │   │   ├── items.py      # Inventory item management endpoints
│       │   │   └── movements.py  # Stock movement (IN, OUT, ADJUST) endpoints
│       │   └── router.py        # Main API version routing
│       ├── models/              # SQLAlchemy 2.0 ORM Entities
│       ├── repositories/        # Async Repository Layer (CRUD & Queries)
│       ├── schemas/             # Pydantic v2 Validation Schemas
│       ├── services/            # Business Logic & Validation Services
│       ├── config.py            # Pydantic Settings configuration
│       ├── database.py          # Async Engine and Session management
│       ├── logging_config.py    # Structured logging configuration
│       └── main.py              # Application entry point & factory
├── tests/                       # Comprehensive Pytest Integration/Unit Test Suite
│   ├── conftest.py              # In-memory Async database test setup
│   ├── test_categories.py
│   ├── test_health.py
│   ├── test_items.py
│   └── test_movements.py
├── Dockerfile                   # Multi-stage production container build
├── docker-compose.yml           # Local multi-container compose configuration
├── pyproject.toml               # Project dependencies and tool configurations
└── .env.example                 # Sample configuration environment variables
```

---

## ⚡ Quick Start & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Virtual Environment Setup

```bash
# Clone repository
git clone https://github.com/aegisci/aegisci-python-inventory.git
cd aegisci-python-inventory

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Linux/macOS)
source .venv/bin/activate
# Activate virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install package in editable mode with development tools
pip install -e ".[dev]"
```

---

## 🚀 Running the Application

### Local Development Server

```bash
# Start API with auto-reload
uvicorn aegisci_inventory.main:app --reload --host 0.0.0.0 --port 8000
```

Once running, interactive API documentation is accessible at:
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 🧪 Testing & Code Quality Checks

This repository maintains strict quality control via automated linting, static type analysis, and comprehensive tests.

```bash
# Run pytest with code coverage
pytest

# Run Ruff linter checks
ruff check src tests

# Run Ruff code formatting check
ruff format --check src tests

# Run Mypy static type checker
mypy src
```

---

## 🐳 Docker Deployment

### Build and Run using Docker

```bash
# Build multi-stage image
docker build -t aegisci-inventory-api:latest .

# Run container
docker run -p 8000:8000 aegisci-inventory-api:latest
```

### Run using Docker Compose

```bash
docker-compose up --build -d
```

---

## 📋 API Reference Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Application health probe |
| `GET` | `/api/v1/ready` | Database readiness probe |
| `POST` | `/api/v1/categories` | Create new category |
| `GET` | `/api/v1/categories` | List all categories |
| `GET` | `/api/v1/categories/{id}` | Get category by ID |
| `PUT` | `/api/v1/categories/{id}` | Update category |
| `DELETE` | `/api/v1/categories/{id}` | Delete category |
| `POST` | `/api/v1/items` | Create new inventory item |
| `GET` | `/api/v1/items` | List items (supports category & low stock filters) |
| `GET` | `/api/v1/items/{id}` | Get item details (includes low-stock calculation) |
| `PUT` | `/api/v1/items/{id}` | Update item details |
| `DELETE` | `/api/v1/items/{id}` | Delete item |
| `POST` | `/api/v1/movements` | Record stock movement (`IN`, `OUT`, `ADJUSTMENT`) |
| `GET` | `/api/v1/movements/item/{id}` | View transaction log history for item |

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` to customize settings:

```env
APP_NAME=AegisCI Inventory API
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite+aiosqlite:///./inventory.db
```

---

## 📄 License

This project is open-source software licensed under the [MIT License](LICENSE).
