# src/threat_detection/simulators/threat_incidents.py
import requests
import json
import random
import time
from datetime import datetime, timedelta


class ThreatIncidentGenerator:
    def __init__(self):
        self.malicious_ips = [
            "185.130.5.231", "45.77.56.124", "192.168.1.666",
            "10.13.37.99", "172.217.168.206", "203.23.186.55"
        ]

        self.suspicious_domains = [
            "paypa1-login.com", "secure-bank-update.com", "amaz0n-security.com",
            "microsoft-billing.com", "apple-verify.net", "faceb00k-login.com"
        ]

        self.malicious_processes = [
            "encrypt_service.exe", "lock_screen.exe", "cryptolocker.exe",
            "keylogger.dll", "backdoor_svc.exe", "miner_process.exe"
        ]

    def generate_ransomware_incident(self):
        """Simulate a ransomware attack"""
        incident = {
            "threat_type": "ransomware",
            "indicators": {
                "file_encryption_patterns": True,
                "suspicious_processes": random.sample(self.malicious_processes, 2),
                "network_connections": [f"{random.choice(self.malicious_ips)}:443"],
                "file_extension_changes": [
                    ".docx -> .locked",
                    ".pdf -> .encrypted",
                    ".jpg -> .crypt",
                    ".xlsx -> .ransom"
                ],
                "ransom_note_present": True,
                "ransom_note_content": "YOUR FILES HAVE BEEN ENCRYPTED! Send 0.5 BTC to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                "rapid_file_changes": random.randint(500, 2000),
                "bitcoin_addresses": ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"],
                "system_modifications": [
                    "Disabled Windows Defender",
                    "Modified registry keys",
                    "Stopped backup services"
                ]
            },
            "metadata": {
                "affected_files": random.randint(1000, 5000),
                "encryption_key": "RSA-2048",
                "ransom_amount": random.uniform(0.3, 2.0),
                "deadline": (datetime.now() + timedelta(hours=72)).isoformat(),
                "attack_vector": "Phishing Email Attachment",
                "impact_level": "Critical"
            }
        }
        return incident

    def generate_ddos_incident(self):
        """Simulate a DDoS attack"""
        source_ips = [f"10.0.1.{i}" for i in range(1, 51)] + [f"192.168.2.{i}" for i in range(1, 31)]

        incident = {
            "threat_type": "ddos",
            "indicators": {
                "request_rate": random.randint(800, 2000),  # requests per second
                "source_ips": random.sample(source_ips, 35),
                "user_agents": [
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                    "Python-urllib/3.8",
                    "Go-http-client/1.1",
                    "Mozilla/5.0 (compatible; mass-scanner/1.0)"
                ],
                "request_types": ["GET", "POST", "HEAD", "OPTIONS"],
                "target_endpoints": ["/api/v1/data", "/login", "/api/users", "/health", "/"],
                "geographic_distribution": "Multiple countries",
                "attack_duration_minutes": random.randint(5, 120),
                "bandwidth_consumption": f"{random.randint(100, 1000)} Mbps"
            },
            "metadata": {
                "attack_type": random.choice(["HTTP Flood", "SYN Flood", "UDP Amplification"]),
                "botnet_size": random.randint(500, 5000),
                "target_service": "Web Application",
                "impact_level": "High"
            }
        }
        return incident

    def generate_data_exfiltration(self):
        """Simulate data exfiltration attempt"""
        incident = {
            "threat_type": "data_exfiltration",
            "indicators": {
                "large_outbound_transfer": True,
                "destination_ip": random.choice(self.malicious_ips),
                "protocol": random.choice(["FTP", "HTTP", "DNS Tunneling"]),
                "data_size": f"{random.randint(50, 500)} MB",
                "suspicious_timing": "After business hours",
                "compressed_data": True,
                "encrypted_transfer": True,
                "sensitive_files": [
                    "customer_database.db",
                    "financial_records.xlsx",
                    "employee_data.csv",
                    "source_code.zip"
                ]
            },
            "metadata": {
                "data_type": "Customer PII",
                "source_user": "svc_backup",
                "exfiltration_method": "Covert channel",
                "impact_level": "Critical"
            }
        }
        return incident

    def generate_insider_threat(self):
        """Simulate insider threat activity"""
        incident = {
            "threat_type": "insider_threat",
            "indicators": {
                "unauthorized_access": True,
                "after_hours_activity": True,
                "access_pattern_change": True,
                "data_download_spike": True,
                "external_device_usage": True,
                "sensitive_file_access": [
                    "salary_information.xlsx",
                    "merger_documents.pdf",
                    "employee_records.db"
                ],
                "failed_access_attempts": random.randint(3, 15)
            },
            "metadata": {
                "user_role": "System Administrator",
                "access_level": "Privileged",
                "suspicious_behavior": "Accessing unrelated departments",
                "risk_level": "High"
            }
        }
        return incident

    def send_threat_incident(self, incident_type=None):
        """Enhanced threat incident detection with reflective AI"""
        if incident_type == "ransomware":
            incident_data = self.generate_ransomware_incident()
        elif incident_type == "ddos":
            incident_data = self.generate_ddos_incident()
        elif incident_type == "data_exfiltration":
            incident_data = self.generate_data_exfiltration()
        elif incident_type == "insider_threat":
            incident_data = self.generate_insider_threat()
        else:
            # Random incident
            incidents = ["ransomware", "ddos", "data_exfiltration", "insider_threat"]
            incident_type = random.choice(incidents)
            incident_data = getattr(self, f"generate_{incident_type}_incident")()

        try:
            print(f"🚨 Generating {incident_type.upper()} incident...")

            response = requests.post(
                "http://localhost:8001/detect-threat",
                json=incident_data,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": "threat-dashboard-key-2024"
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                detection_result = result.get('detection_result', {})
                threat_detected = detection_result.get('threat_detected', False)

                print(f"🔍 Threat Detected: {threat_detected}")

                # Enhanced output with reflective insights
                confidence = detection_result.get('final_confidence', detection_result.get('confidence', 0))
                print(f"🎯 Confidence: {confidence:.2f}")

                # Show reflective AI status
                if detection_result.get('reflection_applied'):
                    print(f"🧠 Reflective AI: ACTIVE")

                    # Show adaptation insights
                    adaptations = detection_result.get('adaptive_actions', [])
                    if adaptations:
                        print(f"📈 Learning Applied: {len(adaptations)} adaptations")

                response_action = detection_result.get('recommended_response', {}).get('action', 'Unknown')
                print(f"🛡️  Action: {response_action}")

                if threat_detected:
                    print("✅ SUCCESS: Threat correctly detected!")
                else:
                    print("❌ FAIL: Threat not detected!")

                return detection_result
            return None

        except Exception as e:
            print(f"❌ Threat test failed: {e}")
            return None


def comprehensive_threat_assessment():
    """Enhanced comprehensive threat assessment with reflective AI analytics"""
    generator = ThreatIncidentGenerator()

    print("🔴 INITIATING COMPREHENSIVE THREAT ASSESSMENT")
    print("🧠 REFLECTIVE AI ANALYTICS ENABLED")
    print("=" * 60)

    threat_types = [
        "ransomware",
        "ddos",
        "data_exfiltration",
        "insider_threat"
    ]

    results = {}
    reflective_usage = 0

    for threat_type in threat_types:
        print(f"\n🎯 Testing {threat_type.upper()} detection...")
        result = generator.send_threat_incident(threat_type)
        results[threat_type] = result

        # Track reflective AI usage
        if result and result.get('reflection_applied'):
            reflective_usage += 1

        time.sleep(2)  # Delay between tests

    # Enhanced assessment summary
    print("\n" + "=" * 60)
    print("📊 ENHANCED THREAT ASSESSMENT SUMMARY")
    print("=" * 60)

    detected_count = 0
    total_confidence = 0
    confidence_count = 0

    for threat_type, result in results.items():
        detected = result and result.get('threat_detected', False)
        status = "✅ DETECTED" if detected else "❌ MISSED"
        detected_count += 1 if detected else 0

        confidence = result.get('final_confidence', result.get('confidence', 0)) if result else 0
        if confidence > 0:
            total_confidence += confidence
            confidence_count += 1

        reflection = "🧠" if result and result.get('reflection_applied') else "  "

        print(f"{threat_type.upper():<20} {reflection} {status} (Confidence: {confidence:.2f})")

    detection_rate = (detected_count / len(threat_types)) * 100
    avg_confidence = (total_confidence / confidence_count) if confidence_count > 0 else 0
    reflective_rate = (reflective_usage / len(threat_types)) * 100

    print(f"\n📈 Performance Metrics:")
    print(f"   🎯 Detection Rate: {detection_rate:.1f}%")
    print(f"   📊 Average Confidence: {avg_confidence:.2f}")
    print(f"   🧠 Reflective AI Usage: {reflective_rate:.1f}%")

    if detection_rate >= 75:
        print("🎉 EXCELLENT: High threat detection capability!")
    elif detection_rate >= 50:
        print("⚠️  MODERATE: Some threats may go undetected!")
    else:
        print("🔴 POOR: Significant security gaps detected!")


if __name__ == "__main__":
    # Test single incident
    generator = ThreatIncidentGenerator()
    generator.send_threat_incident("ransomware")

    # Uncomment for comprehensive test
    # comprehensive_threat_assessment()