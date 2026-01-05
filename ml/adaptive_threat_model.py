# src/ml/adaptive_threat_model.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import hashlib
from typing import Dict, List, Any
import threading
from collections import defaultdict, deque


class ReflectiveCoAdaptiveModel:
    def __init__(self):
        self.model_version = "2.0.0"
        self.learning_rate = 0.01
        self.adaptation_threshold = 0.15
        self.memory_window = 1000  # Last 1000 interactions

        # Reflection components
        self.threat_patterns = defaultdict(list)
        self.false_positive_history = deque(maxlen=500)
        self.false_negative_history = deque(maxlen=500)
        self.adaptation_log = []
        self.performance_metrics = {
            'accuracy_trend': [],
            'response_time_trend': [],
            'threat_evolution': defaultdict(list)
        }

        # Co-adaptation components
        self.user_feedback = {}
        self.system_interactions = {}
        self.environment_context = {}

        # Real-time learning parameters
        self.confidence_threshold = 0.85
        self.adaptation_cooldown = timedelta(minutes=5)
        self.last_adaptation = datetime.now()

        print("🔄 Reflective Co-Adaptive AI Model Initialized")

    def analyze_and_reflect(self, threat_data: Dict, detection_result: Dict) -> Dict:
        """Main reflective analysis method"""
        reflection_insights = {
            'immediate_analysis': self._immediate_analysis(threat_data, detection_result),
            'pattern_recognition': self._recognize_emerging_patterns(threat_data),
            'adaptation_recommendations': self._generate_adaptation_recommendations(detection_result),
            'confidence_calibration': self._calibrate_confidence(detection_result),
            'learning_opportunities': self._identify_learning_opportunities(threat_data, detection_result)
        }

        # Real-time adaptation if needed
        if self._requires_immediate_adaptation(reflection_insights):
            self._perform_adaptive_learning(threat_data, detection_result)

        return reflection_insights

    def _immediate_analysis(self, threat_data: Dict, detection_result: Dict) -> Dict:
        """Analyze current detection for reflection"""
        analysis = {
            'detection_quality': self._assess_detection_quality(detection_result),
            'threat_novelty': self._assess_threat_novelty(threat_data),
            'response_appropriateness': self._assess_response_appropriateness(threat_data, detection_result),
            'system_impact': self._assess_system_impact(threat_data)
        }

        # Store for pattern recognition
        self._update_threat_patterns(threat_data, detection_result, analysis)

        return analysis

    def _recognize_emerging_patterns(self, threat_data: Dict) -> List[Dict]:
        """Identify emerging threat patterns and trends"""
        patterns = []

        # Temporal pattern analysis
        temporal_patterns = self._analyze_temporal_patterns(threat_data)
        if temporal_patterns:
            patterns.append({'type': 'temporal', 'insights': temporal_patterns})

        # Behavioral pattern analysis
        behavioral_patterns = self._analyze_behavioral_patterns(threat_data)
        if behavioral_patterns:
            patterns.append({'type': 'behavioral', 'insights': behavioral_patterns})

        # Threat evolution analysis
        evolution_patterns = self._analyze_threat_evolution(threat_data)
        if evolution_patterns:
            patterns.append({'type': 'evolution', 'insights': evolution_patterns})

        return patterns

    def _analyze_temporal_patterns(self, threat_data: Dict) -> Dict:
        """Analyze time-based threat patterns"""
        current_hour = datetime.now().hour
        current_day = datetime.now().weekday()

        # Analyze if this is part of a coordinated attack
        recent_similar = len([t for t in list(self.threat_patterns.values())[-10:]
                              if self._similar_threats(t, threat_data)])

        return {
            'peak_hour_threat': current_hour in [9, 10, 14, 15],  # Common attack hours
            'weekend_anomaly': current_day >= 5 and threat_data.get('severity') == 'high',
            'coordinated_attack_indicator': recent_similar > 3,
            'recommended_alert_level': 'elevated' if recent_similar > 2 else 'normal'
        }

    def _analyze_behavioral_patterns(self, threat_data: Dict) -> Dict:
        """Analyze behavioral patterns in threats"""
        threat_type = threat_data.get('threat_type', 'unknown')

        # Track behavioral evolution
        if threat_type in self.performance_metrics['threat_evolution']:
            evolution_trend = self.performance_metrics['threat_evolution'][threat_type]
            if len(evolution_trend) > 5:
                trend_direction = 'increasing' if evolution_trend[-1] > evolution_trend[-5] else 'decreasing'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'new'

        return {
            'threat_sophistication': self._assess_sophistication(threat_data),
            'attack_complexity': self._assess_attack_complexity(threat_data),
            'evolution_trend': trend_direction,
            'behavioral_anomalies': self._detect_behavioral_anomalies(threat_data)
        }

    def _analyze_threat_evolution(self, threat_data: Dict) -> Dict:
        """Analyze how threats are evolving over time"""
        threat_signature = self._generate_threat_signature(threat_data)

        if threat_signature in self.threat_patterns:
            pattern_history = self.threat_patterns[threat_signature]
            evolution_metrics = self._calculate_evolution_metrics(pattern_history)

            return {
                'mutation_rate': evolution_metrics.get('mutation_rate', 0),
                'effectiveness_trend': evolution_metrics.get('effectiveness_trend', 'stable'),
                'detection_resistance': evolution_metrics.get('detection_resistance', 'low'),
                'recommended_countermeasures': self._suggest_countermeasures(evolution_metrics)
            }

        return {'status': 'novel_threat', 'recommendation': 'enhance_monitoring'}

    def _generate_adaptation_recommendations(self, detection_result: Dict) -> List[Dict]:
        """Generate adaptive learning recommendations"""
        recommendations = []

        # Confidence-based adaptations
        confidence = detection_result.get('confidence', 0)
        if confidence < self.confidence_threshold:
            recommendations.append({
                'type': 'confidence_calibration',
                'priority': 'high',
                'action': 'adjust_confidence_thresholds',
                'reason': f'Low confidence detection: {confidence:.2f}'
            })

        # Pattern-based adaptations
        if len(self.false_positive_history) > 10:
            fp_rate = len(self.false_positive_history) / 100
            if fp_rate > 0.1:  # 10% false positive rate
                recommendations.append({
                    'type': 'false_positive_reduction',
                    'priority': 'medium',
                    'action': 'increase_detection_specificity',
                    'reason': f'High false positive rate: {fp_rate:.1%}'
                })

        # Performance-based adaptations
        if len(self.performance_metrics['accuracy_trend']) > 7:
            recent_accuracy = np.mean(self.performance_metrics['accuracy_trend'][-7:])
            if recent_accuracy < 0.92:  # Below target accuracy
                recommendations.append({
                    'type': 'performance_optimization',
                    'priority': 'high',
                    'action': 'model_retraining',
                    'reason': f'Accuracy below target: {recent_accuracy:.1%}'
                })

        return recommendations

    def _calibrate_confidence(self, detection_result: Dict) -> Dict:
        """Calibrate confidence scores based on historical performance"""
        actual_confidence = detection_result.get('confidence', 0.5)
        threat_type = detection_result.get('threat_type', 'unknown')

        # Historical accuracy for this threat type
        historical_accuracy = self._get_historical_accuracy(threat_type)

        # Adjust confidence based on historical performance
        calibrated_confidence = actual_confidence * historical_accuracy if historical_accuracy > 0 else actual_confidence

        return {
            'original_confidence': actual_confidence,
            'calibrated_confidence': min(0.99, calibrated_confidence),
            'calibration_factor': historical_accuracy,
            'recommended_threshold_adjustment': self._calculate_threshold_adjustment(calibrated_confidence)
        }

    def _identify_learning_opportunities(self, threat_data: Dict, detection_result: Dict) -> List[Dict]:
        """Identify opportunities for model improvement"""
        opportunities = []

        # Novel threat detection
        if self._is_novel_threat(threat_data):
            opportunities.append({
                'type': 'novel_threat_learning',
                'priority': 'high',
                'description': 'New threat pattern identified',
                'learning_data': threat_data
            })

        # False positive/negative analysis
        if detection_result.get('is_false_positive', False):
            opportunities.append({
                'type': 'false_positive_analysis',
                'priority': 'medium',
                'description': 'Improve specificity for this pattern',
                'learning_data': threat_data
            })

        # Performance optimization
        response_time = detection_result.get('response_time', 0)
        if response_time > 0.1:  # 100ms threshold
            opportunities.append({
                'type': 'performance_optimization',
                'priority': 'low',
                'description': 'Optimize detection pipeline',
                'metrics': {'response_time': response_time}
            })

        return opportunities

    def _requires_immediate_adaptation(self, reflection_insights: Dict) -> bool:
        """Determine if immediate adaptation is required"""
        if datetime.now() - self.last_adaptation < self.adaptation_cooldown:
            return False

        # Check adaptation triggers
        analysis = reflection_insights['immediate_analysis']
        patterns = reflection_insights['pattern_recognition']

        # Trigger adaptation for coordinated attacks
        for pattern in patterns:
            if pattern.get('type') == 'temporal':
                if pattern['insights'].get('coordinated_attack_indicator'):
                    return True

        # Trigger for significant detection quality issues
        if analysis['detection_quality'].get('score', 0) < 0.7:
            return True

        return False

    def _perform_adaptive_learning(self, threat_data: Dict, detection_result: Dict):
        """Perform real-time adaptive learning"""
        print("🔄 Performing adaptive learning...")

        # Update model parameters based on recent performance
        self._update_learning_parameters(threat_data, detection_result)

        # Adjust confidence thresholds
        self._adjust_confidence_thresholds(detection_result)

        # Update pattern recognition
        self._enhance_pattern_recognition(threat_data)

        self.last_adaptation = datetime.now()
        self.adaptation_log.append({
            'timestamp': datetime.now(),
            'threat_data': threat_data,
            'adaptation_type': 'real_time_learning',
            'parameters_updated': ['learning_rate', 'confidence_thresholds', 'pattern_weights']
        })

    # Helper methods
    def _similar_threats(self, threat1: Dict, threat2: Dict) -> bool:
        """Check if two threats are similar"""
        key_attributes = ['threat_type', 'severity', 'source_pattern']
        similarity_score = 0

        for attr in key_attributes:
            if threat1.get(attr) == threat2.get(attr):
                similarity_score += 1

        return similarity_score >= len(key_attributes) * 0.7

    def _generate_threat_signature(self, threat_data: Dict) -> str:
        """Generate unique signature for threat pattern"""
        signature_data = {
            'type': threat_data.get('threat_type'),
            'indicators': str(sorted(threat_data.get('indicators', []))),
            'complexity': threat_data.get('complexity_level', 'medium')
        }
        return hashlib.md5(json.dumps(signature_data, sort_keys=True).encode()).hexdigest()

    def _get_historical_accuracy(self, threat_type: str) -> float:
        """Get historical accuracy for specific threat type"""
        # Simplified implementation - replace with actual historical data
        accuracy_map = {
            'phishing': 0.94,
            'ransomware': 0.96,
            'ddos': 0.92,
            'malware': 0.89,
            'data_theft': 0.91
        }
        return accuracy_map.get(threat_type, 0.90)

    def _calculate_threshold_adjustment(self, confidence: float) -> float:
        """Calculate recommended threshold adjustment"""
        if confidence > 0.9:
            return -0.05  # Lower threshold for high confidence
        elif confidence < 0.7:
            return 0.05  # Raise threshold for low confidence
        else:
            return 0.0  # No adjustment needed

    def _is_novel_threat(self, threat_data: Dict) -> bool:
        """Check if threat is novel based on historical patterns"""
        signature = self._generate_threat_signature(threat_data)
        return signature not in self.threat_patterns

    def _update_threat_patterns(self, threat_data: Dict, detection_result: Dict, analysis: Dict):
        """Update threat pattern database"""
        signature = self._generate_threat_signature(threat_data)
        pattern_record = {
            'timestamp': datetime.now(),
            'threat_data': threat_data,
            'detection_result': detection_result,
            'analysis': analysis,
            'effectiveness': analysis['detection_quality'].get('score', 0.5)
        }

        self.threat_patterns[signature].append(pattern_record)

        # Keep only recent patterns
        if len(self.threat_patterns[signature]) > 50:
            self.threat_patterns[signature] = self.threat_patterns[signature][-50:]

    def _assess_detection_quality(self, detection_result: Dict) -> Dict:
        """Assess the quality of detection"""
        confidence = detection_result.get('confidence', 0)
        response_time = detection_result.get('response_time', 0)

        quality_score = confidence * (1 - min(response_time / 1.0, 1))  # Normalize response time

        return {
            'score': quality_score,
            'confidence_contribution': confidence,
            'speed_contribution': 1 - min(response_time / 1.0, 1),
            'rating': 'excellent' if quality_score > 0.9 else 'good' if quality_score > 0.7 else 'needs_improvement'
        }

    def _assess_threat_novelty(self, threat_data: Dict) -> Dict:
        """Assess how novel the threat is"""
        signature = self._generate_threat_signature(threat_data)
        novelty = signature not in self.threat_patterns

        return {
            'is_novel': novelty,
            'novelty_score': 1.0 if novelty else 0.1,
            'similar_patterns_count': len([p for p in self.threat_patterns.values()
                                           if self._similar_threats(p[0]['threat_data'],
                                                                    threat_data)]) if not novelty else 0
        }

    def _assess_response_appropriateness(self, threat_data: Dict, detection_result: Dict) -> Dict:
        """Assess if the response was appropriate for the threat"""
        severity = threat_data.get('severity', 'medium')
        response_level = detection_result.get('response_level', 'medium')

        severity_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        response_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}

        appropriateness = 1.0 - abs(severity_map.get(severity, 2) - response_map.get(response_level, 2)) / 4.0

        return {
            'appropriateness_score': appropriateness,
            'severity_match': severity == response_level,
            'recommendation': 'increase_response' if severity_map.get(severity, 2) > response_map.get(response_level,
                                                                                                      2) else 'decrease_response'
        }

    def _assess_system_impact(self, threat_data: Dict) -> Dict:
        """Assess potential system impact of the threat"""
        impact_factors = {
            'data_exfiltration_risk': 0.8 if 'data' in threat_data.get('threat_type', '').lower() else 0.2,
            'system_availability_risk': 0.9 if 'ddos' in threat_data.get('threat_type', '').lower() else 0.3,
            'data_integrity_risk': 0.7 if 'ransomware' in threat_data.get('threat_type', '').lower() else 0.2,
            'compliance_risk': 0.6 if 'phishing' in threat_data.get('threat_type', '').lower() else 0.1
        }

        total_impact = sum(impact_factors.values()) / len(impact_factors)

        return {
            'total_impact_score': total_impact,
            'impact_factors': impact_factors,
            'risk_level': 'high' if total_impact > 0.7 else 'medium' if total_impact > 0.4 else 'low'
        }

    def _assess_sophistication(self, threat_data: Dict) -> str:
        """Assess threat sophistication level"""
        indicators = threat_data.get('indicators', [])
        complexity_indicators = ['evasion', 'polymorphic', 'zero-day', 'advanced_persistent']

        sophistication_score = sum(
            1 for indicator in indicators if any(comp in str(indicator).lower() for comp in complexity_indicators))

        if sophistication_score >= 3:
            return 'advanced'
        elif sophistication_score >= 1:
            return 'intermediate'
        else:
            return 'basic'

    def _assess_attack_complexity(self, threat_data: Dict) -> str:
        """Assess attack complexity"""
        tactics_count = len(threat_data.get('attack_tactics', []))
        resources_required = threat_data.get('resources_required', 1)

        complexity_score = tactics_count * resources_required

        if complexity_score > 6:
            return 'high'
        elif complexity_score > 3:
            return 'medium'
        else:
            return 'low'

    def _detect_behavioral_anomalies(self, threat_data: Dict) -> List[str]:
        """Detect behavioral anomalies in the threat"""
        anomalies = []

        # Check for unusual timing
        current_hour = datetime.now().hour
        if current_hour in [2, 3, 4] and threat_data.get('severity') == 'critical':
            anomalies.append('unusual_critical_activity_time')

        # Check for coordination patterns
        if threat_data.get('source_count', 1) > 5:
            anomalies.append('multiple_source_coordination')

        return anomalies

    def _calculate_evolution_metrics(self, pattern_history: List) -> Dict:
        """Calculate evolution metrics for threat patterns"""
        if len(pattern_history) < 2:
            return {'mutation_rate': 0, 'effectiveness_trend': 'stable'}

        effectiveness_trend = []
        for record in pattern_history:
            effectiveness_trend.append(record.get('effectiveness', 0.5))

        # Calculate trend
        if len(effectiveness_trend) >= 3:
            recent_avg = np.mean(effectiveness_trend[-3:])
            previous_avg = np.mean(effectiveness_trend[-6:-3]) if len(effectiveness_trend) >= 6 else \
            effectiveness_trend[0]
            trend = 'improving' if recent_avg > previous_avg else 'declining' if recent_avg < previous_avg else 'stable'
        else:
            trend = 'insufficient_data'

        return {
            'mutation_rate': len(pattern_history) / 30,  # Simplified mutation rate
            'effectiveness_trend': trend,
            'detection_resistance': 'high' if trend == 'declining' else 'medium' if trend == 'stable' else 'low'
        }

    def _suggest_countermeasures(self, evolution_metrics: Dict) -> List[str]:
        """Suggest countermeasures based on evolution metrics"""
        countermeasures = []

        if evolution_metrics.get('detection_resistance') == 'high':
            countermeasures.extend(['enhanced_behavioral_analysis', 'multi_vector_correlation', 'threat_hunting'])

        if evolution_metrics.get('mutation_rate', 0) > 0.5:
            countermeasures.extend(['adaptive_signatures', 'machine_learning_detection', 'anomaly_detection'])

        return countermeasures if countermeasures else ['standard_protocols']

    def _update_learning_parameters(self, threat_data: Dict, detection_result: Dict):
        """Update learning parameters based on recent performance"""
        # Adaptive learning rate based on performance
        accuracy_trend = self.performance_metrics['accuracy_trend']
        if len(accuracy_trend) > 10:
            recent_accuracy = np.mean(accuracy_trend[-5:])
            historical_accuracy = np.mean(accuracy_trend[-10:])

            if recent_accuracy < historical_accuracy:
                # Decrease learning rate if performance is declining
                self.learning_rate = max(0.001, self.learning_rate * 0.9)
            else:
                # Increase learning rate if performance is improving
                self.learning_rate = min(0.1, self.learning_rate * 1.1)

    def _adjust_confidence_thresholds(self, detection_result: Dict):
        """Adjust confidence thresholds dynamically"""
        confidence = detection_result.get('confidence', 0.5)

        # Adjust based on recent performance
        if confidence < 0.7 and len(self.false_negative_history) > len(self.false_positive_history):
            # Lower threshold if missing too many threats
            self.confidence_threshold = max(0.6, self.confidence_threshold * 0.95)
        elif confidence > 0.9 and len(self.false_positive_history) > len(self.false_negative_history):
            # Raise threshold if too many false positives
            self.confidence_threshold = min(0.95, self.confidence_threshold * 1.05)

    def _enhance_pattern_recognition(self, threat_data: Dict):
        """Enhance pattern recognition capabilities"""
        # This would integrate with your existing pattern recognition
        # For now, we'll simulate pattern enhancement
        signature = self._generate_threat_signature(threat_data)

        if signature not in self.threat_patterns:
            print(f"🎯 Enhanced pattern recognition for new threat signature: {signature[:8]}")

    def get_model_insights(self) -> Dict:
        """Get comprehensive model insights for dashboard"""
        return {
            'model_version': self.model_version,
            'learning_rate': self.learning_rate,
            'confidence_threshold': self.confidence_threshold,
            'adaptation_count': len(self.adaptation_log),
            'pattern_database_size': len(self.threat_patterns),
            'recent_adaptations': self.adaptation_log[-5:] if self.adaptation_log else [],
            'performance_trends': self.performance_metrics
        }