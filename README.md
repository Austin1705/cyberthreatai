# AI Cybersecurity Threat Detection System

An intelligent machine learning-based system for real-time detection of malicious network traffic patterns. Uses artificial intelligence to identify potential cyber threats like DDoS attacks, port scanning, and data exfiltration.

## Features

- **Machine Learning Model**: Random Forest classifier trained on synthetic network traffic data
- **Real-time Threat Detection**: REST API for analyzing network traffic
- **Batch Processing**: Process multiple samples simultaneously
- **Feature Importance**: Identifies key indicators of malicious activity
- **Confidence Scoring**: Probability-based threat assessment
- **Web API**: Flask-based interface for easy integration

## Project Structure

```
myproject/
├── data/
│   ├── generate_data.py         # Generate synthetic traffic data
│   └── network_traffic.csv      # Generated dataset
├── models/
│   ├── train_model.py           # ML model training script
│   ├── threat_detector.joblib   # Trained model (generated)
│   └── scaler.joblib            # Feature scaler (generated)
├── app/
│   └── app.py                   # Flask web application
├── test_api.py                  # API testing script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the project directory**:
   ```powershell
   cd c:\Users\Austinsraj\OneDrive\Documents\myproject
   ```

2. **Create a virtual environment** (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

## Quick Start

### Step 1: Generate Training Data
Create synthetic network traffic data for training:
```powershell
python data/generate_data.py
```

This will generate a CSV file with:
- 5,000 samples of normal traffic
- 2,000 samples of malicious traffic
- 10 network features for each sample

### Step 2: Train the Model
Train the threat detection model:
```powershell
python models/train_model.py
```

Output will include:
- Model accuracy and performance metrics
- Confusion matrix
- Feature importance rankings
- Saved model files

### Step 3: Start the API Server
Launch the Flask web server:
```powershell
python app/app.py
```

The server will start on `http://localhost:5000`

### Step 4: Test the API
In a new terminal, run the test script:
```powershell
python test_api.py
```

## API Endpoints

### 1. Home
- **URL**: `GET http://localhost:5000/`
- **Response**: Service information and available endpoints

### 2. Health Check
- **URL**: `GET http://localhost:5000/api/health`
- **Response**: Service status

### 3. Service Info
- **URL**: `GET http://localhost:5000/api/info`
- **Response**: Model details and feature list

### 4. Analyze Single Traffic Sample
- **URL**: `POST http://localhost:5000/api/analyze`
- **Payload**:
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
- **Response**:
  ```json
  {
    "timestamp": "2024-12-03T10:30:45.123456",
    "is_malicious": false,
    "threat_type": "Normal",
    "confidence": 0.95,
    "normal_probability": 0.95,
    "malicious_probability": 0.05
  }
  ```

### 5. Batch Analyze
- **URL**: `POST http://localhost:5000/api/batch-analyze`
- **Payload**:
  ```json
  {
    "samples": [
      {...sample1...},
      {...sample2...}
    ]
  }
  ```
- **Response**: Array of threat detection results

## Features Explained

- **packet_size**: Size of data packets in bytes
- **packet_rate**: Packets sent per second
- **protocol_tcp**: TCP protocol usage (0 or 1)
- **protocol_udp**: UDP protocol usage (0 or 1)
- **protocol_icmp**: ICMP protocol usage (0 or 1)
- **src_port_common**: Source port is commonly used (0 or 1)
- **dst_port_common**: Destination port is commonly used (0 or 1)
- **connection_duration**: Length of connection in seconds
- **payload_entropy**: Randomness of data (higher = more suspicious)
- **retransmission_rate**: Percentage of retransmitted packets

## Model Performance

The trained Random Forest model typically achieves:
- **Accuracy**: ~95-98%
- **Precision**: High (few false positives)
- **Recall**: High (catches most threats)
- **ROC-AUC**: ~0.98

## Example Usage

### Using cURL
```powershell
# Analyze normal traffic
curl -X POST http://localhost:5000/api/analyze `
  -H "Content-Type: application/json" `
  -d @- <<'EOF'
{
  "packet_size": 250,
  "packet_rate": 10,
  "protocol_tcp": 1,
  "protocol_udp": 0,
  "protocol_icmp": 0,
  "src_port_common": 1,
  "dst_port_common": 1,
  "connection_duration": 30,
  "payload_entropy": 4.5,
  "retransmission_rate": 0.02
}
EOF
```

### Using Python
```python
import requests

payload = {
    "packet_size": 250,
    "packet_rate": 10,
    "protocol_tcp": 1,
    "protocol_udp": 0,
    "protocol_icmp": 0,
    "src_port_common": 1,
    "dst_port_common": 1,
    "connection_duration": 30,
    "payload_entropy": 4.5,
    "retransmission_rate": 0.02
}

response = requests.post('http://localhost:5000/api/analyze', json=payload)
print(response.json())
```

## Technology Stack

- **Machine Learning**: scikit-learn (Random Forest)
- **Web Framework**: Flask
- **Data Processing**: Pandas, NumPy
- **Model Serialization**: joblib
- **Testing**: Python requests library

## Security Considerations

This system demonstrates AI-based threat detection. In production:
- Implement authentication for API endpoints
- Use HTTPS/TLS for data in transit
- Add rate limiting to prevent abuse
- Monitor API logs for suspicious patterns
- Regularly retrain models with new threat data
- Implement comprehensive error handling
- Add data validation and sanitization

## Future Enhancements

- Deep learning models (LSTM, Autoencoders)
- Real-time packet capture integration
- Visualization dashboard
- Multi-class threat classification
- Model versioning and A/B testing
- Distributed processing for high-volume traffic
- Integration with SIEM systems

## Troubleshooting

**Issue**: "Model not found" error when starting the API
- **Solution**: Make sure you've run `python models/train_model.py` first

**Issue**: "Data not found" when training the model
- **Solution**: Run `python data/generate_data.py` to generate the dataset

**Issue**: Port 5000 already in use
- **Solution**: Modify the port in `app/app.py` or kill the process using that port

**Issue**: Module not found errors
- **Solution**: Install dependencies with `pip install -r requirements.txt`

## License

This project is provided as an educational example for AI and cybersecurity applications.

## Author

Created as a demonstration of AI-powered cybersecurity threat detection.

---

**Happy threat hunting!** 🛡️
