import pandas as pd
from datetime import datetime, timedelta
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.application import MIMEApplication


@dataclass
class ThreatReport:
    report_date: str
    summary: Dict
    top_threats: List[Dict]
    response_metrics: Dict
    recommendations: List[str]
    compliance_status: Dict


class ThreatReporter:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)

        # Compliance thresholds
        self.compliance_thresholds = {
            'gdpr': {
                'data_breach_time': 72,  # hours to report breach
                'encryption_required': True,
                'access_logs_days': 90
            },
            'hipaa': {
                'access_controls': True,
                'audit_trails': True,
                'data_encryption': True
            },
            'pci_dss': {
                'firewall_configured': True,
                'data_encrypted': True,
                'vulnerability_scans': True
            }
        }

    def generate_daily_report(self, report_date=None):
        """Generate daily threat intelligence report"""
        if not report_date:
            report_date = datetime.now().strftime("%Y-%m-%d")

        print(f"📊 Generating daily threat report for {report_date}...")

        threats_today = self.get_todays_threats(report_date)

        report_data = ThreatReport(
            report_date=report_date,
            summary=self.generate_summary(threats_today),
            top_threats=self.get_top_threats(threats_today),
            response_metrics=self.calculate_response_metrics(threats_today),
            recommendations=self.generate_recommendations(threats_today),
            compliance_status=self.generate_compliance_report()
        )

        report = self.format_report(report_data)

        # Save report
        self.save_report(report, report_date)

        return report

    def get_todays_threats(self, report_date):
        """Get threats for the specified date"""
        # If we have database connection, use it
        if self.db_connection:
            return self.get_threats_from_db(report_date)
        else:
            # Generate sample data for demonstration
            return self.generate_sample_threats(report_date)

    def get_threats_from_db(self, report_date):
        """Get threats from database"""
        try:
            # This would be your actual database query
            query = """
                    SELECT * \
                    FROM threats
                    WHERE DATE (timestamp) = ?
                    ORDER BY timestamp DESC \
                    """
            # cursor = self.db_connection.execute(query, (report_date,))
            # return cursor.fetchall()

            # For now, return sample data
            return self.generate_sample_threats(report_date)
        except Exception as e:
            print(f"❌ Database query failed: {e}")
            return self.generate_sample_threats(report_date)

    def generate_sample_threats(self, report_date):
        """Generate sample threat data for demonstration"""
        threat_types = ['Phishing', 'Ransomware', 'DDoS', 'Malware', 'Data Exfiltration', 'Insider Threat']
        severities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

        threats = []
        for i in range(15):
            threat_type = threat_types[i % len(threat_types)]
            severity = severities[i % len(severities)]

            threats.append({
                'id': f"THREAT-{1000 + i}",
                'type': threat_type,
                'severity': severity,
                'timestamp': f"{report_date} {10 + i % 10}:{i % 60:02d}:00",
                'source_ip': f"192.168.1.{i + 1}",
                'description': f"{threat_type} attempt detected",
                'confidence': round(0.7 + (i * 0.02), 2),
                'status': 'RESOLVED' if i % 3 == 0 else 'ACTIVE',
                'response_time': 120 + (i * 30)  # seconds
            })

        return threats

    def generate_summary(self, threats):
        """Generate summary statistics"""
        total_threats = len(threats)
        critical_threats = sum(1 for t in threats if t['severity'] == 'CRITICAL')
        high_threats = sum(1 for t in threats if t['severity'] == 'HIGH')
        resolved_threats = sum(1 for t in threats if t['status'] == 'RESOLVED')

        # Threat type distribution
        threat_types = {}
        for threat in threats:
            threat_type = threat['type']
            threat_types[threat_type] = threat_types.get(threat_type, 0) + 1

        avg_confidence = sum(t['confidence'] for t in threats) / total_threats if total_threats > 0 else 0
        avg_response_time = sum(t.get('response_time', 0) for t in threats) / total_threats if total_threats > 0 else 0

        return {
            'total_threats': total_threats,
            'critical_threats': critical_threats,
            'high_threats': high_threats,
            'resolved_threats': resolved_threats,
            'resolution_rate': (resolved_threats / total_threats * 100) if total_threats > 0 else 0,
            'threat_type_distribution': threat_types,
            'average_confidence': round(avg_confidence, 2),
            'average_response_time_seconds': round(avg_response_time, 2),
            'threat_trend': self.calculate_threat_trend(threats)
        }

    def calculate_threat_trend(self, threats):
        """Calculate threat trend compared to previous period"""
        # In a real implementation, you'd compare with historical data
        threat_count = len(threats)

        if threat_count < 5:
            return "LOW_ACTIVITY"
        elif threat_count < 15:
            return "NORMAL_ACTIVITY"
        else:
            return "HIGH_ACTIVITY"

    def get_top_threats(self, threats, limit=5):
        """Get top threats by severity and confidence"""
        # Sort by severity (critical first) and then by confidence
        severity_order = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}

        sorted_threats = sorted(
            threats,
            key=lambda x: (severity_order.get(x['severity'], 0), x['confidence']),
            reverse=True
        )

        return sorted_threats[:limit]

    def calculate_response_metrics(self, threats):
        """Calculate response performance metrics"""
        if not threats:
            return {
                'avg_response_time': 0,
                'response_efficiency': 'N/A',
                'escalation_rate': 0,
                'auto_containment_rate': 0
            }

        response_times = [t.get('response_time', 0) for t in threats if t.get('response_time')]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        critical_threats = [t for t in threats if t['severity'] in ['CRITICAL', 'HIGH']]
        escalation_rate = (len(critical_threats) / len(threats)) * 100 if threats else 0

        auto_contained = sum(1 for t in threats if t.get('auto_contained', False))
        auto_containment_rate = (auto_contained / len(threats)) * 100 if threats else 0

        # Response efficiency rating
        if avg_response_time < 60:
            efficiency = 'EXCELLENT'
        elif avg_response_time < 180:
            efficiency = 'GOOD'
        elif avg_response_time < 300:
            efficiency = 'FAIR'
        else:
            efficiency = 'POOR'

        return {
            'avg_response_time_seconds': round(avg_response_time, 2),
            'response_efficiency': efficiency,
            'escalation_rate_percent': round(escalation_rate, 2),
            'auto_containment_rate_percent': round(auto_containment_rate, 2),
            'threats_requiring_manual_intervention': len([t for t in threats if not t.get('auto_contained', False)])
        }

    def generate_recommendations(self, threats):
        """Generate security recommendations based on threat analysis"""
        recommendations = []
        summary = self.generate_summary(threats)

        # Recommendation based on threat volume
        if summary['total_threats'] > 20:
            recommendations.append(
                "🚨 High threat volume detected. Consider increasing monitoring and conducting security awareness training.")
        elif summary['total_threats'] < 5:
            recommendations.append(
                "✅ Low threat activity. Maintain current security posture and continue regular monitoring.")

        # Recommendation based on threat types
        threat_distribution = summary['threat_type_distribution']
        if threat_distribution.get('Phishing', 0) > 5:
            recommendations.append(
                "📧 High phishing activity detected. Enhance email filtering and conduct phishing simulation exercises.")

        if threat_distribution.get('Ransomware', 0) > 0:
            recommendations.append(
                "💀 Ransomware threats detected. Verify backup systems and update endpoint protection.")

        if threat_distribution.get('DDoS', 0) > 0:
            recommendations.append("🌐 DDoS attacks detected. Review DDoS mitigation services and network capacity.")

        # Recommendation based on response time
        response_metrics = self.calculate_response_metrics(threats)
        if response_metrics['response_efficiency'] in ['FAIR', 'POOR']:
            recommendations.append(
                "⏱️ Response times need improvement. Review incident response procedures and consider automation.")

        # General recommendations
        recommendations.extend([
            "🛡️ Ensure all systems are patched with latest security updates",
            "🔍 Conduct regular vulnerability assessments",
            "📚 Review and update incident response playbooks",
            "👥 Schedule security awareness training for staff"
        ])

        return recommendations

    def generate_compliance_report(self):
        """Generate compliance reports for regulations"""
        return {
            'gdpr_compliance': self.check_gdpr_compliance(),
            'hipaa_compliance': self.check_hipaa_compliance(),
            'pci_dss_compliance': self.check_pci_compliance(),
            'overall_compliance_score': self.calculate_overall_compliance()
        }

    def check_gdpr_compliance(self):
        """Check GDPR compliance status"""
        # Simulate compliance checks
        checks = {
            'data_breach_reporting': True,  # Would check actual breach reporting times
            'data_encryption': True,
            'access_logs_maintained': True,
            'data_processing_records': True,
            'user_consent_mechanisms': True
        }

        compliance_score = (sum(checks.values()) / len(checks)) * 100

        return {
            'compliant': compliance_score >= 80,
            'score': round(compliance_score, 2),
            'checks': checks,
            'recommendations': [
                "Ensure data breach reporting within 72 hours",
                "Maintain records of data processing activities",
                "Implement data protection by design"
            ] if compliance_score < 100 else ["GDPR compliance maintained"]
        }

    def check_hipaa_compliance(self):
        """Check HIPAA compliance status"""
        checks = {
            'access_controls': True,
            'audit_controls': True,
            'integrity_controls': True,
            'transmission_security': True,
            'workforce_security': True
        }

        compliance_score = (sum(checks.values()) / len(checks)) * 100

        return {
            'compliant': compliance_score >= 85,
            'score': round(compliance_score, 2),
            'checks': checks,
            'recommendations': [
                "Conduct regular risk assessments",
                "Implement encryption for PHI at rest and in transit",
                "Maintain audit logs for 6 years"
            ] if compliance_score < 100 else ["HIPAA compliance maintained"]
        }

    def check_pci_compliance(self):
        """Check PCI DSS compliance status"""
        checks = {
            'firewall_configuration': True,
            'data_encryption': True,
            'vulnerability_management': True,
            'access_control_measures': True,
            'security_monitoring': True,
            'security_policies': True
        }

        compliance_score = (sum(checks.values()) / len(checks)) * 100

        return {
            'compliant': compliance_score >= 80,
            'score': round(compliance_score, 2),
            'checks': checks,
            'recommendations': [
                "Perform quarterly vulnerability scans",
                "Maintain firewall configuration standards",
                "Restrict access to cardholder data"
            ] if compliance_score < 100 else ["PCI DSS compliance maintained"]
        }

    def calculate_overall_compliance(self):
        """Calculate overall compliance score"""
        gdpr = self.check_gdpr_compliance()
        hipaa = self.check_hipaa_compliance()
        pci = self.check_pci_compliance()

        scores = [gdpr['score'], hipaa['score'], pci['score']]
        return round(sum(scores) / len(scores), 2)

    def format_report(self, report_data: ThreatReport):
        """Format the report for display and export"""
        formatted_report = {
            'metadata': {
                'report_id': f"THREAT-REPORT-{report_data.report_date}",
                'generated_at': datetime.now().isoformat(),
                'report_period': report_data.report_date
            },
            'executive_summary': self.create_executive_summary(report_data),
            'detailed_analysis': {
                'threat_summary': report_data.summary,
                'top_threats': report_data.top_threats,
                'response_metrics': report_data.response_metrics
            },
            'compliance_status': report_data.compliance_status,
            'recommendations': report_data.recommendations,
            'action_items': self.generate_action_items(report_data)
        }

        return formatted_report

    def create_executive_summary(self, report_data: ThreatReport):
        """Create executive summary for management"""
        summary = report_data.summary
        compliance = report_data.compliance_status

        return {
            'overview': f"On {report_data.report_date}, the system detected {summary['total_threats']} security threats.",
            'key_findings': [
                f"{summary['critical_threats']} critical threats requiring immediate attention",
                f"Overall threat trend: {summary['threat_trend'].replace('_', ' ').title()}",
                f"Response efficiency: {report_data.response_metrics['response_efficiency']}",
                f"Compliance score: {compliance['overall_compliance_score']}%"
            ],
            'risk_level': self.calculate_risk_level(summary),
            'priority_actions': report_data.recommendations[:3]  # Top 3 recommendations
        }

    def calculate_risk_level(self, summary):
        """Calculate overall risk level"""
        if summary['critical_threats'] > 3 or summary['total_threats'] > 25:
            return "HIGH"
        elif summary['critical_threats'] > 0 or summary['total_threats'] > 10:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_action_items(self, report_data: ThreatReport):
        """Generate actionable items from the report"""
        action_items = []

        # Based on threat severity
        if report_data.summary['critical_threats'] > 0:
            action_items.append("🔴 IMMEDIATE: Review and respond to critical threats")

        # Based on response metrics
        if report_data.response_metrics['response_efficiency'] in ['FAIR', 'POOR']:
            action_items.append("🟡 PRIORITY: Optimize incident response procedures")

        # Based on compliance
        compliance = report_data.compliance_status
        if compliance['overall_compliance_score'] < 80:
            action_items.append("🟡 PRIORITY: Address compliance gaps")

        # General actions
        action_items.extend([
            "🟢 ONGOING: Monitor threat intelligence feeds",
            "🟢 ONGOING: Update security controls based on recommendations",
            "🟢 SCHEDULED: Conduct security awareness training"
        ])

        return action_items

    def save_report(self, report, report_date):
        """Save report to file"""
        filename = f"threat_report_{report_date}.json"
        filepath = os.path.join(self.reports_dir, filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"✅ Report saved to: {filepath}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")

    def export_report_html(self, report, report_date):
        """Export report as HTML format"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Threat Intelligence Report - {report_date}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; background: #f8f9fa; }}
                .critical {{ border-left-color: #e74c3c; }}
                .warning {{ border-left-color: #f39c12; }}
                .success {{ border-left-color: #27ae60; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #34495e; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛡️ Threat Intelligence Report</h1>
                <h2>Date: {report_date}</h2>
            </div>

            <div class="section">
                <h3>Executive Summary</h3>
                <p>{report['executive_summary']['overview']}</p>
                <ul>
                    {''.join(f'<li>{item}</li>' for item in report['executive_summary']['key_findings'])}
                </ul>
                <p><strong>Risk Level:</strong> {report['executive_summary']['risk_level']}</p>
            </div>

            <div class="section">
                <h3>Top Threats</h3>
                <table>
                    <tr><th>ID</th><th>Type</th><th>Severity</th><th>Confidence</th><th>Description</th></tr>
                    {''.join(f'<tr><td>{t["id"]}</td><td>{t["type"]}</td><td>{t["severity"]}</td><td>{t["confidence"]}</td><td>{t["description"]}</td></tr>'
                             for t in report['detailed_analysis']['top_threats'])}
                </table>
            </div>

            <div class="section">
                <h3>Recommendations</h3>
                <ul>
                    {''.join(f'<li>{rec}</li>' for rec in report['recommendations'])}
                </ul>
            </div>
        </body>
        </html>
        """

        filename = f"threat_report_{report_date}.html"
        filepath = os.path.join(self.reports_dir, filename)

        try:
            with open(filepath, 'w') as f:
                f.write(html_content)
            print(f"✅ HTML report saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Failed to save HTML report: {e}")
            return None

    def send_report_email(self, report, recipients, report_date):
        """Send report via email"""
        try:
            # This is a template - implement with your email service
            html_file = self.export_report_html(report, report_date)

            if html_file:
                print(f"📧 Report would be emailed to: {', '.join(recipients)}")
                print(f"📎 Attachment: {html_file}")
                # Actual email implementation would go here
                # using smtplib, etc.
            else:
                print("❌ Cannot send email: HTML report generation failed")

        except Exception as e:
            print(f"❌ Email sending failed: {e}")


