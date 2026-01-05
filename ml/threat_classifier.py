# Create src/ml/threat_classifier.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib


class MLThreatClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.features = ['request_rate', 'source_ip_count', 'suspicious_keywords', 'url_length']

    def train_on_historical_data(self, historical_data):
        """Train ML model on historical threat data"""
        X = historical_data[self.features]
        y = historical_data['is_threat']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)

        # Save model
        joblib.dump(self.model, 'models/threat_classifier.pkl')

    def predict_threat(self, features):
        """Predict if features indicate a threat"""
        return self.model.predict_proba([features])[0][1]  # Probability of threat