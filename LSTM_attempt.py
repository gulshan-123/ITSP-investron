import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import Model, Sequential
from keras._tf_keras.keras.losses import MeanSquaredError, BinaryCrossentropy
from keras._tf_keras.keras.layers import Dense, Input, Normalization,Dropout, LSTM
# from tensorflow.keras.layers import Dense, Input
# from tensorflow.keras import Sequential
# from tensorflow.keras.losses import MeanSquaredError, BinaryCrossentropy
from keras._tf_keras.keras.activations import sigmoid
from keras._tf_keras.keras.optimizers import Adam

import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
tf.autograph.set_verbosity(0)

# cols_to_use = [0,1,7,8]

data = np.genfromtxt('newdata/Total_data.csv', delimiter=',',skip_header=1)

X = data[:,:-1]
Y = data[:,-1]

cv_index = int(0.6 * len(X))
test_index = int(0.8*len(X))

X_train, X_val, X_test = X[:cv_index], X[cv_index:test_index], X[test_index:]
Y_train,Y_val, Y_test = Y[:cv_index], Y[cv_index:test_index], Y[test_index:]


# X_train = X_train[:,cols_to_use]
# X_val = X_val[:,cols_to_use]
# X_test = X_test[:,cols_to_use]

norm_l = Normalization(axis=-1)
norm_l.adapt(X)
X_train_n = norm_l(X_train)
X_test_n = norm_l(X_test)
X_val_n = norm_l(X_val)

X_train_n = tf.reshape(X_train_n, (X_train_n.shape[0], 1, X_train_n.shape[1]))
X_val_n = tf.reshape(X_val_n, (X_val_n.shape[0], 1, X_val_n.shape[1]))
X_test_n = tf.reshape(X_test_n, (X_test_n.shape[0], 1, X_test_n.shape[1]))
Y_train = tf.reshape(Y_train, (Y_train.shape[0], 1, 1))
Y_val = tf.reshape(Y_val, (Y_val.shape[0], 1, 1))
Y_test = tf.reshape(Y_test, (Y_test.shape[0], 1, 1))


tf.random.set_seed(69)

model = Sequential(
    [
        Input(shape=(1,9)),
        LSTM(32,activation='relu', name="LSTM_1", return_sequences=True),
        Dense(8, activation='relu', name="Dense_2"),
        Dense(1, activation='sigmoid', name="Output")
    ]
)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(X_train_n, Y_train, validation_data=(X_val_n, Y_val), epochs=10, batch_size=32)

model.summary()

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

test_loss, test_accuracy = model.evaluate(X_test_n, Y_test)
print(f'Test Accuracy: {test_accuracy}')
