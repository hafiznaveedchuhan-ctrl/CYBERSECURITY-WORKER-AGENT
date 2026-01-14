# Helm Chart Best Practices

## Chart Structure

```
order-service-chart/
├── Chart.yaml                 # Chart metadata
├── values.yaml               # Default values (dev-friendly)
├── values-dev.yaml          # Dev environment overrides
├── values-staging.yaml       # Staging overrides
├── values-prod.yaml          # Production overrides
├── charts/                    # Dependency charts
│   └── postgres/             # Subchart example
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── pdb.yaml
│   ├── _helpers.tpl          # Helper templates
│   └── NOTES.txt             # Post-install notes
└── README.md                 # Chart documentation
```

## Chart.yaml Template

```yaml
apiVersion: v2
name: order-service
description: Order Service microservice
type: application

version: 1.0.0         # Chart version (semantic versioning)
appVersion: "1.0.0"    # Application version

keywords:
  - order
  - microservice

home: https://example.com
sources:
  - https://github.com/org/order-service

maintainers:
  - name: Platform Team
    email: platform@example.com

dependencies:
  - name: postgres
    version: "14.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgres.enabled
```

## Values.yaml Structure

```yaml
# Global settings shared across all replicas
global:
  environment: dev
  domain: "example.local"
  imagePullSecrets: []

# Service-specific configuration
replicaCount: 1

image:
  repository: order-service
  tag: latest
  pullPolicy: IfNotPresent

# Pod configuration
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

securityContext:
  readOnlyRootFilesystem: true

# Resource limits
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

# Autoscaling
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

# Database configuration
database:
  enabled: true
  name: order_db
  username: order_user
  passwordSecret: order-db-password

# Kafka configuration
kafka:
  enabled: true
  brokers: "kafka-0.kafka-headless:9092"
  topics:
    orders: "order.events.created"

# DAPR configuration
dapr:
  enabled: true
  appPort: 8000
  appId: order-service
  state:
    enabled: true
    storeName: order-state

# Environment variables
env:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "dev"

# Secrets (managed separately, not in values!)
secrets: {}
  # Use helm secrets or external secret management

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8000

# Ingress
ingress:
  enabled: false
  className: "nginx"
  annotations: {}
  hosts:
    - host: "order-service.example.com"
      paths:
        - path: /
          pathType: Prefix
  tls: []

# Node selection
nodeSelector: {}
tolerations: []
affinity: {}
```

## Production Values Override

```yaml
# values-prod.yaml
global:
  environment: prod
  domain: "api.example.com"

replicaCount: 3

image:
  tag: "1.0.0"  # Explicit version, never 'latest'
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70

env:
  LOG_LEVEL: "WARN"
  ENVIRONMENT: "prod"

service:
  type: LoadBalancer

ingress:
  enabled: true
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: "api.example.com"
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: order-service-tls
      hosts:
        - "api.example.com"
```

## Template Helpers (_helpers.tpl)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "order-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "order-service.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "order-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "order-service.labels" -}}
helm.sh/chart: {{ include "order-service.chart" . }}
{{ include "order-service.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "order-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "order-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Deployment.yaml Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "order-service.fullname" . }}
  labels:
    {{- include "order-service.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "order-service.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "order-service.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.podSecurityContext }}
      securityContext:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
      - name: {{ .Chart.Name }}
        {{- with .Values.securityContext }}
        securityContext:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        {{- with .Values.env }}
        env:
        {{- range $key, $value := . }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        {{- end }}
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        {{- with .Values.resources }}
        resources:
          {{- toYaml . | nindent 12 }}
        {{- end }}
```

## Installation Commands

```bash
# Validate chart
helm lint ./order-service-chart

# Dry run to see what will be installed
helm install order-service ./order-service-chart \
  -f values-prod.yaml \
  --dry-run --debug

# Install release
helm install order-service ./order-service-chart \
  -f values-prod.yaml \
  -n microservices \
  --create-namespace

# Upgrade release
helm upgrade order-service ./order-service-chart \
  -f values-prod.yaml \
  -n microservices

# Check release status
helm status order-service -n microservices

# Rollback to previous release
helm rollback order-service 1 -n microservices

# List all releases
helm list -A

# Get values used in release
helm get values order-service -n microservices

# Uninstall release
helm uninstall order-service -n microservices
```

## Pre/Post Install Hooks

```yaml
# Pre-install hook for database migrations
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "order-service.fullname" . }}-db-migrate
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-5"
spec:
  template:
    spec:
      containers:
      - name: db-migrate
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        command: ["python", "-m", "alembic", "upgrade", "head"]
      restartPolicy: Never
  backoffLimit: 3
```

## Chart Version Management

```yaml
# Semantic versioning: MAJOR.MINOR.PATCH
# Increment:
# - MAJOR: Breaking changes to values schema
# - MINOR: New features, backwards compatible
# - PATCH: Bug fixes

# Chart versions do NOT need to match app versions
# Example:
# Chart v2.0.0 can deploy app v1.0.0
# Chart v2.1.0 can deploy app v1.0.0 or v1.1.0

# Document breaking changes in release notes
```

## Validation Checklist

- [ ] Chart lints without errors
- [ ] All templates use helper functions
- [ ] Production values override sensitive defaults
- [ ] Secrets are NOT in values.yaml
- [ ] All resource limits are specified
- [ ] Health checks configured
- [ ] Pre/post-install hooks tested
- [ ] README includes installation instructions
- [ ] Chart version incremented appropriately
- [ ] Dependencies pinned to specific versions
