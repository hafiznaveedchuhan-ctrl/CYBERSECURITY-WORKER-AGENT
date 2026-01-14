#!/usr/bin/env python3
"""
Scaffold a new FastAPI microservice with production-ready structure
"""

import sys
from pathlib import Path
import json

def create_file(path: Path, content: str) -> None:
    """Create a file with given content"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"✓ Created {path}")

def scaffold_service(service_name: str, base_path: str = '.') -> None:
    """Create a production-ready FastAPI service structure"""
    base_dir = Path(base_path) / service_name

    # Create directory structure
    dirs = [
        base_dir / 'src' / service_name / 'api',
        base_dir / 'src' / service_name / 'models',
        base_dir / 'src' / service_name / 'services',
        base_dir / 'src' / service_name / 'utils',
        base_dir / 'tests' / 'unit',
        base_dir / 'tests' / 'integration',
        base_dir / 'k8s',
        base_dir / 'helm',
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / '__init__.py').touch()

    # main.py
    main_content = '''"""
{service_name} API service
"""
import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("{service_name} starting up...")
    yield
    logger.info("{service_name} shutting down...")


app = FastAPI(
    title="{service_name}",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('CORS_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request tracking middleware
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get('x-correlation-id', str(uuid.uuid4()))
    request.state.correlation_id = correlation_id

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        f'{{method}} {{path}} - {{status}} ({{duration:.2f}}s)',
        extra={{
            'method': request.method,
            'path': request.url.path,
            'status': response.status_code,
            'duration': duration,
            'correlation_id': correlation_id
        }}
    )

    response.headers['x-correlation-id'] = correlation_id
    return response


# Health check endpoints
@app.get('/health')
async def health():
    """Liveness probe"""
    return {{'status': 'healthy'}}


@app.get('/ready')
async def readiness():
    """Readiness probe"""
    return {{'status': 'ready'}}


@app.get('/metrics')
async def metrics():
    """Prometheus metrics endpoint"""
    # Implement Prometheus metrics export here
    return {{'metrics': 'available'}}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 8000)),
        reload=os.getenv('ENV') == 'development'
    )
'''.format(service_name=service_name)

    create_file(base_dir / 'src' / service_name / 'main.py', main_content)

    # requirements.txt
    requirements_content = '''fastapi==0.104.0
uvicorn[standard]==0.24.0
pydantic==2.4.0
pydantic-settings==2.0.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
kafka-python==2.0.2
python-dapr==1.10.0
prometheus-client==0.18.0
opentelemetry-api==1.20.0
opentelemetry-sdk==1.20.0
opentelemetry-exporter-jaeger==1.20.0
opentelemetry-instrumentation-fastapi==0.41b0
opentelemetry-instrumentation-sqlalchemy==0.41b0
pytest==7.4.0
httpx==0.25.0
'''
    create_file(base_dir / 'requirements.txt', requirements_content)

    # .env.example
    env_example = '''# Environment
ENV=development
LOG_LEVEL=INFO

# Server
PORT=8000
CORS_ORIGINS=*

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/{service_name}

# Kafka
KAFKA_BROKERS=localhost:9092

# DAPR
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001

# Tracing
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831
'''
    create_file(base_dir / '.env.example', env_example)

    # Dockerfile
    dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src .

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

CMD ["python", "-m", "main"]
'''
    create_file(base_dir / 'Dockerfile', dockerfile_content)

    # Kubernetes deployment
    k8s_deployment = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
    spec:
      containers:
      - name: {service_name}
        image: {service_name}:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: {service_name}
spec:
  selector:
    app: {service_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
'''
    create_file(base_dir / 'k8s' / 'deployment.yaml', k8s_deployment.format(service_name=service_name))

    # Helm values
    helm_values = '''replicaCount: 1

image:
  repository: {service_name}
  tag: latest
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

env:
  LOG_LEVEL: "INFO"
'''
    create_file(base_dir / 'helm' / 'values.yaml', helm_values.format(service_name=service_name))

    # Test file
    test_content = '''"""
Tests for {service_name}
"""
import pytest
from fastapi.testclient import TestClient
from src.{service_name}.main import app

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


def test_readiness():
    response = client.get('/ready')
    assert response.status_code == 200
    assert response.json()['status'] == 'ready'
'''
    create_file(base_dir / 'tests' / 'test_main.py', test_content.format(service_name=service_name))

    # README
    readme_content = '''# {service_name}

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run service
python src/{service_name}/main.py
```

## Testing

```bash
pytest
```

## Docker Build

```bash
docker build -t {service_name}:latest .
docker run -p 8000:8000 {service_name}:latest
```

## Kubernetes Deployment

```bash
kubectl apply -f k8s/
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.
'''.format(service_name=service_name)
    create_file(base_dir / 'README.md', readme_content)

    print(f"\n✓ Service '{service_name}' scaffolded successfully at {base_dir}")
    print("\nNext steps:")
    print(f"  1. cd {service_name}")
    print("  2. python -m venv venv && source venv/bin/activate")
    print("  3. pip install -r requirements.txt")
    print("  4. cp .env.example .env")
    print("  5. python src/{service_name}/main.py".format(service_name=service_name))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scaffold-service.py <service-name>")
        sys.exit(1)

    service_name = sys.argv[1]
    base_path = sys.argv[2] if len(sys.argv) > 2 else '.'
    scaffold_service(service_name, base_path)
