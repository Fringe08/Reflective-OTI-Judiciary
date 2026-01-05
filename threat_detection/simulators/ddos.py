# src/threat_detection/simulators/ddos.py
import requests
import threading
import time


def ddos_worker(worker_id, duration=30):
    """Enhanced DDoS worker with reflective AI monitoring"""
    start_time = time.time()
    request_count = 0
    detections = []

    while time.time() - start_time < duration:
        try:
            ddos_payload = {
                "threat_type": "ddos",
                "indicators": {
                    "request_rate": 1000,
                    "source_ips": [f"10.0.1.{i}" for i in range(1, 51)],
                    "user_agents": ["Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"],
                    "request_types": ["GET", "POST", "HEAD"],
                    "target_endpoints": ["/api/v1/data", "/login", "/api/users"]
                }
            }

            response = requests.post(
                "http://localhost:8001/detect-threat",
                json=ddos_payload,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": "threat-dashboard-key-2024"
                },
                timeout=2
            )
            request_count += 1

            if response.status_code == 200:
                result = response.json().get('detection_result', {})
                if result.get('threat_detected'):
                    detections.append(result)
                    print(f"🚨 Worker {worker_id}: DDoS DETECTED! (Request {request_count})")

                    # Show reflective insights for detections
                    if result.get('reflection_applied'):
                        confidence = result.get('final_confidence', result.get('confidence', 0))
                        print(f"   🎯 Calibrated Confidence: {confidence:.2f}")

        except requests.exceptions.Timeout:
            print(f"⏰ Worker {worker_id}: Request timed out")
        except Exception as e:
            print(f"❌ Worker {worker_id}: Error - {e}")

        time.sleep(0.1)

    return request_count, len(detections)


def simulate_ddos_attack(concurrent_workers=5, duration=30):
    """Enhanced DDoS simulation with reflective AI analytics"""
    print(f"🚀 Starting DDoS simulation with {concurrent_workers} workers for {duration} seconds...")
    print("🌐 Attack Pattern: High-volume requests from multiple sources")

    threads = []
    results = []

    for i in range(concurrent_workers):
        thread = threading.Thread(target=lambda: results.append(ddos_worker(i, duration)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Summary analytics
    total_requests = sum(r[0] for r in results)
    total_detections = sum(r[1] for r in results)
    detection_rate = (total_detections / total_requests) * 100 if total_requests > 0 else 0

    print(f"\n📊 DDoS Simulation Complete!")
    print(f"   📨 Total Requests: {total_requests}")
    print(f"   🚨 Total Detections: {total_detections}")
    print(f"   🎯 Detection Rate: {detection_rate:.1f}%")
    print(f"   👥 Concurrent Workers: {concurrent_workers}")

    if detection_rate > 80:
        print("   ✅ EXCELLENT: High DDoS detection capability!")
    elif detection_rate > 50:
        print("   ⚠️  MODERATE: Moderate DDoS detection")
    else:
        print("   🔴 NEEDS IMPROVEMENT: Low DDoS detection rate")


if __name__ == "__main__":
    simulate_ddos_attack(concurrent_workers=3, duration=10)