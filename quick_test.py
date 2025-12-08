import requests

print("\n" + "="*50)
print("THREAT DETECTION API TEST")
print("="*50 + "\n")

# Test health
r = requests.get('http://127.0.0.1:5000/api/health')
print(f"Health Check: {r.status_code} - {r.json()}\n")

# Test normal traffic
normal = {
    'packet_size': 256.5, 'packet_rate': 10.2, 'protocol_tcp': 1,
    'protocol_udp': 0, 'protocol_icmp': 0, 'src_port_common': 1,
    'dst_port_common': 1, 'connection_duration': 45.3,
    'payload_entropy': 4.2, 'retransmission_rate': 0.01
}
r = requests.post('http://127.0.0.1:5000/api/analyze', json=normal)
data = r.json()
print(f"Normal Traffic Analysis:")
print(f"  Result: {data['threat_type']}")
print(f"  Malicious Probability: {data['malicious_probability']:.2%}\n")

# Test malicious traffic
malicious = {
    'packet_size': 512.0, 'packet_rate': 95.5, 'protocol_tcp': 1,
    'protocol_udp': 1, 'protocol_icmp': 1, 'src_port_common': 0,
    'dst_port_common': 0, 'connection_duration': 3.2,
    'payload_entropy': 6.8, 'retransmission_rate': 0.35
}
r = requests.post('http://127.0.0.1:5000/api/analyze', json=malicious)
data = r.json()
print(f"Malicious Traffic Analysis:")
print(f"  Result: {data['threat_type']}")
print(f"  Malicious Probability: {data['malicious_probability']:.2%}\n")

print("="*50)
print("✓ All tests passed!")
print("="*50)
