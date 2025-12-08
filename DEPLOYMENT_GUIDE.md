# Website Deployment Guide

## Current Setup
- **Frontend Server**: http://localhost:8000 (Python SimpleHTTPServer)
- **API Server**: http://127.0.0.1:5001 (Flask)
- **Database**: SQLite (website_threats.db)
- **ML Model**: threat_detector.joblib + scaler.joblib

## Deployment Options

### Option 1: Local Network Deployment (Recommended for Testing)
Make the servers accessible from other machines on your network:

```powershell
# Edit server.py to bind to 0.0.0.0 instead of localhost
# Then access via: http://<your-ip>:8000
```

### Option 2: Cloud Deployment (AWS, Heroku, Azure, DigitalOcean)

#### Prerequisites:
- Python 3.14+
- pip (Python package manager)
- Git
- Cloud provider account

#### Step 1: Prepare Project for Deployment

1. Create `Procfile` for cloud deployment:
```
web: python server.py
api: python app/app.py
```

2. Create `runtime.txt`:
```
python-3.14.0
```

3. Create `.gitignore`:
```
__pycache__/
*.pyc
.env
*.db
models/threat_detector.joblib
models/scaler.joblib
data/
.DS_Store
```

4. Install requirements:
```powershell
pip freeze > requirements.txt
```

#### Step 2: Deploy to Heroku (Free Option)

```powershell
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Deploy code
git push heroku main

# View logs
heroku logs --tail
```

#### Step 3: Deploy to AWS EC2

1. Launch EC2 instance (Ubuntu 20.04)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install python3.14 python3-pip
```

4. Clone repository:
```bash
git clone https://github.com/Austin1705/FlaskApp.git
cd FlaskApp
```

5. Install requirements:
```bash
pip install -r requirements.txt
```

6. Run servers with systemd:
```bash
# Create service files
sudo nano /etc/systemd/system/threat-api.service
sudo nano /etc/systemd/system/threat-web.service
```

### Option 3: Docker Deployment (Production)

Create `Dockerfile`:
```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001 8000

CMD ["sh", "-c", "python app/app.py & python server.py"]
```

Build and run:
```bash
docker build -t threat-detection .
docker run -p 5001:5001 -p 8000:8000 threat-detection
```

## Important Notes Before Deployment

1. **API URL Update**: Update `API_URL` in HTML files from `127.0.0.1:5001` to your deployment URL
2. **CORS Configuration**: Update CORS settings in `app/app.py`
3. **Environment Variables**: Use `.env` file for sensitive data
4. **Database Migration**: Back up `website_threats.db` before deployment
5. **SSL/HTTPS**: Use Let's Encrypt for free SSL certificates
6. **Authentication**: Implement user authentication for production

## Quick Local Network Deployment

To make your site accessible from other computers on your network:

```powershell
# Get your IP address
ipconfig

# Update server binding (edit server.py)
# Change: TCPServer(("", PORT)...)
# This makes it accessible at: http://<your-ip>:8000
```

## Monitoring & Maintenance

- Monitor API logs: Check `api.log` for errors
- Database backup: Regular backups of `website_threats.db`
- Model updates: Retrain model with new data regularly
- Security: Keep dependencies updated

## Support

For issues, check:
- `README.md` - Project overview
- `START_HERE.md` - Quick start guide
- `api.log` - API errors
