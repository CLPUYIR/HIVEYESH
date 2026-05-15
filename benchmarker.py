import socket
import time
import json
import argparse
import sys

def run_server(port=8100):
    print(f"--- Hyveyesh Benchmark Server listening on {port} ---")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                # Simple loop to receive data and measure throughput
                start_time = time.time()
                total_received = 0
                while True:
                    data = conn.recv(65536)
                    if not data:
                        break
                    total_received += len(data)
                end_time = time.time()
                duration = end_time - start_time
                if duration > 0:
                    mbps = (total_received * 8) / (duration * 1024 * 1024)
                    print(f"Received {total_received} bytes in {duration:.2f}s ({mbps:.2f} Mbps)")

def run_client(server_ip, port=8100, duration=5):
    print(f"--- Hyveyesh Benchmark Client connecting to {server_ip}:{port} ---")
    data = b'x' * 65536
    total_sent = 0
    
    # 1. Bandwidth Test
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, port))
            start_time = time.time()
            while time.time() - start_time < duration:
                s.sendall(data)
                total_sent += len(data)
            end_time = time.time()
        
        real_duration = end_time - start_time
        mbps = (total_sent * 8) / (real_duration * 1024 * 1024)
        print(f"Sent {total_sent} bytes in {real_duration:.2f}s ({mbps:.2f} Mbps)")
    except Exception as e:
        print(f"Bandwidth test failed: {e}")
        return

    # 2. Jitter/Latency Test (ICMP-like but over TCP for simplicity/permissions)
    latencies = []
    print("Measuring Jitter...")
    try:
        for _ in range(20):
            start = time.perf_counter()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                s.connect((server_ip, port))
                s.sendall(b'ping')
            latencies.append((time.perf_counter() - start) * 1000)
            time.sleep(0.05)
        
        avg_latency = sum(latencies) / len(latencies)
        jitter = sum(abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))) / (len(latencies) - 1)
        print(f"Avg Latency: {avg_latency:.2f}ms | Jitter: {jitter:.2f}ms")
    except Exception as e:
        print(f"Latency test failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hyveyesh Network Benchmarker")
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--ip", help="Server IP (required for client mode)")
    parser.add_argument("--port", type=int, default=8100)
    parser.add_argument("--duration", type=int, default=5)
    
    args = parser.parse_args()
    
    if args.mode == "server":
        run_server(args.port)
    else:
        if not args.ip:
            print("Error: --ip is required for client mode")
            sys.exit(1)
        run_client(args.ip, args.port, args.duration)
