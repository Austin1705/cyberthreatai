#!/usr/bin/env python
"""Test the scanner API"""
import requests
import json
import time

time.sleep(2)  # Wait for server to start

try:
    # Test health endpoint
    print("Testing /api/health endpoint...")
    r = requests.get('http://localhost:5000/api/health', timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}\n")
    
    # Test scan-website endpoint
    print("Testing /api/scan-website endpoint...")
    payload = {'url': 'https://www.example.com'}
    r = requests.post('http://localhost:5000/api/scan-website', json=payload, timeout=30)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        result = r.json()
        print(f"Threat Level: {result.get('threat_level')}")
        print(f"Threat Score: {result.get('threat_score')}")
        print(f"Vulnerabilities Found: {result.get('vulnerabilities_found')}")
    else:
        print(f"Error: {r.text}")
        
except Exception as e:
    print(f"Error: {e}")
