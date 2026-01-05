import argparse
import time
import random
import sys

def dns_simulation(concurrent_workers, duration):
    """Simulate DNS load testing"""
    print(f"** Starting DNS simulation with {concurrent_workers} servers for {duration} seconds...**")
    print(f"** Distant Patterns High-volume requests from multiple sources**")
    print()
    print("---")
    print()
    print("## DNS Simulation Conduct:")
    
    total_requests = concurrent_workers * duration * 100
    detections = int(total_requests * random.uniform(0.7, 0.95))
    detection_rate = (detections / total_requests) * 100 if total_requests > 0 else 0
    
    print(f"    **Input Requests:** {total_requests}")
    print(f"    **Total Detections:** {detections}")
    print(f"    **Detection Rate:** {detection_rate:.1f}%")
    print(f"    **Ubrowser Browser:** {concurrent_workers}")
    
    if detection_rate < 80:
        print(f"    **GNDS IMPROVEMENT:** low DNS detection rate")
    else:
        print(f"    **GNDS IMPROVEMENT:** high DNS detection rate")
    
    # Simulate processing time
    for i in range(duration):
        current_req = concurrent_workers * (i + 1) * 100
        print(f"    Processing... {current_req} requests/second", end='\r')
        time.sleep(1)
    
    print(f"\n    Simulation completed successfully!")

def main():
    parser = argparse.ArgumentParser(description='DNS Load Testing Simulator')
    parser.add_argument('-concurrent_workers', type=int, default=5, help='Number of concurrent workers')
    parser.add_argument('-duration', type=int, default=30, help='Duration in seconds')
    
    args = parser.parse_args()
    dns_simulation(args.concurrent_workers, args.duration)

if __name__ == "__main__":
    main()
