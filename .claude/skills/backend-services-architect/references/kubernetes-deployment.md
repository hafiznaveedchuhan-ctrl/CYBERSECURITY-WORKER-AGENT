# Kubernetes Deployment Patterns

## Complete Deployment Example

```yaml
---
# Namespace (optional but recommended)
apiVersion: v1
kind: Namespace
metadata:
  name: microservices

---
# ConfigMap for non-sensitive configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
  namespace: microservices
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  KAFKA_BROKERS: "kafka-0.kafka-headless.default.svc.cluster.local:9092"

---
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: order-service-secrets
  namespace: microservices
type: Opaque
data:
  DATABASE_PASSWORD: cGFzc3dvcmQxMjM=  # base64 encoded
  DAPR_API_TOKEN: dGlja2V0MTIz

---
# Deployment with proper resource management
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: microservices
  labels:
    app: order-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  selector:
    matchLabels:
      app: order-service

  template:
    metadata:
      labels:
        app: order-service
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"

    spec:
      serviceAccountName: order-service

      # Init container for pre-flight checks
      initContainers:
      - name: wait-for-db
        image: busybox:1.28
        command: ['sh', '-c', 'until nc -z postgres.microservices.svc.cluster.local 5432; do echo waiting for db; sleep 2; done']

      containers:
      - name: order-service
        image: order-service:1.0.0
        imagePullPolicy: IfNotPresent
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true

        ports:
        - name: http
          containerPort: 8000
          protocol: TCP

        # Environment variables from ConfigMap and Secret
        envFrom:
        - configMapRef:
            name: order-service-config

        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: order-service-secrets
              key: DATABASE_PASSWORD

        # Resource requests and limits (REQUIRED)
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Liveness probe - restart if unhealthy
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 15
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3

        # Readiness probe - remove from traffic if not ready
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 1

        # Volume mounts for temp files
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache

      # Pod-level volumes
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}

      # Pod Disruption Budget (for graceful degradation)
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - order-service
              topologyKey: kubernetes.io/hostname

      terminationGracePeriodSeconds: 30

---
# Service for internal communication
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: microservices
  labels:
    app: order-service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: http
    protocol: TCP
    name: http
  selector:
    app: order-service

---
# HorizontalPodAutoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
  namespace: microservices
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

---
# PodDisruptionBudget (prevent accidental disruption)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: order-service-pdb
  namespace: microservices
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: order-service

---
# ServiceAccount with RBAC
apiVersion: v1
kind: ServiceAccount
metadata:
  name: order-service
  namespace: microservices

---
# ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: order-service-role
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "watch", "list"]

---
# ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: order-service-rolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: order-service-role
subjects:
- kind: ServiceAccount
  name: order-service
  namespace: microservices

---
# NetworkPolicy (restrict traffic)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: order-service-netpol
  namespace: microservices
spec:
  podSelector:
    matchLabels:
      app: order-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 53  # DNS
    - protocol: UDP
      port: 53
```

## Health Check Endpoints

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.get('/health', status_code=status.HTTP_200_OK)
async def health():
    """Liveness check - is the service running?"""
    return {'status': 'alive'}

@app.get('/ready', status_code=status.HTTP_200_OK)
async def readiness():
    """Readiness check - is the service ready to accept traffic?"""
    try:
        # Check database connectivity
        await db.execute("SELECT 1")

        # Check dependencies
        response = httpx.get(f"{dapr_url}/health", timeout=2)
        if response.status_code != 200:
            raise Exception("DAPR unavailable")

        return {
            'status': 'ready',
            'database': 'connected',
            'dapr': 'connected'
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service not ready'
        )
```

## Rolling Update Strategy

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # One extra pod during update
      maxUnavailable: 0    # Zero pods down at any time

      # Timeline:
      # Pod 1,2,3 running (3 total)
      # Surge pod starts (4 total)
      # Pod 1 terminates (3 total) - old version
      # New pod starts (3 total) - new version
      # Repeat for pods 2, 3
```

## Deployment Validation

```bash
# Validate manifest syntax
kubectl apply -f deployment.yaml --dry-run=client

# Check deployment status
kubectl get deployment order-service -o wide

# View pod status
kubectl get pods -l app=order-service

# Check events
kubectl describe deployment order-service

# View logs
kubectl logs -l app=order-service --tail=50

# Port forward for testing
kubectl port-forward svc/order-service 8000:80
```

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| CrashLoopBackOff | Application crashes | Check logs: `kubectl logs <pod> --previous` |
| ImagePullBackOff | Image not found | Verify image name and tag in registry |
| Pending | No resources available | Check node capacity: `kubectl top nodes` |
| Not Ready | Readiness probe failing | Check service dependencies, logs |
| Slow rollout | maxUnavailable too low | Increase maxSurge and adjust strategy |
