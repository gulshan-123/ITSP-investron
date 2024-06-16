import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import Model, Sequential
from keras._tf_keras.keras.losses import MeanSquaredError, BinaryCrossentropy
from keras._tf_keras.keras.layers import Dense, Input, Normalization,Dropout
# from tensorflow.keras.layers import Dense, Input
# from tensorflow.keras import Sequential
# from tensorflow.keras.losses import MeanSquaredError, BinaryCrossentropy
from keras._tf_keras.keras.activations import sigmoid
from keras._tf_keras.keras.optimizers import Adam

import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
tf.autograph.set_verbosity(0)

cols_to_use = [0,3,5,6,7,8]

X_train = np.genfromtxt('data/Training_data_sliced.csv', delimiter=',')

X_train = X_train[:,cols_to_use]

Y_train = np.genfromtxt('data/Output_Training_data.csv', delimiter=',')
X_val = np.genfromtxt('data/cross_validation_sliced.csv', delimiter=',')

X_val = X_val[:,cols_to_use]

y_val = np.genfromtxt('data/Output_cross_validation.csv', delimiter=',')
X_test = np.genfromtxt('data/test_set_sliced.csv', delimiter=',')

X_test = X_test[:,cols_to_use]

y_test = np.genfromtxt('data/Output_test_set.csv', delimiter=',')
print(X_train)
print(Y_train)
norm_l = Normalization(axis=-1)
norm_l.adapt(X_train)
X_n = norm_l(X_train)
X_val_n = norm_l(X_val)
X_test_n = norm_l(X_test)




tf.random.set_seed(69)

model = Sequential(
    [
        Input(shape=(6,)),
        # # Dense(1024,activation='relu', name='L_12_more'),
        # # # Dropout(0.3),
        Dense(512,activation='relu', name='L_1_more'),
        # Dropout(0.3),
        Dense(256,activation='relu', name='L_more'),
        # Dropout(0.3),
        # Dense(512,activation='relu', name='L1'),
        # # Dropout(0.3),
        Dense(128,activation='relu', name='L_add'),
        # Dropout(0.3),
        # Dense(64,activation='relu', name="L2"),
        # Dropout(0.2),
        # Dense(8,activation='relu', name="LZ"),
        # # # Dense(16,activation='relu', name="L3"),
        # Dense(32,activation='relu', name="L4"),
        # # Dropout(0.2),
        Dense(64,activation='relu', name="LY"),
        # # # Dropout(0.3),
        Dense(32,activation='relu', name="LX"),
        # # # Dropout(0.3),
        Dense(16,activation='relu', name="L5"),
        Dense(8,activation='relu', name="LW"),
        Dense(1,activation='sigmoid', name="Output")
    ]
)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_n, Y_train, validation_data=(X_val_n, y_val), epochs=5, batch_size=32)

model.summary()

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

test_loss, test_accuracy = model.evaluate(X_test_n, y_test)
print(f'Test Accuracy: {test_accuracy}')

all_layers = model.layers

# # Iterate through each layer to get its weights and biases
# for layer in all_layers:
#     # Check if the layer has weights (e.g., Dense layers have weights)
#     if hasattr(layer, 'weights'):
#         # Get weights and biases for the layer
#         weights = layer.get_weights()[0]  # weights
#         biases = layer.get_weights()[1]   # biases
        
#         print(f"Layer: {layer.name}")
#         print(f"Weights shape: {weights.shape}")
#         print(f"Biases shape: {biases.shape}")
#         print(f"Weights: \n{weights}")
#         print(f"Biases: \n{biases}")