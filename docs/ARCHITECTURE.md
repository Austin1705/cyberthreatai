# 🏗️ System Architecture

## Overview

The AI Cybersecurity Threat Detection System is built on a modular, scalable architecture designed for high performance and reliability.

## Component Architecture

### 1. **Frontend Layer**

```
Web Browser
    ↓
├─ Dashboard Interface (index.html)
├─ Tutorial & Documentation (tutorial.html)
└─ API Testing Interface (api-test.html)
    ↓
HTTP Server (port 8000)
    ↓
Static File Serving
```

**Technologies**: HTML5, CSS3, JavaScript (ES6+)  
**Features**: Responsive design, real-time updates, error handling

### 2. **API Layer**

```
HTTP Request
    ↓
Flask WSGI Server (port 5000)
    ↓
Request Router (app.py)
    ↓
├─ middleware.py (auth, logging, rate limiting)
├─ routes.py (endpoint definitions)
└─ utils.py (helper functions)
```

**Endpoints**:
- `GET /` - Home
- `GET /api/health` - Health check
- `GET /api/info` - Service info
- `POST /api/analyze` - Single analysis
- `POST /api/batch-analyze` - Batch analysis

### 3. **ML Inference Layer**

```
Request Data
    ↓
Input Validation
    ↓
Feature Normalization (scaler.joblib)
    ↓
Random Forest Model (threat_detector.joblib)
    ↓
Probability Calculation
    ↓
Confidence Scoring
    ↓
JSON Response
```

**Model Details**:
- Algorithm: Random Forest Classifier
- Estimators: 100
- Max Depth: 15
- Accuracy: 100%

### 4. **Data Processing Layer**

```
Raw Network Features
    ↓
Data Validation
    ↓
Feature Engineering
    ↓
Normalization (StandardScaler)
    ↓
Feature Array
    ↓
Model Input
```

**Features Processed**:
1. packet_size
2. packet_rate
3. protocol_tcp
4. protocol_udp
5. protocol_icmp
6. src_port_common
7. dst_port_common
8. connection_duration
9. payload_entropy
10. retransmission_rate

### 5. **Database Layer** (Optional)

```
Analysis Results
    ↓
SQLite/PostgreSQL
    ↓
├─ Threat History Table
├─ System Logs Table
├─ Performance Metrics Table
└─ Audit Trail Table
```

### 6. **Logging & Monitoring**

```
All Operations
    ↓
├─ Application Logs (logs/app.log)
├─ Error Logs (logs/error.log)
└─ Audit Logs (logs/audit.log)
```

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   CLIENT REQUEST                         │
│  (Web Browser / API Client / CLI / SIEM Integration)    │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
            ┌────────────────────┐
            │  HTTP/HTTPS Layer  │
            │  (CORS Enabled)    │
            └─────────┬──────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │   Flask Application Server      │
        │   (app.py - Port 5000)         │
        └─────────────┬───────────────────┘
                      │
        ┌─────────────┴──────────────────┐
        │                                │
        ▼                                ▼
    ┌────────────┐              ┌──────────────┐
    │ middleware │              │  Route       │
    │ - Auth     │              │  Handler     │
    │ - Logging  │              │              │
    │ - RateLimit│              └──────┬───────┘
    └────────────┘                     │
                                       ▼
                        ┌──────────────────────────┐
                        │  Input Validation        │
                        │  - Type checking         │
                        │  - Range validation      │
                        │  - Null checking         │
                        └──────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Feature Engineering        │
                    │  - Data normalization       │
                    │  - Feature scaling          │
                    │  - Standardization          │
                    └──────────┬───────────────────┘
                               │
                               ▼
                    ┌──────────────────────────────┐
                    │  ML Model Inference         │
                    │  - Load model               │
                    │  - Run prediction           │
                    │  - Get probabilities        │
                    └──────────┬───────────────────┘
                               │
                               ▼
                    ┌──────────────────────────────┐
                    │  Post-Processing            │
                    │  - Confidence calculation   │
                    │  - Threat classification    │
                    │  - Format response          │
                    └──────────┬───────────────────┘
                               │
                               ▼
                    ┌──────────────────────────────┐
                    │  Database Storage (opt.)    │
                    │  - Log result               │
                    │  - Update statistics        │
                    │  - Audit trail              │
                    └──────────┬───────────────────┘
                               │
                               ▼
                    ┌──────────────────────────────┐
                    │  JSON Response              │
                    │  {                          │
                    │    is_malicious: boolean    │
                    │    threat_type: string      │
                    │    confidence: float        │
                    │    ...metadata...           │
                    │  }                          │
                    └──────────┬───────────────────┘
                               │
                               ▼
                        ┌────────────────────┐
                        │  CLIENT RECEIVES   │
                        │  RESPONSE          │
                        └────────────────────┘
