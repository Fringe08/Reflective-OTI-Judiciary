# src/threat_detection/detection_engine.py
import numpy as np
from datetime import datetime
from typing import Dict, Any
import sys
import os

# Import the reflective model
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from src.threat_detection.enhanced_detector import enhanced_detector

    # Check if the required method exists
    if hasattr(enhanced_detector, 'detect_threat_with_reflection'):
        REFLECTIVE_AI_AVAILABLE = True
    else:
        REFLECTIVE_AI_AVAILABLE = False
        print("⚠️  Reflective AI module found but missing required method")

except ImportError as e:
    REFLECTIVE_AI_AVAILABLE = False
    print(f"⚠️  Reflective AI module not available: {e}")


class ThreatDetectionEngine:
    def __init__(self, model, config, data_processor):
        self.model = model
        self.config = config
        self.data_processor = data_processor
        self.threat_history = []
        self.reflective_enabled = REFLECTIVE_AI_AVAILABLE

        # Create a safe fallback method if reflective AI is not available
        if not self.reflective_enabled:
            self._create_fallback_methods()

        print(
            f"🎯 Threat Detection Engine Initialized - Reflective AI: {'ENABLED' if self.reflective_enabled else 'DISABLED'}")

    def _create_fallback_methods(self):
        """Create fallback methods when reflective AI is not available"""

        def fallback_detect_threat_with_reflection(threat_data):
            """Fallback method when reflective AI is not available"""
            # Just return basic threat data without reflection
            return {
                'threat_type': threat_data.get('threat_type', 'unknown'),
                'severity': threat_data.get('severity', 'low'),
                'confidence': threat_data.get('confidence', 0.5),
                'reflection_insights': {'status': 'fallback_mode', 'message': 'Reflective AI unavailable'},
                'model_adaptation': {'status': 'none'},
                'confidence_calibrated': False,
                'adaptation_recommendations': []
            }

        def fallback_get_detector_status():
            """Fallback status method"""
            return {
                'status': 'fallback_mode',
                'model_insights': {
                    'model_version': '1.0.0-fallback',
                    'recent_adaptations': [],
                    'total_learning_cycles': 0
                },
                'adaptive_learning_cycles': 0,
                'fallback_message': 'Reflective AI module not available'
            }

        # Create a mock enhanced_detector object
        class MockEnhancedDetector:
            def detect_threat_with_reflection(self, threat_data):
                return fallback_detect_threat_with_reflection(threat_data)

            def get_detector_status(self):
                return fallback_get_detector_status()

        # Make the mock available globally
        global enhanced_detector
        enhanced_detector = MockEnhancedDetector()
        self.reflective_enabled = True  # Enable with fallback

    def detect_threat(self, features):
        """Enhanced threat detection with reflective AI capabilities"""
        # Original detection logic
        processed_features = self.data_processor.scaler.transform([features])
        predictions = self.model.predict(processed_features, verbose=0)
        threat_detection, threat_severity, response_recommendation = predictions

        # Original threat result
        threat_result = {
            'timestamp': datetime.now().isoformat(),
            'threat_detected': np.any(threat_detection > 0.5),
            'threat_categories': self._interpret_threat_categories(threat_detection),
            'severity_score': float(threat_severity[0][0]),
            'recommended_response': self._interpret_response(response_recommendation),
            'original_confidence': float(np.max(threat_detection)),
            'processing_time': datetime.now().isoformat(),
            'detection_method': 'ml_model'
        }

        # Enhance with reflective AI if available
        if self.reflective_enabled:
            threat_result = self._enhance_with_reflective_ai(threat_result, features)

        self.threat_history.append(threat_result)
        return threat_result

    def _enhance_with_reflective_ai(self, threat_result: Dict, features) -> Dict:
        """Enhance detection results with reflective AI insights"""
        try:
            # Convert features to threat data format for reflective model
            threat_data = self._convert_to_threat_data(threat_result, features)

            # Get reflective insights - USE CORRECT METHOD
            enhanced_result = enhanced_detector.detect_threat_with_reflection(threat_data)

            # Merge results - preserve original structure while adding reflective insights
            threat_result.update({
                'reflection_insights': enhanced_result.get('reflection_insights', {}),
                'model_adaptation': enhanced_result.get('model_adaptation', {}),
                'confidence_calibrated': enhanced_result.get('confidence_calibrated', False),
                'reflection_applied': True,
                'final_confidence': enhanced_result.get('confidence', threat_result['original_confidence']),
                'adaptive_actions': enhanced_result.get('adaptation_recommendations', [])
            })

            # Update confidence if calibrated
            if enhanced_result.get('confidence_calibrated'):
                threat_result['original_confidence'] = enhanced_result['confidence']

        except Exception as e:
            print(f"⚠️  Reflective AI enhancement failed: {e}")
            threat_result['reflection_applied'] = False
            threat_result['reflection_error'] = str(e)

        return threat_result

    def _convert_to_threat_data(self, threat_result: Dict, features) -> Dict:
        """Convert ML model output to threat data format for reflective AI"""
        # Determine threat type from categories
        threat_categories = threat_result['threat_categories']
        primary_category = threat_categories[0]['category'] if threat_categories else 'unknown'

        # Map categories to threat types
        category_to_type = {
            'phishing': 'phishing',
            'malware': 'malware',
            'ransomware': 'ransomware',
            'ddos': 'ddos',
            'data_exfiltration': 'data_theft',
            'insider_threat': 'insider_threat'
        }

        threat_type = category_to_type.get(primary_category, 'unknown')

        # Determine severity based on score
        severity_score = threat_result['severity_score']
        if severity_score > 0.8:
            severity = 'critical'
        elif severity_score > 0.6:
            severity = 'high'
        elif severity_score > 0.4:
            severity = 'medium'
        else:
            severity = 'low'

        return {
            'threat_type': threat_type,
            'severity': severity,
            'confidence': threat_result['original_confidence'],
            'categories': [cat['category'] for cat in threat_categories],
            'indicators': self._extract_indicators(features),
            'response_action': threat_result['recommended_response']['action'],
            'timestamp': threat_result['timestamp']
        }

    def _extract_indicators(self, features) -> list:
        """Extract threat indicators from features"""
        indicators = []
        feature_names = getattr(self.config, 'FEATURE_NAMES', [f'feature_{i}' for i in range(len(features))])

        # Simple indicator extraction based on feature values
        for i, value in enumerate(features):
            if value > 0.7:  # High feature value
                indicator_name = feature_names[i] if i < len(feature_names) else f'high_value_feature_{i}'
                indicators.append(f'high_{indicator_name}')
            elif value < 0.3:  # Low feature value
                indicator_name = feature_names[i] if i < len(feature_names) else f'low_value_feature_{i}'
                indicators.append(f'low_{indicator_name}')

        return indicators

    def _interpret_threat_categories(self, threat_detection):
        """Your original method - preserved exactly"""
        categories = []
        for category, score in zip(self.config.THREAT_CATEGORIES.keys(), threat_detection[0]):
            if score > 0.5:
                categories.append({
                    'category': category,
                    'confidence': float(score)
                })
        return categories

    def _interpret_response(self, response_recommendation):
        """Your original method - preserved exactly"""
        responses = [
            'no_action',
            'alert_security_team',
            'block_ip_address',
            'quarantine_system',
            'initiate_incident_response'
        ]
        best_response_idx = np.argmax(response_recommendation[0])
        return {
            'action': responses[best_response_idx],
            'confidence': float(response_recommendation[0][best_response_idx])
        }

    def get_engine_status(self) -> Dict:
        """Get enhanced engine status with reflective AI info"""
        status = {
            'status': 'active',
            'model_loaded': self.model is not None,
            'data_processor_ready': self.data_processor is not None,
            'total_detections': len(self.threat_history),
            'reflective_ai_enabled': self.reflective_enabled,
            'reflective_ai_available': REFLECTIVE_AI_AVAILABLE
        }

        if self.reflective_enabled:
            try:
                ai_status = enhanced_detector.get_detector_status()
                status.update({
                    'reflective_model_version': ai_status.get('model_insights', {}).get('model_version', '2.0.0'),
                    'adaptive_learning_cycles': ai_status.get('adaptive_learning_cycles', 0),
                    'recent_adaptations': len(ai_status.get('model_insights', {}).get('recent_adaptations', []))
                })
            except Exception as e:
                status['reflective_error'] = str(e)

        return status

    def get_reflective_insights(self) -> Dict:
        """Get reflective AI insights for dashboard"""
        if not self.reflective_enabled:
            return {'status': 'reflective_ai_disabled'}

        try:
            return enhanced_detector.get_detector_status()
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def detect_threat_with_reflection(self, features):
        """Enhanced detection with reflective AI - MAIN FIX HERE"""
        # Simply call the main detect_threat method which already handles reflection
        return self.detect_threat(features)


# Backward compatibility - if you have existing code that uses these
def create_detection_engine(model, config, data_processor):
    """Factory function for backward compatibility"""
    return ThreatDetectionEngine(model, config, data_processor)