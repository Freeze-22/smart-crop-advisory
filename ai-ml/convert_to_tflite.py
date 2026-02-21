import tensorflow as tf

# Load the saved model
model = tf.keras.models.load_model('models/pest_model.h5')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save
with open('models/pest_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite model saved successfully!")
