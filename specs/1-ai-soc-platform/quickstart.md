# Quickstart Guide: AI-SOC SecOps Agents Platform

**Branch**: `1-ai-soc-platform` | **Date**: 2026-01-04 | **Phase**: 1
**Input**: [plan.md](./plan.md) | [data-model.md](./data-model.md)

---

## Prerequisites

Ensure the following tools are installed on your development machine:

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| Docker Desktop | 4.25+ | Container runtime | [docker.com](https://www.docker.com/products/docker-desktop) |
| Minikube | 1.32+ | Local Kubernetes | `choco install minikube` / `brew install minikube` |
| kubectl | 1.28+ | Kubernetes CLI | `choco install kubernetes-cli` / `brew install kubectl` |
| Helm | 3.13+ | Kubernetes package manager | `choco install kubernetes-helm` / `brew install helm` |
| Dapr CLI | 1.12+ | Dapr runtime | [docs.dapr.io](https://docs.dapr.io/getting-started/install-dapr-cli/) |
| Node.js | 20.x LTS | Frontend/Docs runtime | [nodejs.org](https://nodejs.org/) |
| Python | 3.11+ | Backend runtime | [python.org](https://www.python.org/) |
| Poetry | 1.7+ | Python dependency management | `pip install poetry` |
| pnpm | 8.x | Node.js package manager | `npm install -g pnpm` |

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/hafiznaveedchuhan-ctrl/Agentic-AI-CYBERSECURITY.git
cd Agentic-AI-CYBERSECURITY
git checkout 1-ai-soc-platform
```

### 2. Configure Environment Variables

Create a `.env` file in the repository root:

```bash
# Copy template
cp .env.example .env
```

Required environment variables:

```env
# OpenAI API
OPENAI_API_KEY=sk-your-key-here
OPENAI_ORG_ID=org-your-org-id  # Optional

# Neon Postgres
DATABASE_URL=postgresql://user:password@host.neon.tech/ai_soc?sslmode=require

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Optional for local

# JWT Secrets
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_REFRESH_SECRET_KEY=your-refresh-secret-key

# Service Configuration
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
TOKEN_BUDGET_PER_REQUEST=4000
TOKEN_BUDGET_PER_MONTH=1000000
```

### 3. Start Minikube Cluster

```bash
# Start Minikube with adequate resources
minikube start \
  --memory=8192 \
  --cpus=4 \
  --driver=docker \
  --kubernetes-version=v1.28.0

# Verify cluster is running
kubectl cluster-info
```

### 4. Initialize Dapr

```bash
# Install Dapr on the cluster
dapr init --kubernetes --wait

# Verify Dapr is running
dapr status -k
```

Expected output:
```
NAME                   NAMESPACE    HEALTHY  STATUS   REPLICAS  VERSION  AGE
dapr-sidecar-injector  dapr-system  True     Running  1         1.12.0   2m
dapr-operator          dapr-system  True     Running  1         1.12.0   2m
dapr-placement-server  dapr-system  True     Running  1         1.12.0   2m
dapr-sentry            dapr-system  True     Running  1         1.12.0   2m
```

---

## Local Development (Without Kubernetes)

For rapid development, run services directly:

### Backend Services

```bash
# Navigate to backend
cd backend

# Install dependencies
poetry install

# Run database migrations
poetry run alembic upgrade head

# Start chatbot API (terminal 1)
poetry run uvicorn services.chatbot_api.main:app --reload --port 8000

# Start RAG service (terminal 2)
poetry run uvicorn services.rag_service.main:app --reload --port 8003

# Start ingestion service (terminal 3)
poetry run uvicorn services.ingestion_service.main:app --reload --port 8002
```

### MCP Server

```bash
# Navigate to MCP
cd mcp

# Install dependencies
poetry install

# Start MCP server
poetry run uvicorn server.main:app --reload --port 8001
```

### Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

Access at: http://localhost:3000

### Documentation (Docusaurus)

```bash
# Navigate to docs
cd docs

# Install dependencies
pnpm install

# Start development server
pnpm start
```

Access at: http://localhost:3001

### Local Qdrant

```bash
# Run Qdrant in Docker
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest

# Verify Qdrant is running
curl http://localhost:6333/health
```

---

## Kubernetes Development

### 1. Build Docker Images

```bash
# Build all images
docker compose build

# Or build individually
docker build -t ai-soc-frontend:dev ./frontend
docker build -t ai-soc-docs:dev ./docs
docker build -t ai-soc-chatbot-api:dev ./backend/services/chatbot_api
docker build -t ai-soc-rag-service:dev ./backend/services/rag_service
docker build -t ai-soc-ingestion-service:dev ./backend/services/ingestion_service
docker build -t ai-soc-mcp-server:dev ./mcp
```

### 2. Load Images into Minikube

```bash
# Load images into Minikube's Docker daemon
minikube image load ai-soc-frontend:dev
minikube image load ai-soc-docs:dev
minikube image load ai-soc-chatbot-api:dev
minikube image load ai-soc-rag-service:dev
minikube image load ai-soc-ingestion-service:dev
minikube image load ai-soc-mcp-server:dev
```

### 3. Create Kubernetes Secrets

```bash
# Create namespace
kubectl create namespace ai-soc

# Create secrets from .env file
kubectl create secret generic ai-soc-secrets \
  --from-env-file=.env \
  --namespace=ai-soc
```

### 4. Deploy with Helm

```bash
# Add Dapr Helm repo
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

# Deploy Dapr components
kubectl apply -f deploy/dapr/components/ -n ai-soc

# Deploy AI-SOC platform
helm install ai-soc ./deploy/helm/ai-soc-platform \
  -f ./deploy/helm/values-local.yaml \
  --namespace ai-soc
```

### 5. Access Services

```bash
# Port forward frontend
kubectl port-forward svc/frontend 3000:80 -n ai-soc &

# Port forward docs
kubectl port-forward svc/docs 3001:80 -n ai-soc &

# Port forward API (for debugging)
kubectl port-forward svc/chatbot-api 8000:80 -n ai-soc &
```

Access:
- Frontend: http://localhost:3000
- Docs: http://localhost:3001
- API: http://localhost:8000/docs

---

## Ingesting Textbook Content

### Initial Ingestion

```bash
# Start ingestion job via API
curl -X POST http://localhost:8002/ingest/textbook \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "source": "local",
    "source_path": "./docs/docs",
    "chunk_config": {
      "chunk_size": 500,
      "chunk_overlap": 50
    }
  }'
```

### Verify Ingestion

```bash
# Check job status
curl http://localhost:8002/ingest/jobs/<job_id> \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Check Qdrant collection
curl http://localhost:6333/collections/textbook_chunks
```

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=. --cov-report=html

# Run specific test file
poetry run pytest tests/unit/test_agents.py

# Run integration tests (requires running services)
poetry run pytest tests/integration/ --run-integration
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
pnpm test

# Run E2E tests (requires running backend)
pnpm test:e2e

# Run tests with UI
pnpm test:e2e:ui
```

### RAG Evaluation

```bash
cd backend

# Run RAG evaluation suite
poetry run python -m scripts.run_rag_eval \
  --eval-set evaluation/textbook_eval.json \
  --output results/rag_eval_$(date +%Y%m%d).json
```

---

## Observability Setup

### Local Observability Stack

```bash
# Deploy Prometheus + Grafana + Jaeger
kubectl apply -f deploy/observability/ -n ai-soc

# Port forward Grafana
kubectl port-forward svc/grafana 3002:3000 -n ai-soc &

# Port forward Jaeger
kubectl port-forward svc/jaeger-query 16686:16686 -n ai-soc &
```

Access:
- Grafana: http://localhost:3002 (admin/admin)
- Jaeger: http://localhost:16686

### Import Dashboards

```bash
# Import pre-configured dashboards
cd deploy/observability/grafana
./import-dashboards.sh
```

---

## Troubleshooting

### Common Issues

**Issue**: Pods stuck in `Pending` state
```bash
# Check events
kubectl describe pod <pod-name> -n ai-soc

# Check resources
kubectl top nodes
```

**Issue**: Dapr sidecar not injecting
```bash
# Verify annotation
kubectl get deployment <deployment> -n ai-soc -o jsonpath='{.spec.template.metadata.annotations}'

# Should contain: dapr.io/enabled: "true"
```

**Issue**: Cannot connect to Qdrant
```bash
# Check Qdrant pods
kubectl get pods -l app=qdrant -n ai-soc

# Check Qdrant logs
kubectl logs -l app=qdrant -n ai-soc
```

**Issue**: OpenAI rate limiting
```bash
# Check current usage
curl http://localhost:8000/metrics | grep openai

# Adjust rate limits in config
kubectl edit configmap ai-soc-config -n ai-soc
```

### Logs

```bash
# View service logs
kubectl logs -f deployment/chatbot-api -n ai-soc

# View all pods
kubectl logs -f -l app.kubernetes.io/part-of=ai-soc -n ai-soc --max-log-requests=10
```

### Reset Environment

```bash
# Delete all resources
helm uninstall ai-soc -n ai-soc
kubectl delete namespace ai-soc

# Reset Minikube
minikube delete
```

---

## Development Workflow

### Daily Workflow

1. **Start cluster**: `minikube start`
2. **Check status**: `kubectl get pods -n ai-soc`
3. **Forward ports**: `./scripts/local-dev.sh`
4. **Make changes**: Edit code
5. **Rebuild affected services**: `docker compose build <service>`
6. **Reload in Minikube**: `minikube image load <image>`
7. **Restart deployment**: `kubectl rollout restart deployment/<name> -n ai-soc`

### Hot Reload (Development Mode)

For rapid iteration, use local development mode (without K8s):

```bash
# Terminal 1: Backend API with reload
cd backend && poetry run uvicorn services.chatbot_api.main:app --reload

# Terminal 2: Frontend with HMR
cd frontend && pnpm dev

# Terminal 3: Docs with HMR
cd docs && pnpm start
```

---

## Next Steps

1. Complete environment setup
2. Run initial textbook ingestion
3. Verify RAG retrieval is working
4. Test authentication flow
5. Test agent interactions
6. Review observability dashboards

For implementation tasks, run `/sp.tasks` to generate the task breakdown.
