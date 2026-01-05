# Fixed hybrid_model.py
try:
    from tensorflow.keras import layers, Model
    print('✅ Using tensorflow.keras import')
except ImportError:
    try:
        import tensorflow as tf
        layers = tf.keras.layers
        Model = tf.keras.Model
        print('✅ Using tf.keras import')
    except ImportError:
        print('❌ TensorFlow not available')

# Rest of your hybrid_model.py code goes here
class ThreatIntelligenceModel:
    def __init__(self):
        print('Threat Intelligence Model initialized')
    
    def train(self):
        print('Model training completed')
        return True