# Test the threat reporter
if __name__ == "__main__":
    reporter = ThreatReporter()

    # Generate daily report
    print("🚀 Generating comprehensive threat report...")
    report = reporter.generate_daily_report()

    # Print summary
    print("\n" + "=" * 60)
    print("📊 THREAT REPORT SUMMARY")
    print("=" * 60)

    executive_summary = report['executive_summary']
    print(f"Overview: {executive_summary['overview']}")
    print(f"Risk Level: {executive_summary['risk_level']}")
    print("\nKey Findings:")
    for finding in executive_summary['key_findings']:
        print(f"  • {finding}")

    print(f"\nCompliance Score: {report['compliance_status']['overall_compliance_score']}%")

    print(f"\nTop {len(report['detailed_analysis']['top_threats'])} Threats:")
    for threat in report['detailed_analysis']['top_threats']:
        print(f"  • {threat['type']} ({threat['severity']}) - Confidence: {threat['confidence']}")

    print(f"\nRecommendations ({len(report['recommendations'])}):")
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"  {i}. {rec}")

    # Export HTML version
    html_path = reporter.export_report_html(report, report['metadata']['report_period'])
    if html_path:
        print(f"\n✅ HTML report exported: {html_path}")

    print("\n🎯 Threat reporting system ready!")