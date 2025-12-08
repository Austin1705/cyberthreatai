# 🚀 Deployment Guide

Complete guide for deploying the AI Cybersecurity Threat Detection System to production environments.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Production Checklist](#production-checklist)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Development

### Quick Start (5 minutes)

```powershell
# 1. Clone repository
cd c:\Users\Austinsraj\OneDrive\Documents\myproject

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate data
python data/generate_data.py

# 5. Train model
python models/train_model.py

# 6. Start servers
# Terminal 1:
python app/app.py

# Terminal 2:
python server.py

# 7. Open browser
# Dashboard: http://localhost:8000
# API: http://127.0.0.1:5000
```

### Development Tools

```powershell
# Run tests
pytest

# Check code quality
flake8 app/ models/

# Format code
black app/ models/

# Type checking
mypy app/ models/

# Profiling
python -m cProfile -s cumtime app/app.py
```

---

## Docker Deployment

### Building Docker Image

```powershell
# Build image
docker build -t threat-detection:latest .

# Tag image
docker tag threat-detection:latest myregistry/threat-detection:latest

# Push to registry
docker push myregistry/threat-detection:latest
```

### Running with Docker

```powershell
# Single container
docker run -p 5000:5000 -p 8000:8000 threat-detection:latest

# With environment variables
docker run -p 5000:5000 -p 8000:8000 `
  -e FLASK_ENV=production `
  -e DATABASE_URL=postgresql://user:pass@db:5432/threats `
  threat-detection:latest

# With volume mounts
docker run -p 5000:5000 -p 8000:8000 `
  -v C:\data:/app/data `
  -v C:\logs:/app/logs `
  threat-detection:latest

# Run in background
docker run -d --name threat-detection `
  -p 5000:5000 -p 8000:8000 `
  threat-detection:latest

# View logs
docker logs threat-detection

# Stop container
docker stop threat-detection

# Remove container
docker rm threat-detection
```

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://user:pass@db:5432/threats
    depends_on:
      - db
      - cache
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  dashboard:
    build: .
    ports:
      - "8000:8000"
    environment:
      FLASK_ENV: production
    depends_on:
      - api
    restart: unless-stopped

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: threats
      POSTGRES_USER: user
      POSTGRES_PASSWORD: securepassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  postgres_data:
```

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Restart services
docker-compose restart
```

---

## Cloud Deployment

### AWS Deployment

#### Using EC2

```bash
#!/bin/bash
# Deploy to AWS EC2

# 1. SSH into instance
ssh -i key.pem ec2-user@instance-ip

# 2. Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip git -y

# 3. Clone repository
git clone https://github.com/user/threat-detection.git
cd threat-detection

# 4. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Train model
python models/train_model.py

# 6. Start with systemd
sudo tee /etc/systemd/system/threat-detection.service > /dev/null <<EOF
[Unit]
Description=AI Threat Detection
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/threat-detection
ExecStart=/home/ec2-user/threat-detection/venv/bin/gunicorn -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable threat-detection
sudo systemctl start threat-detection
```

#### Using ECS (Elastic Container Service)

```json
{
  "family": "threat-detection",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "threat-detection-api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/threat-detection:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        },
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/threat-detection",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Azure Deployment

```bash
#!/bin/bash
# Deploy to Azure App Service

# 1. Login to Azure
az login

# 2. Create resource group
az group create --name threat-detection --location eastus

# 3. Create App Service plan
az appservice plan create \
  --name threat-detection-plan \
  --resource-group threat-detection \
  --sku B2

# 4. Create web app
az webapp create \
  --resource-group threat-detection \
  --plan threat-detection-plan \
  --name threat-detection-app \
  --runtime "PYTHON|3.9"

# 5. Deploy code
az webapp deployment source config-zip \
  --resource-group threat-detection \
  --name threat-detection-app \
  --src deployment.zip

# 6. Configure environment
az webapp config appsettings set \
  --resource-group threat-detection \
  --name threat-detection-app \
  --settings FLASK_ENV=production
```

### Google Cloud Deployment

```bash
#!/bin/bash
# Deploy to Google Cloud Run

# 1. Authenticate
gcloud auth login

# 2. Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/threat-detection

# 3. Deploy to Cloud Run
gcloud run deploy threat-detection \
  --image gcr.io/PROJECT_ID/threat-detection \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 1 \
  --allow-unauthenticated \
  --set-env-vars="FLASK_ENV=production"

# 4. View logs
gcloud run logs read threat-detection --limit 50
```

---

## Kubernetes Deployment

### Prerequisites

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Create cluster (if not exists)
# Using minikube for local testing
minikube start --cpus=4 --memory=8192

# Or cloud providers:
# AWS EKS, Azure AKS, Google GKE
```

### Kubernetes Manifests

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: threat-detection-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: threat-detection-api
  template:
    metadata:
      labels:
        app: threat-detection-api
    spec:
      containers:
      - name: api
        image: myregistry/threat-detection:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5

---
# api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: threat-detection-api
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
  selector:
    app: threat-detection-api

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: threat-detection-ingress
spec:
  rules:
  - host: api.threat-detection.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: threat-detection-api
            port:
              number: 80
```

### Deploy to Kubernetes

```bash
# Apply configurations
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
kubectl apply -f ingress.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/threat-detection-api

# Scale deployment
kubectl scale deployment threat-detection-api --replicas=5

# Update image
kubectl set image deployment/threat-detection-api \
  threat-detection-api=myregistry/threat-detection:v2

# Delete deployment
kubectl delete deployment threat-detection-api
```

---

## Production Checklist

### Pre-Deployment

- [ ] Run full test suite (`pytest`)
- [ ] Code review completed
- [ ] Security audit passed
- [ ] Performance benchmarks acceptable
- [ ] Database migrations tested
- [ ] Configuration validated
- [ ] Secrets properly stored (not in code)
- [ ] Documentation updated
- [ ] API versioning in place

### Infrastructure

- [ ] SSL/TLS certificates installed
- [ ] Load balancer configured
- [ ] Database backups enabled
- [ ] Monitoring/alerting set up
- [ ] Logging configured
- [ ] Firewall rules applied
- [ ] DDoS protection enabled
- [ ] CDN configured (if applicable)

### Security

- [ ] API authentication enabled
- [ ] Rate limiting configured
- [ ] Input validation in place
- [ ] SQL injection prevention
- [ ] CORS properly restricted
- [ ] Secrets encrypted
- [ ] SSH keys secured
- [ ] IAM roles configured
- [ ] Audit logging enabled

### Performance

- [ ] Caching configured
- [ ] Database indexes created
- [ ] Query optimization done
- [ ] Connection pooling enabled
- [ ] Load testing passed
- [ ] Stress testing passed
- [ ] Memory leaks checked

### Operations

- [ ] Runbook created
- [ ] Incident response plan
- [ ] Rollback procedure documented
- [ ] On-call rotation established
- [ ] Monitoring dashboards set up
- [ ] Alert thresholds configured
- [ ] Deployment automation in place

---

## Monitoring & Maintenance

### Health Checks

```bash
# API health
curl http://api.threat-detection.com/api/health

# Database health
SELECT * FROM healthcheck; -- or equivalent

# System metrics
# CPU: should be <70% under normal load
# Memory: should be <80%
# Disk: should be <85% full
# Request latency: should be <100ms (p99)
```

### Logging Strategy

```
Application Logs:
├─ Level: INFO for normal, ERROR for issues
├─ Rotation: Daily or 100MB
├─ Retention: 30 days
└─ Format: JSON for easier parsing

Access Logs:
├─ All API requests
├─ Rotation: Daily
├─ Retention: 90 days
└─ Use for analytics

Audit Logs:
├─ Authentication attempts
├─ Configuration changes
├─ Data access
├─ Retention: 1 year
└─ Immutable storage
```

### Backup & Recovery

```bash
# Database backup
pg_dump threat_detection > backup-$(date +%Y%m%d).sql
gzip backup-*.sql

# Model backup
cp models/threat_detector.joblib models/threat_detector.joblib.backup

# Restore database
gunzip < backup-20240101.sql.gz | psql threat_detection

# Test restore
# Regularly test backup/restore process
```

### Updates & Patching

```bash
# Update dependencies
pip list --outdated
pip install --upgrade package-name

# Update Python
# Plan for Python version upgrades (major release every 12 months)

# Model retraining
# Retrain quarterly or when performance degrades
python models/train_model.py --use-new-data

# Security patches
# Apply immediately for critical vulnerabilities
# Test on staging first
```

### Scaling Strategy

```
Vertical Scaling (current server):
├─ Increase CPU (4→8 cores)
├─ Increase RAM (8GB→16GB)
├─ Use SSD storage
└─ Good for: <5x growth

Horizontal Scaling (more servers):
├─ Add load balancer
├─ Run multiple instances
├─ Use database connection pooling
├─ Add caching layer (Redis)
└─ Good for: 5x-100x growth

Database Scaling:
├─ Indexing optimization
├─ Query optimization
├─ Read replicas
├─ Sharding (if needed)
└─ Good for: Large datasets
```

---

**Next Steps**: See `DEVELOPMENT.md` for development guidelines.
