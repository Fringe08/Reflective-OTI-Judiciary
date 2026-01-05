# src/threat_detection/performance.py
import time
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.threat_detection.enhanced_detector import enhanced_detector


class PerformanceMonitor:
    def __init__(self):
        self.detection_times = []
        self.accuracy_metrics = []
        self.adaptive_learning_stats = []
        self.start_time = datetime.now()

        print("📊 Performance Monitor with Reflective Tracking Initialized")

    def record_detection(self, threat_data: Dict, result: Dict, processing_time: float):
        """Record detection performance with reflective insights"""
        record = {
            'timestamp': datetime.now(),
            'threat_type': threat_data.get('threat_type'),
            'processing_time': processing_time,
            'confidence': result.get('confidence', 0),
            'reflection_applied': result.get('reflection_applied', False),
            'adaptation_used': result.get('detection_enhanced', False)
        }

        self.detection_times.append(record)

        # Keep only last 1000 records
        if len(self.detection_times) > 1000:
            self.detection_times = self.detection_times[-1000:]

    def calculate_performance_metrics(self) -> Dict:
        """Calculate comprehensive performance metrics"""
        if not self.detection_times:
            return {}

        # Basic metrics
        recent_detections = self.detection_times[-100:]  # Last 100 detections
        processing_times = [d['processing_time'] for d in recent_detections]
        confidence_scores = [d['confidence'] for d in recent_detections]

        # Reflective metrics
        reflective_detections = [d for d in recent_detections if d.get('reflection_applied')]
        adaptation_used = [d for d in recent_detections if d.get('adaptation_used')]

        # Get AI insights
        ai_insights = enhanced_detector.get_detector_status()

        return {
            'avg_processing_time': np.mean(processing_times) if processing_times else 0,
            'max_processing_time': max(processing_times) if processing_times else 0,
            'avg_confidence': np.mean(confidence_scores) if confidence_scores else 0,
            'reflective_usage_rate': len(reflective_detections) / len(recent_detections) if recent_detections else 0,
            'adaptation_usage_rate': len(adaptation_used) / len(recent_detections) if recent_detections else 0,
            'total_detections': len(self.detection_times),
            'system_uptime': (datetime.now() - self.start_time).total_seconds(),
            'ai_model_insights': ai_insights.get('model_insights', {}),
            'reflective_effectiveness': self._calculate_reflective_effectiveness()
        }

    def _calculate_reflective_effectiveness(self) -> Dict:
        """Calculate how effective reflective AI is"""
        recent_with_reflection = [d for d in self.detection_times[-50:] if d.get('reflection_applied')]
        recent_without_reflection = [d for d in self.detection_times[-50:] if not d.get('reflection_applied')]

        if not recent_with_reflection or not recent_without_reflection:
            return {'improvement_rate': 0, 'confidence_boost': 0}

        avg_confidence_with = np.mean([d['confidence'] for d in recent_with_reflection])
        avg_confidence_without = np.mean([d['confidence'] for d in recent_without_reflection])

        avg_time_with = np.mean([d['processing_time'] for d in recent_with_reflection])
        avg_time_without = np.mean([d['processing_time'] for d in recent_without_reflection])

        return {
            'confidence_improvement': avg_confidence_with - avg_confidence_without,
            'processing_time_impact': avg_time_with - avg_time_without,
            'improvement_rate': max(0, (avg_confidence_with - avg_confidence_without) / avg_confidence_without),
            'samples_compared': f"{len(recent_with_reflection)} vs {len(recent_without_reflection)}"
        }

    def test_detection_speed(self, sample_size: int = 100) -> Dict:
        """Enhanced performance test with reflective metrics"""
        print(f"🚀 Running enhanced performance test with {sample_size} samples...")

        test_results = []
        threat_types = ['phishing', 'ransomware', 'ddos', 'malware']

        for i in range(sample_size):
            threat_data = {
                'threat_type': np.random.choice(threat_types),
                'description': f"Test threat {i} with suspicious activity",
                'severity': np.random.choice(['low', 'medium', 'high']),
                'indicators': ['suspicious_pattern', 'unusual_behavior']
            }

            start_time = time.time()

            # Use the enhanced detection
            from src.threat_detection.detection_engine import detection_engine
            result = detection_engine.detect_threat(threat_data)

            processing_time = time.time() - start_time

            # Record with reflective insights
            self.record_detection(threat_data, result, processing_time)

            test_results.append({
                'iteration': i + 1,
                'processing_time': processing_time,
                'confidence': result.get('confidence', 0),
                'reflection_used': result.get('reflection_applied', False),
                'threat_type': threat_data['threat_type']
            })

        # Calculate metrics
        processing_times = [r['processing_time'] for r in test_results]
        confidence_scores = [r['confidence'] for r in test_results]
        reflective_usage = sum(1 for r in test_results if r['reflection_used'])

        performance_report = {
            'total_tests': sample_size,
            'avg_processing_time': np.mean(processing_times),
            'min_processing_time': min(processing_times),
            'max_processing_time': max(processing_times),
            'avg_confidence': np.mean(confidence_scores),
            'reflective_usage_count': reflective_usage,
            'reflective_usage_percentage': (reflective_usage / sample_size) * 100,
            'throughput': sample_size / sum(processing_times),
            'performance_grade': 'A' if np.mean(processing_times) < 0.05 else 'B' if np.mean(
                processing_times) < 0.1 else 'C'
        }

        print("🎯 Enhanced Performance Test Completed!")
        print(f"   Average Processing Time: {performance_report['avg_processing_time']:.4f}s")
        print(f"   Reflective AI Usage: {performance_report['reflective_usage_percentage']:.1f}%")
        print(f"   Average Confidence: {performance_report['avg_confidence']:.2f}")
        print(f"   Performance Grade: {performance_report['performance_grade']}")

        return performance_report


# Global instance
performance_monitor = PerformanceMonitor()