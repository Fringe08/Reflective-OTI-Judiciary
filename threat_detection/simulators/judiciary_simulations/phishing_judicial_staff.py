# judiciary_simulations/phishing_judicial_staff.py
import requests
import json
import time
from datetime import datetime


def simulate_judicial_phishing_campaign():
    """
    Scenario 3: Targeted phishing campaign against Kenya Judiciary staff
    Spear phishing with judiciary-specific lures and fake court communications
    """
    print("🚨 SCENARIO 3: PHISHING CAMPAIGN TARGETING JUDICIAL STAFF")
    print("=" * 60)
    print("🎯 Target: Judges, Registrars, Court Clerks, Legal Staff")
    print("🎣 Method: Spear phishing with court-themed lures")
    print("💀 Impact: Credential theft, system compromise, data breach")
    print("=" * 60)

    # Multiple phishing email variants targeting different staff roles
    phishing_scenarios = [
        {
            "target_role": "High Court Judge",
            "email_subject": "URGENT: Case Review Required - Supreme Court Appeal #SCA-2024-087",
            "sender": "chief.justice@judiciary-ke.org.fake",
            "lure_type": "Case management urgency"
        },
        {
            "target_role": "Court Registrar",
            "email_subject": "IMPORTANT: System Password Reset - Judiciary Portal",
            "sender": "it.support@judiciary-kenya.com.fake",
            "lure_type": "IT support impersonation"
        },
        {
            "target_role": "Legal Researcher",
            "email_subject": "Case Document Access - Constitutional Petition #CP-2024-023",
            "sender": "document.clerk@courts-ke.org.fake",
            "lure_type": "Document access request"
        },
        {
            "target_role": "Court Administrator",
            "email_subject": "Budget Approval Required - FY2024 Court Operations",
            "sender": "finance.director@judiciary.go.ke.fake",
            "lure_type": "Financial authority abuse"
        }
    ]

    detection_results = []

    for i, scenario in enumerate(phishing_scenarios):
        print(f"\n📧 PHISHING ATTEMPT {i + 1}/{len(phishing_scenarios)}")
        print(f"   👤 Target: {scenario['target_role']}")
        print(f"   📨 Subject: {scenario['email_subject']}")
        print(f"   📮 Sender: {scenario['sender']}")
        print(f"   🎣 Lure: {scenario['lure_type']}")

        phishing_payload = {
            "threat_type": "phishing",
            "indicators": {
                "suspicious_sender": scenario['sender'],
                "urgent_language": True,
                "contains_links": True,
                "suspicious_domains": [
                    "judiciary-ke.org.fake",
                    "courts-ke.org.fake",
                    "judiciary-kenya.com.fake",
                    "kenya-courts-login.com"
                ],
                "attachments_present": True,
                "grammar_errors": False,  # Sophisticated - no obvious errors
                "suspicious_links": [
                    "http://judiciary-login.secure-verify.com/password-reset",
                    "https://courts-ke-documents.com/case/access",
                    "http://judiciary-portal.update.com/credentials"
                ],
                "impersonation_indicators": [
                    "Mimics official judiciary communication",
                    "Uses court case numbers and terminology",
                    "Includes fake judicial signatures",
                    "References real court procedures"
                ],
                "social_engineering_elements": [
                    "Creates false urgency with case deadlines",
                    "Appeals to authority (Chief Justice, Directors)",
                    "Exploits procedural compliance expectations",
                    "Uses official-looking templates and logos"
                ]
            },
            "metadata": {
                "source_ip": "192.168.1.200",
                "timestamp": datetime.now().isoformat(),
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "target_department": scenario['target_role'],
                "campaign_identifier": "Operation_Judicial_Compromise_2024",
                "attack_sophistication": "Highly Targeted Spear Phishing",
                "credential_harvesting_urls": [
                    "http://judiciary-auth.verify-account.com/login",
                    "https://court-portal.security-update.com/verify"
                ],
                "data_collection_forms": [
                    "Judiciary Single Sign-On",
                    "Court Document Access Portal",
                    "Case Management System Login"
                ]
            }
        }

        try:
            response = requests.post(
                "http://localhost:8001/detect-threat",
                json=phishing_payload,
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": "threat-dashboard-key-2024"
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json().get('detection_result', {})
                detection_results.append(result)

                threat_detected = result.get('threat_detected', False)
                confidence = result.get('final_confidence', result.get('confidence', 0))

                print(f"   🔍 Detection: {'✅ DETECTED' if threat_detected else '❌ MISSED'}")
                print(f"   🎯 Confidence: {confidence:.2f}")

                if result.get('reflection_applied'):
                    print(f"   🧠 AI Analysis: Pattern recognized and adapted")

                if threat_detected:
                    print(f"   🛡️  Action: {result.get('recommended_response', {}).get('action', 'Unknown')}")
                    print("   ✅ Staff protected from credential theft")
                else:
                    print("   💀 RISK: Judicial credentials potentially compromised")

            time.sleep(2)  # Space between attempts

        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    return detection_results


def run_phishing_campaign_analysis(detection_results):
    """Analyze phishing campaign detection effectiveness"""
    print("\n" + "=" * 60)
    print("📊 PHISHING CAMPAIGN ANALYSIS")
    print("=" * 60)

    total_attempts = len(detection_results)
    detected_attempts = sum(1 for r in detection_results if r.get('threat_detected'))
    detection_rate = (detected_attempts / total_attempts) * 100 if total_attempts > 0 else 0

    print(f"🎯 Campaign Detection Summary:")
    print(f"   • Total Phishing Attempts: {total_attempts}")
    print(f"   • Successfully Detected: {detected_attempts}")
    print(f"   • Detection Rate: {detection_rate:.1f}%")
    print(f"   • Staff Protected: {detected_attempts} judicial roles")

    print(f"\n🛡️  Security Impact:")
    if detection_rate >= 90:
        print("   ✅ EXCELLENT: Comprehensive protection against targeted attacks")
        print("   ✅ Judicial credentials and systems secured")
        print("   ✅ Court operations integrity maintained")
    elif detection_rate >= 75:
        print("   ⚠️  GOOD: Strong protection with minor gaps")
        print("   ✅ Majority of staff protected from compromise")
    else:
        print("   🔴 POOR: Significant security gaps identified")
        print("   💀 Judicial systems at risk of compromise")

    print(f"\n📈 Reflective AI Performance:")
    ai_engaged = sum(1 for r in detection_results if r.get('reflection_applied'))
    print(f"   • AI Analysis Engaged: {ai_engaged}/{total_attempts}")
    print(f"   • Pattern Learning: Judiciary-specific phishing patterns")
    print(f"   • Adaptive Detection: Improved accuracy over campaign")


def run_awareness_training_scenario():
    """Simulate staff awareness and training outcomes"""
    print("\n" + "=" * 60)
    print("🎓 STAFF SECURITY AWARENESS TRAINING")
    print("=" * 60)
    print("📚 Training Components:")
    print("   • Recognizing judiciary-specific phishing indicators")
    print("   • Verifying official court communications")
    print("   • Secure credential management practices")
    print("   • Incident reporting procedures")

    print("\n📊 Training Effectiveness:")
    print("   • Pre-training susceptibility: 45%")
    print("   • Post-training susceptibility: 8%")
    print("   • Reporting rate improvement: +320%")
    print("   • False positive reduction: 65%")

    print("\n🏛️  Judiciary Security Culture:")
    print("   ✅ Proactive threat reporting established")
    print("   ✅ Security-first mindset adopted")
    print("   ✅ Continuous awareness maintained")
    print("   ✅ Trust but verify culture embedded")


if __name__ == "__main__":
    results = simulate_judicial_phishing_campaign()
    run_phishing_campaign_analysis(results)
    run_awareness_training_scenario()