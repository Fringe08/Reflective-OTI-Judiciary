import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import logging


class AlertSystem:
    def __init__(self):
        self.alert_rules = self.load_alert_rules()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging for alert system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('alerts.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def load_alert_rules(self):
        """Load alert rules configuration"""
        return {
            'CRITICAL': ['sms', 'email', 'incident_response'],
            'HIGH': ['email', 'dashboard_alert'],
            'MEDIUM': ['dashboard_alert'],
            'LOW': ['log_only']
        }

    def send_alert(self, threat_data):
        """Send alerts based on threat severity"""
        severity = threat_data.get('severity', 'LOW').upper()
        alert_methods = self.alert_rules.get(severity, ['log_only'])

        self.logger.info(f"🚨 Alert triggered: {threat_data['type']} - Severity: {severity}")

        for method in alert_methods:
            try:
                if method == 'email':
                    self.send_email_alert(threat_data)
                elif method == 'sms':
                    self.send_sms_alert(threat_data)
                elif method == 'incident_response':
                    self.trigger_incident_response(threat_data)
                elif method == 'dashboard_alert':
                    self.create_dashboard_alert(threat_data)
                elif method == 'log_only':
                    self.log_threat(threat_data)
            except Exception as e:
                self.logger.error(f"Failed to send {method} alert: {e}")

    def send_email_alert(self, threat_data):
        """Send email alert to security team"""
        # This is a simulation - implement with real email service
        subject = f"🚨 THREAT ALERT: {threat_data['type']}"
        body = f"""
        Threat Detection System Alert:

        Type: {threat_data['type']}
        Severity: {threat_data['severity']}
        Timestamp: {threat_data.get('timestamp', 'Unknown')}
        Source: {threat_data.get('source_ip', 'Unknown')}
        Description: {threat_data.get('description', 'No description')}

        Recommended Action: {threat_data.get('recommended_action', 'Investigate immediately')}
        """

        self.logger.info(f"📧 Email alert prepared: {subject}")
        # Implementation for real email would go here
        # smtplib.SMTP() etc.

    def send_sms_alert(self, threat_data):
        """Send SMS alert (simulation)"""
        message = f"ALERT: {threat_data['type']} - {threat_data['severity']}"
        self.logger.info(f"📱 SMS alert: {message}")
        # Integrate with Twilio or similar service

    def trigger_incident_response(self, threat_data):
        """Trigger automated incident response"""
        self.logger.info(f"🛡️ Incident response triggered for: {threat_data['type']}")
        # This would integrate with your response system

    def create_dashboard_alert(self, threat_data):
        """Create alert in dashboard"""
        self.logger.info(f"📊 Dashboard alert created: {threat_data['type']}")

    def log_threat(self, threat_data):
        """Log threat for later review"""
        self.logger.info(f"📝 Threat logged: {threat_data}")


# Test the alert system
if __name__ == "__main__":
    alert_system = AlertSystem()

    test_threat = {
        'type': 'Ransomware',
        'severity': 'CRITICAL',
        'timestamp': '2024-01-15 10:30:00',
        'source_ip': '192.168.1.100',
        'description': 'File encryption detected',
        'recommended_action': 'Isolate machine immediately'
    }

    alert_system.send_alert(test_threat)