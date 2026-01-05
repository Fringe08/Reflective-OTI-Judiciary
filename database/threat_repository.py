import sqlite3
from datetime import datetime
import os


class ThreatRepository:
    def __init__(self, db_path='threat_intelligence.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """Create necessary database tables"""
        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS threats
                          (
                              id
                              INTEGER
                              PRIMARY
                              KEY
                              AUTOINCREMENT,
                              threat_type
                              TEXT
                              NOT
                              NULL,
                              severity
                              TEXT
                              NOT
                              NULL,
                              timestamp
                              DATETIME
                              DEFAULT
                              CURRENT_TIMESTAMP,
                              source_ip
                              TEXT,
                              description
                              TEXT,
                              resolved
                              BOOLEAN
                              DEFAULT
                              FALSE,
                              confidence
                              REAL
                              DEFAULT
                              0.0
                          )
                          ''')

        self.conn.execute('''
                          CREATE TABLE IF NOT EXISTS system_metrics
                          (
                              id
                              INTEGER
                              PRIMARY
                              KEY
                              AUTOINCREMENT,
                              metric_name
                              TEXT
                              NOT
                              NULL,
                              metric_value
                              REAL
                              NOT
                              NULL,
                              timestamp
                              DATETIME
                              DEFAULT
                              CURRENT_TIMESTAMP
                          )
                          ''')

        self.conn.commit()

    def log_threat(self, threat_data):
        """Log detected threat to database"""
        try:
            self.conn.execute('''
                              INSERT INTO threats (threat_type, severity, source_ip, description, confidence)
                              VALUES (?, ?, ?, ?, ?)
                              ''', (
                                  threat_data['type'],
                                  threat_data['severity'],
                                  threat_data.get('source_ip', 'Unknown'),
                                  threat_data.get('description', ''),
                                  threat_data.get('confidence', 0.0)
                              ))
            self.conn.commit()
            print("✅ Threat logged to database")
        except Exception as e:
            print(f"❌ Failed to log threat: {e}")

    def get_recent_threats(self, limit=10):
        """Get recent threats from database"""
        try:
            cursor = self.conn.execute('''
                                       SELECT *
                                       FROM threats
                                       ORDER BY timestamp DESC
                                           LIMIT ?
                                       ''', (limit,))

            threats = []
            for row in cursor.fetchall():
                threats.append({
                    'id': row[0],
                    'type': row[1],
                    'severity': row[2],
                    'timestamp': row[3],
                    'source_ip': row[4],
                    'description': row[5],
                    'resolved': bool(row[6]),
                    'confidence': row[7]
                })
            return threats
        except Exception as e:
            print(f"❌ Failed to get recent threats: {e}")
            return []

    def get_threat_statistics(self):
        """Get threat statistics for dashboard"""
        try:
            cursor = self.conn.execute('''
                                       SELECT COUNT(*)                                               as total_threats,
                                              SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END) as critical_threats,
                                              SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END)          as resolved_threats,
                                              AVG(confidence)                                        as avg_confidence
                                       FROM threats
                                       ''')

            stats = cursor.fetchone()
            return {
                'total_threats': stats[0],
                'critical_threats': stats[1],
                'resolved_threats': stats[2],
                'avg_confidence': stats[3] or 0.0
            }
        except Exception as e:
            print(f"❌ Failed to get threat statistics: {e}")
            return {}


# Test the database
if __name__ == "__main__":
    repo = ThreatRepository()

    # Test logging a threat
    repo.log_threat({
        'type': 'Phishing',
        'severity': 'HIGH',
        'source_ip': '192.168.1.100',
        'description': 'Test phishing attempt',
        'confidence': 0.85
    })

    # Get recent threats
    threats = repo.get_recent_threats()
    print("📋 Recent threats:", threats)

    # Get statistics
    stats = repo.get_threat_statistics()
    print("📊 Statistics:", stats)