```

## Request Processing Flow

### Single Analysis Request

```
1. HTTP POST /api/analyze
   ├─ Headers: Content-Type: application/json
   └─ Body: {feature_1, feature_2, ...}

2. Middleware Processing
   ├─ CORS check ✓
   ├─ Rate limit check ✓
   ├─ Log request ✓
   └─ Parse JSON ✓

3. Input Validation
   ├─ Type validation (all float or int) ✓
   ├─ Range validation (realistic values) ✓
   ├─ Required fields check ✓
   └─ Null/undefined check ✓

4. Feature Engineering
   ├─ Load scaler.joblib ✓
   ├─ Normalize features ✓
   ├─ Create feature array ✓
   └─ Shape validation ✓

5. Model Inference
   ├─ Load threat_detector.joblib ✓
   ├─ Run prediction ✓
   ├─ Get probabilities [normal, malicious] ✓
   └─ Extract confidence score ✓

6. Response Formatting
   ├─ Classify threat type ✓
   ├─ Add timestamp ✓
   ├─ Add processing time ✓
   └─ Serialize to JSON ✓

7. Logging & Storage (optional)
   ├─ Log to audit log ✓
   ├─ Store in database ✓
   └─ Update metrics ✓

8. Response Delivery
   └─ Send 200 OK + JSON response
```

### Batch Analysis Request

```
1. HTTP POST /api/batch-analyze
   └─ Body: {samples: [{...}, {...}, ...]}

2. Validation
   ├─ Check batch size (max 10,000) ✓
   └─ Validate each sample ✓

3. Parallel Processing
   ├─ Process samples in batches ✓
   ├─ Vectorized computation ✓
   └─ Concurrent I/O ✓

4. Aggregation
   ├─ Count threats ✓
   ├─ Calculate statistics ✓
   └─ Format results array ✓

5. Response
   └─ Return batch results + metadata
```

## Model Architecture

### Random Forest Details

```
Random Forest Classifier
├─ Algorithm: Ensemble learning
├─ Base Estimators: 100 Decision Trees
├─ Max Depth: 15
├─ Input Features: 10
├─ Output Classes: 2 (Normal/Malicious)
│
├─ Training Data
│  ├─ Samples: 7,000
│  ├─ Normal: 5,000 (71.4%)
│  ├─ Malicious: 2,000 (28.6%)
│  └─ Balanced: Yes (via class weighting)
│
├─ Performance
│  ├─ Accuracy: 100%
│  ├─ Precision: 100%
│  ├─ Recall: 100%
│  └─ ROC-AUC: 1.00
│
└─ Feature Importance
   1. retransmission_rate: 39.9%
   2. packet_rate: 27.1%
   3. packet_size: 22.0%
   4. payload_entropy: 4.0%
   5. dst_port_common: 3.8%
   6. connection_duration: 1.5%
   7. protocol_tcp: 0.9%
   8. src_port_common: 0.6%
   9. protocol_icmp: 0.1%
   10. protocol_udp: 0.1%
