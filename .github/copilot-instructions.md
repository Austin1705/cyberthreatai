# AI Cybersecurity Threat Detection System - Project Instructions

This is an AI-powered network threat detection system built with machine learning and Flask.

## Project Overview

- **Type**: Python ML/Web Application
- **Purpose**: Real-time detection of malicious network traffic using AI
- **Framework**: Flask (Web API), scikit-learn (ML Model)
- **Status**: Fully functional and ready to run

## Quick Start

1. **Generate training data**:
   ```powershell
   python data/generate_data.py
   ```

2. **Train the ML model**:
   ```powershell
   python models/train_model.py
   ```

3. **Start the API server**:
   ```powershell
   python app/app.py
   ```

4. **Test the API** (in new terminal):
   ```powershell
   python test_api.py
   ```

## Project Structure

- `data/generate_data.py` - Creates synthetic network traffic data
- `models/train_model.py` - Trains Random Forest threat detection model
- `app/app.py` - Flask REST API server
- `test_api.py` - API testing script
- `requirements.txt` - Python dependencies

## Key Features

- Machine Learning threat detection using Random Forest
- REST API with batch processing support
- Real-time confidence scoring
- Feature importance analysis
- Synthetic data generation for training

## API Endpoints

- `GET /` - Home
- `GET /api/health` - Health check
- `GET /api/info` - Service info
- `POST /api/analyze` - Analyze single traffic sample
- `POST /api/batch-analyze` - Analyze multiple samples

See README.md for detailed documentation.
