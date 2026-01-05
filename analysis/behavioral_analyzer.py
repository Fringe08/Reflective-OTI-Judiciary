import numpy as np
from datetime import datetime, time


class BehavioralAnalyzer:
    def __init__(self):
        self.normal_baseline = {
            'working_hours_start': time(8, 0),  # 8 AM
            'working_hours_end': time(18, 0),  # 6 PM
            'max_download_size': 100,  # 100 MB
            'normal_access_patterns': ['HR', 'IT', 'Finance']  # Normal departments
        }

    def analyze_user_behavior(self, user_actions):
        """Detect anomalous user behavior"""
        anomalies = []

        # Check for after-hours access
        if self.is_after_hours_access(user_actions):
            anomalies.append('after_hours_access')

        # Check for mass downloads
        if self.is_mass_download(user_actions):
            anomalies.append('mass_download')

        # Check for unauthorized department access
        if self.has_unauthorized_access(user_actions):
            anomalies.append('unauthorized_department_access')

        return anomalies

    def is_after_hours_access(self, user_actions):
        """Check if access occurs outside working hours"""
        for action in user_actions:
            action_time = action.get('timestamp', datetime.now()).time()
            if not (self.normal_baseline['working_hours_start'] <= action_time <= self.normal_baseline[
                'working_hours_end']):
                return True
        return False

    def is_mass_download(self, user_actions):
        """Check for unusually large downloads"""
        total_download_size = sum(action.get('download_size', 0) for action in user_actions)
        return total_download_size > self.normal_baseline['max_download_size']

    def has_unauthorized_access(self, user_actions):
        """Check for access to unauthorized departments"""
        for action in user_actions:
            department = action.get('department', '')
            if department and department not in self.normal_baseline['normal_access_patterns']:
                return True
        return False

    def detect_insider_threats(self, user_actions):
        """Identify potential insider threats"""
        anomalies = self.analyze_user_behavior(user_actions)

        threat_level = 'LOW'
        if len(anomalies) >= 2:
            threat_level = 'HIGH'
        elif len(anomalies) == 1:
            threat_level = 'MEDIUM'

        return {
            'threat_level': threat_level,
            'anomalies_detected': anomalies,
            'recommended_action': self.get_recommended_action(threat_level)
        }

    def get_recommended_action(self, threat_level):
        """Get recommended action based on threat level"""
        actions = {
            'LOW': 'Monitor user activity',
            'MEDIUM': 'Review user permissions and alert manager',
            'HIGH': 'Immediately restrict access and initiate investigation'
        }
        return actions.get(threat_level, 'Monitor')


# Test the behavioral analyzer
if __name__ == "__main__":
    analyzer = BehavioralAnalyzer()

    # Test data
    test_actions = [
        {'timestamp': datetime(2024, 1, 15, 22, 0), 'download_size': 50, 'department': 'HR'},  # After hours
        {'timestamp': datetime(2024, 1, 15, 14, 0), 'download_size': 80, 'department': 'R&D'}  # Unauthorized dept
    ]

    threat_assessment = analyzer.detect_insider_threats(test_actions)
    print("🔍 Behavioral Analysis Results:")
    print(f"Threat Level: {threat_assessment['threat_level']}")
    print(f"Anomalies: {threat_assessment['anomalies_detected']}")
    print(f"Action: {threat_assessment['recommended_action']}")