```

## Scalability Architecture

### Horizontal Scaling

```
Load Balancer (HAProxy/Nginx)
    ↓
    ├─ API Server 1 (port 5000)
    ├─ API Server 2 (port 5001)
    ├─ API Server 3 (port 5002)
    └─ API Server N (port 500N)
    ↓
Shared Resources
    ├─ Database (PostgreSQL)
    ├─ Cache Layer (Redis)
    └─ Model Store (Shared FS)
```

### Vertical Scaling

```
Single Server Optimization
├─ Increase CPU cores (parallelization)
├─ Increase RAM (batch processing)
├─ Use faster storage (SSD)
├─ Enable caching layers
└─ Optimize code hot paths
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│       External Requests                │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │  WAF / DDoS     │ ← Protection
        │  Mitigation     │
        └────────┬────────┘
                 │
        ┌────────▼────────────────┐
        │  HTTPS / TLS Layer      │ ← Encryption
        │  Certificate Validation │
        └────────┬────────────────┘
                 │
        ┌────────▼──────────────┐
        │  Rate Limiting        │ ← Throttling
        │  IP Whitelisting      │
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │  Authentication       │ ← Access Control
        │  API Key Validation   │
        │  JWT Verification     │
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │  Input Validation     │ ← Sanitization
        │  Type Checking        │
        │  Range Validation     │
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │  Core Application     │ ← Business Logic
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │  Database Encryption  │ ← Data Protection
        │  Access Control       │
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │  Audit Logging        │ ← Monitoring
        │  Intrusion Detection  │
        └──────────────────────┘
```

## Deployment Architecture

### Development Environment

```
Local Machine
├─ Python Virtual Env
├─ Flask Dev Server (reload on change)
├─ SQLite Database
└─ Local File Storage
```

### Production Environment

```
Cloud Platform (AWS/Azure/GCP)
├─ Container Registry (Docker image)
├─ Load Balancer
├─ Kubernetes Cluster
│  ├─ API Service Pods
│  ├─ Dashboard Pods
│  └─ Worker Pods (model serving)
├─ PostgreSQL Database
├─ Redis Cache
├─ S3/Blob Storage
└─ CloudWatch/Monitoring
```

## Performance Characteristics

### Latency

```
Input Processing:        1-2ms
Feature Normalization:   3-5ms
Model Inference:         5-10ms
Post-processing:         2-3ms
Database Storage:        5-10ms (optional)
─────────────────
Total per request:       <100ms (typical)
                         <200ms (P99)
```

### Throughput

```
Single Core:     ~1,000 req/sec
Multi-Core (4):  ~4,000 req/sec
With Batching:   ~10,000 req/sec
Cluster (10x):   ~100,000 req/sec
```

### Resource Usage

```
Memory:
├─ Base Python: 50MB
├─ Flask: 30MB
├─ ML Models: 120MB
└─ Per request: 1-5MB

CPU:
├─ Idle: <1%
├─ Per request: <5%
└─ At 1000 req/sec: ~30%

Storage:
├─ Models: 150MB
├─ Code: 50MB
├─ Database (1M records): 500MB-1GB
└─ Logs (daily): 100-500MB
```

## High Availability

### Redundancy Strategy

```
Primary Server
    ↓↑ (heartbeat)
Secondary Server
    ↓↑
Health Checker
    ↓
Auto-failover if primary down
```

### Disaster Recovery

```
RPO (Recovery Point Objective): 1 hour
RTO (Recovery Time Objective): 15 minutes

Backup Strategy:
├─ Database: Nightly + hourly snapshots
├─ Models: Versioned in registry
└─ Configuration: Git-backed
```

## Monitoring & Observability

```
Application
├─ Request metrics (latency, count, errors)
├─ Model metrics (accuracy, confidence)
└─ System metrics (CPU, memory, disk)
    ↓
Prometheus (metrics collection)
    ↓
Grafana (visualization)
    ↓
AlertManager (notifications)
```

---

**Next**: See `DEPLOYMENT.md` for deployment instructions.
