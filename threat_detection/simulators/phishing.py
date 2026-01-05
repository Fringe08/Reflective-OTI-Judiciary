# src/threat_detection/simulators/phishing.py
import requests
import json
import time


def simulate_phishing_attack():
    """Enhanced phishing simulation with reflective AI insights"""
    phishing_payload = {
        "threat_type": "phishing",
        "indicators": {
            "suspicious_sender": "security@paypa1.com",  # Typosquatting
            "urgent_language": True,
            "contains_links": True,
            "suspicious_domains": ["paypa1-login.com", "secure-bank-update.com"],
            "attachments_present": True,
            "grammar_errors": True
        },
        "metadata": {
            "source_ip": "192.168.1.100",
            "timestamp": "2024-01-15T10:30:00Z",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    }

    try:
        print("🎣 Simulating phishing attack...")
        print("   Indicators: Suspicious sender, urgent language, fake domains")

        response = requests.post(
            "http://localhost:8001/detect-threat",
            json=phishing_payload,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": "threat-dashboard-key-2024"
            },
            timeout=10
        )

        print(f"📡 Phishing Test Response: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            detection_result = result.get('detection_result', {})

            # Enhanced output with reflective insights
            print(f"🔍 Threat Detected: {detection_result.get('threat_detected', False)}")
            print(
                f"🎯 Confidence: {detection_result.get('final_confidence', detection_result.get('confidence', 0)):.2f}")

            # Show reflective AI insights
            if detection_result.get('reflection_applied'):
                print(f"🧠 Reflective AI: ACTIVE")

                # Show confidence calibration
                if detection_result.get('confidence_calibrated'):
                    print(f"🔄 Confidence Calibrated: Yes")

                # Show adaptation recommendations
                adaptations = detection_result.get('adaptive_actions', [])
                if adaptations:
                    print(f"📈 Recommended Adaptations: {len(adaptations)}")

            # Show threat categories if available
            categories = detection_result.get('threat_categories', [])
            if categories:
                category_names = [cat['category'] for cat in categories]
                print(f"🏷️  Threat Categories: {', '.join(category_names)}")

            # Show response action
            response_action = detection_result.get('recommended_response', {}).get('action', 'Unknown')
            print(f"🛡️  Recommended Action: {response_action}")

            return detection_result
        else:
            print(f"❌ Error: {response.json()}")
            return None

    except Exception as e:
        print(f"❌ Phishing test failed: {e}")
        return None


if __name__ == "__main__":
    result = simulate_phishing_attack()
    if result:
        print(f"\n🎯 Final Result: Threat {'DETECTED' if result.get('threat_detected') else 'NOT DETECTED'}")