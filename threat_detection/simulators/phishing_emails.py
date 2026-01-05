# src/threat_detection/simulators/phishing_emails.py
import requests
import json


def simulate_phishing_attack():
    """Enhanced phishing email simulation with reflective AI"""
    phishing_payload = {
        "threat_type": "phishing",
        "indicators": {
            "suspicious_sender": "security@paypa1.com",
            "urgent_language": True,
            "contains_links": True,
            "suspicious_domains": ["paypa1-login.com", "secure-bank-update.com"],
            "attachments_present": True,
            "grammar_errors": True
        },
        "metadata": {
            "source_ip": "192.168.1.100",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    }

    try:
        print("📧 Simulating phishing email attack...")
        print("   Characteristics: Fake sender, urgent language, malicious links")

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
            threat_detected = detection_result.get('threat_detected', False)
            print(f"🔍 Threat Detected: {threat_detected}")

            confidence = detection_result.get('final_confidence', detection_result.get('confidence', 0))
            print(f"🎯 Confidence: {confidence:.2f}")

            # Show reflective AI insights
            if detection_result.get('reflection_applied'):
                print(f"🧠 Reflective AI: ACTIVE")

                # Show confidence calibration
                if detection_result.get('confidence_calibrated'):
                    original_conf = detection_result.get('original_confidence', 0)
                    print(f"🔄 Confidence Calibrated: {original_conf:.2f} → {confidence:.2f}")

                # Show pattern recognition
                insights = detection_result.get('reflection_insights', {})
                patterns = insights.get('pattern_recognition', [])
                if patterns:
                    print(f"📊 Pattern Analysis: {len(patterns)} insights generated")

            # Show response action
            response_action = detection_result.get('recommended_response', {}).get('action', 'Unknown')
            print(f"🛡️  Recommended Action: {response_action}")

            if threat_detected:
                print("✅ SUCCESS: Phishing email correctly detected!")
            else:
                print("❌ FAIL: Phishing email not detected!")

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
        print(f"\n🎯 Final Result: Phishing {'DETECTED' if result.get('threat_detected') else 'NOT DETECTED'}")