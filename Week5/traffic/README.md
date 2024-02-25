# 0

```python
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=['accuracy']
)
```

can't use loss="sparse_categorical_crossentropy"

# 1

```python
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=['accuracy']
)
```

result:

333/333 - 2s - loss: 0.0258 - accuracy: 0.9470 - 2s/epoch - 5ms/step

# 2
```python
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D((3, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=['accuracy']
)
```

result:

333/333 - 1s - loss: 0.0247 - accuracy: 0.9347 - 1s/epoch - 4ms/step

# 3
```python
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D((3, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=['accuracy']
)
```

添加了一层有32个神经元的全连接层（隐藏层）

result:
333/333 - 1s - loss: 0.1177 - accuracy: 0.0527 - 1s/epoch - 4ms/step

# 4

```python

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=['accuracy']
)
```

添加新的卷积层和池化层

result:

333/333 - 2s - loss: 0.0141 - accuracy: 0.9703 - 2s/epoch - 5ms/step

# 5 
```python

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(128, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=['accuracy']
)
```

添加卷积层和池化层

result:

333/333 - 3s - loss: 0.0077 - accuracy: 0.9730 - 3s/epoch - 9ms/step
