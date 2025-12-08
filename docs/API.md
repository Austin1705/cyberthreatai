# 📡 API Reference Documentation

Complete API documentation for the AI Cybersecurity Threat Detection System.

## Base URL

```
http://127.0.0.1:5000/api
```

## Authentication

Currently, the system uses simple API validation. For enterprise/production use:

```
Authorization: Bearer YOUR_API_KEY
```

## HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Authentication failed |
| 403 | Forbidden | Access denied |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | Server overloaded |

## Error Response Format

```json
{
  "error": true,
  "code": "INVALID_INPUT",
  "message": "packet_size must be a number between 0 and 10000",
  "timestamp": "2024-12-03T10:30:45.123456",
  "request_id": "req_abc123def456"
}
```

---

## Endpoints

### 1. Home Endpoint

Returns basic service information.

```http
GET /
```

**Response** (200 OK):
```json
{
  "service": "AI Cybersecurity Threat Detection System",
  "version": "1.0.0",
  "status": "running",
  "api_base": "/api",
  "endpoints": {
    "health": "/api/health",
    "info": "/api/info",
    "analyze": "/api/analyze",
    "batch_analyze": "/api/batch-analyze"
  }
}
```

**cURL Example**:
```bash
curl http://127.0.0.1:5000/
```

---

### 2. Health Check Endpoint

Verify the API server and ML model are operational.

```http
GET /api/health
```

**Response** (200 OK):
```json
{
  "status": "ok",
  "timestamp": "2024-12-03T10:30:45.123456",
  "model_status": "loaded",
  "database_status": "connected",
  "uptime_seconds": 3600,
  "response_time_ms": 2.34
}
```

**Response** (503 Service Unavailable):
```json
{
  "status": "error",
  "error": "Model not loaded",
  "timestamp": "2024-12-03T10:30:45.123456"
}
```

**cURL Example**:
```bash
curl http://127.0.0.1:5000/api/health
```

**Python Example**:
```python
import requests

response = requests.get('http://127.0.0.1:5000/api/health')
print(response.json())
# Output: {'status': 'ok', 'model_status': 'loaded', ...}
```

---

### 3. Service Information Endpoint

Get detailed information about the ML model and available features.

```http
GET /api/info
```

**Response** (200 OK):
```json
{
  "service": "AI Threat Detection",
  "version": "1.0.0",
  "model": {
    "type": "Random Forest Classifier",
    "estimators": 100,
    "max_depth": 15,
    "accuracy": 1.0,
    "precision": 1.0,
    "recall": 1.0,
    "roc_auc": 1.0,
    "training_samples": 7000,
    "training_date": "2024-12-03"
  },
  "features": {
    "count": 10,
    "names": [
      "packet_size",
      "packet_rate",
      "protocol_tcp",
      "protocol_udp",
      "protocol_icmp",
      "src_port_common",
      "dst_port_common",
      "connection_duration",
      "payload_entropy",
      "retransmission_rate"
    ],
    "importance": {
      "retransmission_rate": 0.399,
      "packet_rate": 0.271,
      "packet_size": 0.220,
      "payload_entropy": 0.040,
      "dst_port_common": 0.038,
      "connection_duration": 0.015,
      "protocol_tcp": 0.009,
      "src_port_common": 0.006,
      "protocol_icmp": 0.001,
      "protocol_udp": 0.001
    }
  },
  "performance": {
    "avg_response_time_ms": 45.23,
    "max_response_time_ms": 156.78,
    "throughput_requests_per_sec": 250,
    "uptime_hours": 24
  },
  "timestamp": "2024-12-03T10:30:45.123456"
}
```

**cURL Example**:
```bash
curl http://127.0.0.1:5000/api/info
```

---

### 4. Analyze Single Sample

Analyze a single network traffic sample for threats.

```http
POST /api/analyze
Content-Type: application/json
```

**Request Body**:
```json
{
  "packet_size": 256.5,
  "packet_rate": 10.2,
  "protocol_tcp": 1,
  "protocol_udp": 0,
  "protocol_icmp": 0,
  "src_port_common": 1,
  "dst_port_common": 1,
  "connection_duration": 45.3,
  "payload_entropy": 4.2,
  "retransmission_rate": 0.01
}
```

**Response** (200 OK - Normal Traffic):
```json
{
  "is_malicious": false,
  "threat_type": "Normal",
  "confidence": 1.0,
  "normal_probability": 1.0,
  "malicious_probability": 0.0,
  "timestamp": "2024-12-03T10:30:45.123456",
  "processing_time_ms": 12.34,
  "model_version": "1.0"
}
```

