# src/incident_response/response_engine.py
from datetime import datetime


class IncidentResponseEngine:
    def __init__(self, config):
        self.config = config
        self.incident_log = []

    def execute_response(self, threat_data):
        if threat_data['threat_detected']:
            incident_id = f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            incident_record = {
                'incident_id': incident_id,
                'timestamp': datetime.now().isoformat(),
                'threat_data': threat_data,
                'status': 'open'
            }

            self.incident_log.append(incident_record)

            response_actions = []
            if threat_data['severity_score'] > 0.7:
                response_actions.append(self._alert_security_team(threat_data, incident_id))

            return response_actions
        return []

    def _alert_security_team(self, threat_data, incident_id):
        print(f"🚨 SECURITY ALERT {incident_id}")
        return {'action': 'alert_sent', 'incident_id': incident_id}