"""
Test script for the threat detection API.
Demonstrates how to use the API endpoints.
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_api():
    """Test the API with a simple request."""
    print("\n" + "="*60)
    print("  THREAT DETECTION API TEST")
    print("="*60 + "\n")
    
    try:
        # Test health check first
        print("Testing API Health...")
        response = requests.get(f'{BASE_URL}/api/health', timeout=5)
        print(f"✓ API is running (Status: {response.status_code})\n")
        
        # Test normal traffic
        print("Testing NORMAL Traffic Detection...")
        normal_traffic = {
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
        
        response = requests.post(f'{BASE_URL}/api/analyze', json=normal_traffic, timeout=5)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Result: {result['threat_type']} (Confidence: {result['confidence']:.2%})")
        print(f"Malicious Probability: {result['malicious_probability']:.4f}\n")
        
        # Test malicious traffic
        print("Testing MALICIOUS Traffic Detection...")
        malicious_traffic = {
            'packet_size': 512.0,
            'packet_rate': 95.5,
            'protocol_tcp': 1,
            'protocol_udp': 1,
            'protocol_icmp': 1,
            'src_port_common': 0,
            'dst_port_common': 0,
            'connection_duration': 3.2,
            'payload_entropy': 6.8,
            'retransmission_rate': 0.35
        }
        
        response = requests.post(f'{BASE_URL}/api/analyze', json=malicious_traffic, timeout=5)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Result: {result['threat_type']} (Confidence: {result['confidence']:.2%})")
        print(f"Malicious Probability: {result['malicious_probability']:.4f}\n")
        
        # Test batch analysis
        print("Testing BATCH Analysis...")
        batch_data = {
            'samples': [
                {
                    'packet_size': 250.0,
                    'packet_rate': 8.5,
                    'protocol_tcp': 1,
                    'protocol_udp': 0,
                    'protocol_icmp': 0,
                    'src_port_common': 1,
                    'dst_port_common': 1,
                    'connection_duration': 30.0,
                    'payload_entropy': 4.5,
                    'retransmission_rate': 0.02
                },
                {
                    'packet_size': 600.0,
                    'packet_rate': 120.0,
                    'protocol_tcp': 1,
                    'protocol_udp': 1,
                    'protocol_icmp': 1,
                    'src_port_common': 0,
                    'dst_port_common': 0,
                    'connection_duration': 2.0,
                    'payload_entropy': 7.0,
                    'retransmission_rate': 0.4
                }
            ]
        }
        
        response = requests.post(f'{BASE_URL}/api/batch-analyze', json=batch_data, timeout=5)
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Processed {result['total_samples']} samples")
        for i, res in enumerate(result['results'], 1):
            print(f"  Sample {i}: {res['threat_type']} (Confidence: {res['confidence']:.2%})")
        
        print("\n" + "="*60)
        print("✓ All tests completed successfully!")
        print("="*60 + "\n")
    
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the server.")
        print("  Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == '__main__':
    test_api()