**Response** (200 OK - Malicious Traffic):
```json
{
  "is_malicious": true,
  "threat_type": "Malicious",
  "confidence": 1.0,
  "normal_probability": 0.0,
  "malicious_probability": 1.0,
  "timestamp": "2024-12-03T10:30:45.123456",
  "processing_time_ms": 15.67,
  "model_version": "1.0"
}
```

**Response** (400 Bad Request):
```json
{
  "error": true,
  "code": "INVALID_INPUT",
  "message": "Missing required field: packet_size",
  "timestamp": "2024-12-03T10:30:45.123456"
}
```

**Input Validation Rules**:

| Field | Type | Range | Required |
|-------|------|-------|----------|
| packet_size | float | 0 - 10000 | Yes |
| packet_rate | float | 0 - 1000 | Yes |
| protocol_tcp | int | 0 - 1 | Yes |
| protocol_udp | int | 0 - 1 | Yes |
| protocol_icmp | int | 0 - 1 | Yes |
| src_port_common | int | 0 - 1 | Yes |
| dst_port_common | int | 0 - 1 | Yes |
| connection_duration | float | 0 - 10000 | Yes |
| payload_entropy | float | 0 - 8 | Yes |
| retransmission_rate | float | 0 - 1 | Yes |

**cURL Example**:
```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "packet_size": 256.5,
    "packet_rate": 10.2,
    "protocol_tcp": 1,
    "protocol_udp": 0,
    "protocol_icmp": 0,
    "src_port_common": 1,
    "dst_port_common": 1,
    "connection_duration": 45.3,
    "payload_entropy": 4.2,
    "retransmission_rate": 0.01
  }'
```

**Python Example**:
```python
import requests

url = 'http://127.0.0.1:5000/api/analyze'
data = {
    'packet_size': 256.5,
    'packet_rate': 10.2,
    'protocol_tcp': 1,
    'protocol_udp': 0,
    'protocol_icmp': 0,
    'src_port_common': 1,
    'dst_port_common': 1,
    'connection_duration': 45.3,
    'payload_entropy': 4.2,
    'retransmission_rate': 0.01
}

response = requests.post(url, json=data)
result = response.json()

print(f"Threat: {result['threat_type']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Response Time: {result['processing_time_ms']}ms")
```

---

### 5. Batch Analysis

Analyze multiple network traffic samples simultaneously.

```http
POST /api/batch-analyze
Content-Type: application/json
```

**Request Body**:
```json
{
  "samples": [
    {
      "packet_size": 256.5,
      "packet_rate": 10.2,
      "protocol_tcp": 1,
      "protocol_udp": 0,
      "protocol_icmp": 0,
      "src_port_common": 1,
      "dst_port_common": 1,
      "connection_duration": 45.3,
      "payload_entropy": 4.2,
      "retransmission_rate": 0.01
    },
    {
      "packet_size": 512.0,
      "packet_rate": 95.5,
      "protocol_tcp": 1,
      "protocol_udp": 1,
      "protocol_icmp": 1,
      "src_port_common": 0,
      "dst_port_common": 0,
      "connection_duration": 3.2,
      "payload_entropy": 6.8,
      "retransmission_rate": 0.35
    }
  ]
}
```

**Response** (200 OK):
```json
{
  "batch_id": "batch_20241203_103045",
  "total": 2,
  "processed": 2,
  "failed": 0,
  "threats_detected": 1,
  "normal_count": 1,
  "malicious_count": 1,
  "average_confidence": 1.0,
  "processing_time_ms": 45.67,
  "results": [
    {
      "index": 0,
      "is_malicious": false,
      "threat_type": "Normal",
      "confidence": 1.0,
      "malicious_probability": 0.0,
      "processing_time_ms": 12.34
    },
    {
      "index": 1,
      "is_malicious": true,
      "threat_type": "Malicious",
      "confidence": 1.0,
      "malicious_probability": 1.0,
      "processing_time_ms": 15.67
    }
  ],
  "timestamp": "2024-12-03T10:30:45.123456"
}
```

**Response** (400 Bad Request):
```json
{
  "error": true,
  "code": "INVALID_BATCH_SIZE",
  "message": "Batch size exceeds maximum of 10000",
  "timestamp": "2024-12-03T10:30:45.123456"
}
```

**Constraints**:
- Maximum batch size: 10,000 samples
- Maximum request size: 50MB
- Maximum processing time: 30 seconds

**cURL Example**:
```bash
curl -X POST http://127.0.0.1:5000/api/batch-analyze \
  -H "Content-Type: application/json" \
  -d @batch_samples.json
```

