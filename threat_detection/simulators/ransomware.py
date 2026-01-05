# src/threat_detection/simulators/ransomware.py
import requests
import json


def simulate_ransomware_attack():
    """Enhanced ransomware simulation with reflective AI insights"""
    ransomware_payload = {
        "threat_type": "ransomware",
        "indicators": {
            "file_encryption_patterns": True,
            "suspicious_processes": ["encrypt_service.exe", "lock_screen.exe"],
            "network_connections": ["185.130.5.231:443", "45.77.56.124:8080"],
            "file_extension_changes": [".txt -> .crypt", ".docx -> .locked", ".jpg -> .encrypted"],
            "ransom_note_present": True,
            "rapid_file_changes": 1500,
            "bitcoin_addresses": ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"]
        }
    }

    try:
        print("💀 Simulating ransomware attack...")
        print("   Indicators: File encryption, ransom note, Bitcoin addresses")

        response = requests.post(
            "http://localhost:8001/detect-threat",
            json=ransomware_payload,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": "threat-dashboard-key-2024"
            },
            timeout=10
        )

        print(f"📡 Ransomware Test Response: {response.status_code}")

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

                # Show reflection insights
                insights = detection_result.get('reflection_insights', {})
                analysis = insights.get('immediate_analysis', {})

                # Show detection quality
                quality = analysis.get('detection_quality', {})
                print(f"📊 Detection Quality: {quality.get('rating', 'N/A')}")

                # Show system impact assessment
                impact = analysis.get('system_impact', {})
                print(f"⚠️  System Impact: {impact.get('risk_level', 'N/A')}")

            # Show response action
            response_action = detection_result.get('recommended_response', {}).get('action', 'Unknown')
            print(f"🛡️  Recommended Action: {response_action}")

            if threat_detected:
                print("✅ SUCCESS: Ransomware correctly detected!")
            else:
                print("❌ FAIL: Ransomware not detected!")

            return detection_result
        else:
            print(f"❌ Error: {response.json()}")
            return None

    except Exception as e:
        print(f"❌ Ransomware test failed: {e}")
        return None


if __name__ == "__main__":
    result = simulate_ransomware_attack()
    if result:
        print(f"\n🎯 Final Result: Threat {'DETECTED' if result.get('threat_detected') else 'NOT DETECTED'}")