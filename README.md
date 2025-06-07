# 🐝 BeeKeeper Project - Advanced Beekeeping Data Platform

<div align="center">

<img src="./media/imgs/project_img.jpeg" alt="BeeKeeper Project" width="200" height="200">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./docs/changelogs/1.0.0.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](./utils/docker-compose.yaml)
[![API](https://img.shields.io/badge/API-FastAPI-009688.svg)](./src/api/)

*A comprehensive data engineering platform for modern beekeeping operations*

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-documentation) • [🏗️ Architecture](#-architecture) • [🛠️ Development](#-development)

</div>

---

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#-architecture)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🔧 Configuration](#-configuration)
- [🛠️ Development](#-development)
- [📊 Monitoring & Observability](#-monitoring--observability)
- [🔐 Security](#-security)
- [📚 API Documentation](#-api-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Project Overview

**BeeKeeper** is a professional-grade data engineering platform designed to revolutionize beekeeping operations through intelligent data analysis and decision support. Originally developed as an MVP for INRAE "Institut de l'abeille" and now serving over **5,000 beekeepers** worldwide through the [BeeGIS application](https://appli.itsap.asso.fr/app/01-beegis).

### 🌟 Mission Statement

In the context of declining honey yields and climate change, BeeKeeper empowers beekeepers with data-driven insights to:
- **Optimize hive placement** through cartographic analysis
- **Predict production cycles** using weather correlation models
- **Monitor hive health** with automated sensor integration
- **Make informed decisions** with ML-powered recommendations

### 🎯 Target Audience

- **Professional beekeepers** managing transhumant operations
- **Agricultural researchers** studying pollinator behavior
- **Data scientists** working with environmental datasets
- **Apiculture consultants** providing advisory services

---

## ✨ Key Features

### 🗺️ Cartographic Intelligence
- **Multi-layer mapping** with agricultural parcels, forests, and hydrography
- **Foraging area analysis** with customizable radius (500m - 3km)
- **Melliferous crop identification** from 360+ categories simplified to 70 relevant types
- **Comparative visualization** of multiple apiary locations

### 🌤️ Weather Integration
- **Real-time meteorological data** from OpenMeteo API
- **Historical weather analysis** for seasonal planning
- **Nectar flow prediction** based on weather patterns
- **Climate correlation models** with hive weight data

### 🤖 Machine Learning Pipeline
- **Automated data processing** with Apache Airflow
- **Weight gain prediction** using environmental variables
- **Decision support indices** for optimal hive management
- **MLflow experiment tracking** for model versioning

### 📊 Comprehensive Monitoring
- **Prometheus metrics collection**
- **Grafana dashboards** for operational insights
- **Distributed tracing** with OpenTelemetry
- **Alert management** with custom notifications

### 🔐 Enterprise Security
- **JWT-based authentication** with Argon2 password hashing
- **GDPR-compliant** user data handling
- **Role-based access control**
- **API rate limiting** and request throttling

---

## 🏗️ Architecture

<div align="center">
<img src="./media/imgs/architecture_schema.svg" alt="System Architecture" width="800">
</div>

### 🎯 Core Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **API Gateway** | FastAPI + Uvicorn | RESTful API with OpenAPI documentation |
| **Web Application** | BeeGIS UI | User interface for beekeepers |
| **Data Pipeline** | Apache Airflow | ETL processes and workflow orchestration |
| **ML Platform** | MLflow | Model training, versioning, and deployment |
| **Databases** | PostgreSQL + PostGIS, MongoDB | Geospatial and user data storage |
| **Cache Layer** | Redis Stack | Session management and query caching |
| **Monitoring** | Prometheus + Grafana | Metrics collection and visualization |
| **Logging** | Loki + Promtail | Centralized log aggregation |

### 🌐 Network Architecture

```
🌍 Internet
    ↓
🔒 Load Balancer (Public Network)
    ↓
🖥️ BeeGIS UI ← → 🚀 FastAPI Gateway
    ↓                    ↓
📊 Monitoring Stack   🔒 Private Network
    ↓                    ↓
🎯 Data Pipeline  ← → 🗄️ Database Cluster
```

---

## 🚀 Quick Start

Get BeeKeeper running in under 5 minutes:

### Prerequisites

- **Docker** 20.10+ & **Docker Compose** 2.0+
- **Linux/Unix** environment (tested on Ubuntu 20.04+)
- **8GB RAM** minimum (16GB recommended)
- **20GB** free disk space

### 1️⃣ Clone & Initialize

```bash
# Clone the repository
git clone https://github.com/your-org/beekeeper-project.git
cd beekeeper-project

# Initialize default configurations
./utils/init_services.sh
```

### 2️⃣ Configure Services

```bash
# Review and customize configurations
nano utils/common.env
nano src/api/.env

# Update default passwords (IMPORTANT!)
nano utils/secrets/postgres_password
nano utils/secrets/mongodb_password
```

### 3️⃣ Launch Platform

```bash
# Start all services
./utils/start_containers.sh

# Select deployment profile when prompted:
# [1] Full stack (recommended for production)
# [2] API only (development)
# [3] Database only (testing)
```

### 4️⃣ Access Applications

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| **BeeGIS UI** | http://localhost:3000 | - |
| **API Documentation** | http://localhost:8000/docs | - |
| **Airflow** | http://localhost:8080 | admin/admin |
| **MLflow** | http://localhost:8002 | - |
| **Grafana** | http://localhost:3001 | admin/admin |

---

## 📦 Installation

### 🐳 Docker Deployment (Recommended)

The platform uses a sophisticated multi-service Docker architecture:

```bash
# Full installation with monitoring
./utils/start_containers.sh
# Select: [1] Full stack

# Services will start in dependency order:
# 1. Databases (PostgreSQL, MongoDB, Redis)
# 2. Core services (API, Airflow, MLflow)  
# 3. Monitoring stack (Prometheus, Grafana)
# 4. Web interface (BeeGIS UI)
```

### 🔧 Development Setup

```bash
# Install Python dependencies for local development
cd src/api
pip install -r requirements.txt

cd ../airflow
pip install -r requirements.txt

# Start only databases for local development
./utils/start_containers.sh
# Select: [3] Database only
```

### 📊 Service Profiles

Control which services to deploy:

```bash
# API + Databases only
docker-compose --profile api up -d

# Full Airflow ETL pipeline
docker-compose --profile airflow up -d

# Complete monitoring stack
docker-compose --profile monitoring up -d
```

---

## 🔧 Configuration

### 🌐 Environment Variables

The platform uses centralized configuration management:

#### Core Settings (`utils/common.env`)
```env
# Project Configuration
PROJECT_VERSION=1.0.0
ENVIRONMENT=production  # development, staging, production
GITLAB_REGISTRY_URL=registry.gitlab.com/your-project

# Data Directories
RAW_DATA_DIRECTORY=./data/raw
PROCESSED_DATA_DIRECTORY=./data/cleaned
LOGS_DIRECTORY=./logs

# Service Discovery
API_HOST=beem-api
API_PORT=8000
POSTGRES_HOST=postgres_beem
MONGODB_HOST=mongodb_beem
REDIS_HOST=beem-redis
```

#### API Configuration (`src/api/.env`)
```env
# Security
DEBUG=False  # Set to False in production!
JWT_SECRET_KEY=your-secret-key
HASH_ALGORITHM=argon2
ACCESS_TOKEN_EXPIRATION_IN_MINUTES=60

# Rate Limiting
LIMITER_TYPE=user  # user or ip
DEFAULT_LIMITS_FOR_LIMITER=60/minute
WEATHER_LIMIT=15/minute
CARTO_LIMIT=60/minute

# Database Connections
POSTGRES_HOST=postgres_beem
POSTGRES_PORT=5432
POSTGRES_API_USER=api_user
CARTO_DATABASE=dbcarto
USER_DATABASE=users

MONGODB_HOST=mongodb_beem
MONGODB_PORT=27017
MONGODB_DATABASE=data_user_beegis
```

### 🔐 Security Configuration

Critical security settings to review:

```bash
# Change default passwords
echo "your-secure-postgres-password" > utils/secrets/postgres_password
echo "your-secure-mongodb-password" > utils/secrets/mongodb_password
echo "your-jwt-secret-key" > utils/secrets/JWT_secret_key

# Set proper file permissions
chmod 600 utils/secrets/*
```

### 📊 Monitoring Configuration

Customize monitoring and alerting:

```bash
# Prometheus configuration
src/prometheus/conf/prometheus.yml

# Grafana dashboards
src/grafana/conf/dashboards/

# Alert rules
src/alertmanager/conf/alerts.yml
```

---

## 🛠️ Development

### 🏗️ Project Structure

```
beekeeper-project/
├── 📁 src/                     # Source code
│   ├── 🚀 api/                 # FastAPI application
│   │   ├── code/
│   │   │   ├── main.py         # API entry point
│   │   │   ├── routers/        # API endpoints
│   │   │   ├── models/         # Pydantic models
│   │   │   ├── services/       # Business logic
│   │   │   └── utils/          # Utilities
│   │   └── requirements.txt
│   ├── 🌊 airflow/             # Data pipeline
│   │   ├── dags/               # Workflow definitions
│   │   ├── plugins/            # Custom operators
│   │   └── requirements.txt
│   ├── 🤖 mlflow/              # ML platform
│   ├── 🗄️ postgres/            # Database schemas
│   ├── 📊 mongodb/             # NoSQL collections
│   └── 📈 monitoring/          # Observability stack
├── 📁 utils/                   # Deployment utilities
│   ├── docker-compose.yaml    # Service orchestration
│   ├── init_services.sh       # Environment setup
│   ├── start_containers.sh    # Service launcher
│   └── script_functions/       # Utility functions
├── 📁 docs/                    # Documentation
└── 📁 data/                    # Data storage
    ├── raw/                    # Incoming data
    ├── processed/              # ETL outputs
    └── archives/               # Data retention
```

### 🔧 API Development

The FastAPI application follows a modular architecture:

```python
# Example: Adding a new endpoint
# src/api/code/routers/my_router.py

from fastapi import APIRouter, Depends
from models.my_models import MyModel
from services.my_service import MyService
from utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/my-endpoint", tags=["my-feature"])

@router.get("/", response_model=MyModel)
async def get_data(
    current_user: dict = Depends(get_current_user),
    service: MyService = Depends()
):
    return await service.get_data()
```

### 🌊 Airflow DAGs

Data pipeline development:

```python
# Example: Weather data processing DAG
# src/airflow/dags/weather_processing.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'beekeeper',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'weather_data_processing',
    default_args=default_args,
    description='Process weather data for ML models',
    schedule_interval='@hourly',
    catchup=False
)

def extract_weather_data(**context):
    # Implementation here
    pass

extract_task = PythonOperator(
    task_id='extract_weather',
    python_callable=extract_weather_data,
    dag=dag
)
```

### 🧪 Testing

```bash
# API tests
cd src/api/code
python -m pytest unit_tests/

# Run with coverage
pytest --cov=. --cov-report=html unit_tests/

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## 📊 Monitoring & Observability

### 📈 Metrics Collection

The platform includes comprehensive monitoring:

- **System Metrics**: CPU, memory, disk usage
- **Application Metrics**: Request rates, response times, error rates
- **Business Metrics**: User registrations, API usage, data processing volumes
- **Database Metrics**: Query performance, connection pools, storage usage

### 🎯 Key Performance Indicators

Monitor these critical metrics:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API Response Time | < 200ms | > 500ms |
| Database Connections | < 80% pool | > 90% pool |
| ETL Pipeline Success | > 95% | < 90% |
| Memory Usage | < 70% | > 85% |
| Disk Space | < 80% | > 90% |

### 📊 Grafana Dashboards

Pre-configured dashboards available:

- **System Overview**: Infrastructure health
- **API Performance**: Endpoint metrics and user activity
- **Data Pipeline**: Airflow task execution and data quality
- **ML Models**: Training metrics and prediction accuracy
- **Business Intelligence**: User engagement and feature adoption

### 🚨 Alerting

Configure alerts for critical events:

```yaml
# Example: API availability alert
groups:
- name: api_alerts
  rules:
  - alert: APIDown
    expr: up{job="beem-api"} == 0
    for: 30s
    labels:
      severity: critical
    annotations:
      summary: "API service is down"
      description: "The BeeKeeper API has been down for more than 30 seconds"
```

---

## 🔐 Security

### 🛡️ Authentication & Authorization

- **JWT Tokens**: Stateless authentication with configurable expiration
- **Password Security**: Argon2 hashing with salt
- **Session Management**: Redis-backed session storage
- **API Keys**: Service-to-service authentication

### 🔒 Data Protection

- **GDPR Compliance**: User data rights and retention policies
- **Data Encryption**: At-rest and in-transit encryption
- **Access Logging**: Audit trails for all data access
- **Personal Data**: Anonymization and pseudonymization

### 🚫 Security Headers

The API implements security best practices:

```python
# Automatic security headers
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security: max-age=31536000
```

### 🔍 Vulnerability Management

```bash
# Dependency scanning
pip-audit -r requirements.txt

# Container security scanning
docker scout cves beem-api:latest

# Static code analysis
bandit -r src/api/code/
```

---

## 📚 API Documentation

### 🎯 Interactive Documentation

Access comprehensive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### 🔑 Authentication

```bash
# Register a new user
curl -X POST "http://localhost:8000/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "beekeeper", "password": "secure123"}'

# Login and get token
curl -X POST "http://localhost:8000/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "beekeeper", "password": "secure123"}'

# Use token for authenticated requests
curl -X GET "http://localhost:8000/v1/users/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 🗺️ Core Endpoints

#### Cartographic Data
```bash
# Get cartographic data for a location
GET /v1/cartographic/data?lat=45.764043&lon=4.835659&radius=2000&data_types=rpg,forest_v2

# Response includes land use categories and melliferous potential
```

#### Weather Integration
```bash
# Get weather data for coordinates
GET /v1/weather/current?lat=45.764043&lon=4.835659

# Get historical weather for date range
GET /v1/weather/historical?lat=45.764043&lon=4.835659&start_date=2024-01-01&end_date=2024-01-31
```

#### User Management
```bash
# Get user locations (apiaries)
GET /v1/users/locations

# Add new apiary location
POST /v1/users/locations
{
  "name": "Mountain Apiary",
  "latitude": 45.764043,
  "longitude": 4.835659,
  "description": "High altitude lavender location"
}
```

---

## 🤝 Contributing

We welcome contributions from the beekeeping and data science communities!

### 🚀 Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** thoroughly
6. **Submit** a pull request

### 📋 Development Guidelines

- **Code Style**: Follow PEP 8 for Python, use Black formatter
- **Testing**: Maintain >80% test coverage
- **Documentation**: Update docs for any API changes
- **Commits**: Use conventional commit messages

### 🐛 Reporting Issues

Use our issue templates for:
- 🐛 Bug reports
- ✨ Feature requests  
- 📚 Documentation improvements
- 🔒 Security vulnerabilities

### 👥 Community

- **Discord**: Join our developer community
- **Forums**: Participate in technical discussions
- **Conferences**: Present at beekeeping and data conferences

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🏛️ Acknowledgments

- **INRAE "Institut de l'abeille"** - Original project sponsor
- **ITSAP - Institut de l'Abeille** - Production deployment and user feedback
- **DataScientest Bootcamp** - Educational framework and mentorship
- **Open Source Community** - Libraries and tools that make this possible

---

## 👨‍💻 Authors & Contributors

<div align="center">

| Author | Role | Contact |
|--------|------|---------|
| **Alexandre Dangléant** | Data Engineer | Client coordinator | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alexandre-dangl%C3%A9ant-062014148/) |
| **Julien Landouar** | Data Engineer | DevOps | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/julien-landouar/) [![GitHub](https://img.shields.io/badge/GitHub-222222?style=flat&logo=github&logoColor=white)](https://github.com/dixse-pt) |
| **Guillaume Pot** | Data Engineer | Project Manager | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/062guillaumepot/) [![GitHub](https://img.shields.io/badge/GitHub-222222?style=flat&logo=github&logoColor=white)](https://github.com/guillaumepot) |

</div>

---

<div align="center">

**Made with 🐝 for beekeepers worldwide**

*Supporting sustainable apiculture through data-driven innovation*

[⬆️ Back to Top](#-beekeeper-project---advanced-beekeeping-data-platform)

</div>

