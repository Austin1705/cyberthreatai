"""
Generate synthetic network traffic data for training the threat detection model.
Creates normal and malicious traffic patterns.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_normal_traffic(num_samples=5000):
    """Generate normal network traffic patterns."""
    data = {
        'packet_size': np.random.normal(256, 50, num_samples),
        'packet_rate': np.random.normal(10, 2, num_samples),
        'protocol_tcp': np.random.binomial(1, 0.6, num_samples),
        'protocol_udp': np.random.binomial(1, 0.3, num_samples),
        'protocol_icmp': np.random.binomial(1, 0.1, num_samples),
        'src_port_common': np.random.binomial(1, 0.8, num_samples),
        'dst_port_common': np.random.binomial(1, 0.75, num_samples),
        'connection_duration': np.random.exponential(30, num_samples),
        'payload_entropy': np.random.normal(4.5, 1, num_samples),
        'retransmission_rate': np.random.uniform(0, 0.05, num_samples),
        'label': 0  # 0 = normal traffic
    }
    return pd.DataFrame(data)

def generate_malicious_traffic(num_samples=2000):
    """Generate malicious network traffic patterns (DDoS, port scanning, exfiltration)."""
    data = {
        'packet_size': np.random.normal(512, 100, num_samples),
        'packet_rate': np.random.normal(100, 30, num_samples),  # High rate
        'protocol_tcp': np.random.binomial(1, 0.7, num_samples),
        'protocol_udp': np.random.binomial(1, 0.5, num_samples),
        'protocol_icmp': np.random.binomial(1, 0.3, num_samples),
        'src_port_common': np.random.binomial(1, 0.2, num_samples),  # Uncommon ports
        'dst_port_common': np.random.binomial(1, 0.15, num_samples),
        'connection_duration': np.random.exponential(5, num_samples),  # Short connections
        'payload_entropy': np.random.normal(6.5, 1.5, num_samples),  # High entropy
        'retransmission_rate': np.random.uniform(0.1, 0.5, num_samples),  # High retransmission
        'label': 1  # 1 = malicious traffic
    }
    return pd.DataFrame(data)

def create_dataset():
    """Create and save the complete dataset."""
    print("Generating synthetic network traffic data...")
    
    normal = generate_normal_traffic(5000)
    malicious = generate_malicious_traffic(2000)
    
    df = pd.concat([normal, malicious], ignore_index=True)
    df = df.sample(frac=1).reset_index(drop=True)  # Shuffle
    
    data_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(data_dir, 'network_traffic.csv')
    df.to_csv(csv_path, index=False)
    
    print(f"Dataset created with {len(df)} samples")
    print(f"Normal traffic: {len(normal)} samples")
    print(f"Malicious traffic: {len(malicious)} samples")
    print(f"Saved to: {csv_path}")
    
    return df

if __name__ == '__main__':
    create_dataset()
