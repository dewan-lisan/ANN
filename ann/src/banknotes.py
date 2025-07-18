import csv
import tensorflow as tf
import numpy as np

from sklearn.model_selection import train_test_split

# Read data in from file
with open("resources/banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })

# Separate data into training and testing groups
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]
X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)


# Create a neural network using Keras. Keras is a high-level API for building and training neural networks,
# designed for ease of use and rapid prototyping. It simplifies the process of creating deep learning models by
# providing a user-friendly interface and pre-built components like layers, optimizers, and loss functions. Keras is
# designed to work with other deep learning frameworks like TensorFlow, JAX, and PyTorch, making it flexible and
# adaptable to different needs.
model = tf.keras.models.Sequential()

# Add a hidden layer with 8 units, with ReLU activation
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"))

# Add output layer with 1 unit, with sigmoid activation
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# Train neural network
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(np.array(X_training), np.array(y_training), epochs=20)

# Evaluate how well model performs
print("Testing now...")
model.evaluate(np.array(X_testing), np.array(y_testing), verbose=2)
