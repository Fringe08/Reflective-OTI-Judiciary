# src/data_processing/data_processor.py
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder


class ThreatDataProcessor:
    def __init__(self, config):
        self.config = config
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def generate_sample_data(self, n_samples=1000):
        """Generate sample training data"""
        features = np.random.randn(n_samples, 50)
        labels = np.random.choice(
            list(self.config.THREAT_CATEGORIES.keys()),
            size=n_samples
        )
        return features, labels

    def preprocess_data(self, features, labels):
        features_scaled = self.scaler.fit_transform(features)
        labels_encoded = self.label_encoder.fit_transform(labels)
        return features_scaled, labels_encoded