**Python Example**:
```python
import requests

url = 'http://127.0.0.1:5000/api/batch-analyze'
data = {
    'samples': [
        # Sample 1 (normal)
        {
            'packet_size': 256.5, 'packet_rate': 10.2,
            'protocol_tcp': 1, 'protocol_udp': 0, 'protocol_icmp': 0,
            'src_port_common': 1, 'dst_port_common': 1,
            'connection_duration': 45.3, 'payload_entropy': 4.2,
            'retransmission_rate': 0.01
        },
        # Sample 2 (malicious)
        {
            'packet_size': 512.0, 'packet_rate': 95.5,
            'protocol_tcp': 1, 'protocol_udp': 1, 'protocol_icmp': 1,
            'src_port_common': 0, 'dst_port_common': 0,
            'connection_duration': 3.2, 'payload_entropy': 6.8,
            'retransmission_rate': 0.35
        }
    ]
}

response = requests.post(url, json=data)
result = response.json()

print(f"Total Analyzed: {result['total']}")
print(f"Threats Detected: {result['threats_detected']}")
for i, res in enumerate(result['results']):
    print(f"Sample {i}: {res['threat_type']} ({res['malicious_probability']:.0%})")
```

---

## Rate Limiting

The API implements rate limiting to prevent abuse:

```
Rate Limit: 60 requests per minute per IP
Burst Limit: 10 requests per second
```

**Rate Limit Headers**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1701591045
```

**Rate Limit Response** (429 Too Many Requests):
```json
{
  "error": true,
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please retry after 60 seconds.",
  "retry_after": 60,
  "timestamp": "2024-12-03T10:30:45.123456"
}
```

---

## Response Time Characteristics

| Operation | Min | Avg | Max | P99 |
|-----------|-----|-----|-----|-----|
| Health check | 1ms | 2ms | 5ms | 4ms |
| Single analyze | 10ms | 15ms | 50ms | 45ms |
| Batch (100 samples) | 50ms | 70ms | 200ms | 180ms |
| Batch (1000 samples) | 500ms | 700ms | 2000ms | 1800ms |

---

## Common Use Cases

### Use Case 1: Real-time DDoS Detection

```python
import requests
import time

api_url = 'http://127.0.0.1:5000/api/analyze'

# Monitor network traffic in real-time
while True:
    # Capture network metrics from your system
    traffic = get_network_metrics()  # Your function
    
    response = requests.post(api_url, json=traffic)
    result = response.json()
    
    if result['is_malicious']:
        print(f"ALERT: DDoS detected! Confidence: {result['confidence']:.2%}")
        trigger_mitigation()  # Your response function
    
    time.sleep(1)  # Check every second
```

### Use Case 2: Batch Analysis of Logs

```python
import requests
import csv

api_url = 'http://127.0.0.1:5000/api/batch-analyze'

# Read network traffic logs
logs = []
with open('network_logs.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        logs.append({
            'packet_size': float(row['packet_size']),
            'packet_rate': float(row['packet_rate']),
            # ... other fields
        })

# Analyze in batches
batch_size = 1000
for i in range(0, len(logs), batch_size):
    batch = logs[i:i+batch_size]
    response = requests.post(api_url, json={'samples': batch})
    results = response.json()
    
    # Process results
    for result in results['results']:
        if result['is_malicious']:
            print(f"Threat detected: {result['threat_type']}")
```

### Use Case 3: API Integration Example

```python
class ThreatDetectionClient:
    def __init__(self, base_url='http://127.0.0.1:5000/api'):
        self.base_url = base_url
    
    def health_check(self):
        """Check API health"""
        r = requests.get(f'{self.base_url}/health')
        return r.json()
    
    def get_info(self):
        """Get model information"""
        r = requests.get(f'{self.base_url}/info')
        return r.json()
    
    def analyze(self, traffic_data):
        """Analyze single sample"""
        r = requests.post(f'{self.base_url}/analyze', json=traffic_data)
        return r.json()
    
    def batch_analyze(self, samples):
        """Analyze multiple samples"""
        r = requests.post(f'{self.base_url}/batch-analyze', 
                         json={'samples': samples})
        return r.json()

# Usage
client = ThreatDetectionClient()
result = client.analyze({
    'packet_size': 256.5,
    'packet_rate': 10.2,
    # ... other fields
})
print(f"Threat detected: {result['is_malicious']}")
```

---

## Webhook Integration (Enterprise)

Forward threat alerts to your systems:

```json
POST https://your-webhook-endpoint.com/threats

{
  "event": "threat_detected",
  "threat_type": "Malicious",
  "confidence": 1.0,
  "timestamp": "2024-12-03T10:30:45.123456",
  "sample": {
    "packet_size": 512.0,
    "packet_rate": 95.5,
    ...
  }
}
```

---

**Version**: 1.0  
**Last Updated**: December 3, 2024  
**Maintainer**: Threat Detection Team
