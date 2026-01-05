# src/model_training/hybrid_model.py
import tensorflow as tf
from tensorflow.keras import layers, Model
# OR try this alternative:
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


class ReGLU(layers.Layer):
    def __init__(self, **kwargs):
        super(ReGLU, self).__init__(**kwargs)

    def call(self, inputs):
        x, gate = tf.split(inputs, 2, axis=-1)
        return tf.nn.relu(x) * tf.sigmoid(gate)


class ThreatIntelligenceModel:
    def __init__(self, config):
        self.config = config
        self.model = self._build_model()

    def _build_model(self):
        main_input = layers.Input(shape=(50,), name='main_features')

        x = layers.Dense(128, activation='relu')(main_input)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(64, activation='relu')(x)

        # ReGLU implementation
        reglu_input = layers.Dense(128 * 2)(x)
        reglu_output = ReGLU()(reglu_input)

        x = layers.Dense(32, activation='relu')(reglu_output)

        # Output layers
        threat_detection = layers.Dense(
            len(self.config.THREAT_CATEGORIES),
            activation='sigmoid',
            name='threat_detection'
        )(x)

        threat_severity = layers.Dense(1, activation='linear', name='threat_severity')(x)

        response_recommendation = layers.Dense(
            5, activation='softmax', name='response_recommendation'
        )(x)

        model = Model(
            inputs=main_input,
            outputs=[threat_detection, threat_severity, response_recommendation]
        )

        return model

    def compile_model(self):
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.LEARNING_RATE),
            loss={
                'threat_detection': 'binary_crossentropy',
                'threat_severity': 'mse',
                'response_recommendation': 'categorical_crossentropy'
            }
        )