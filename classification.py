import tensorflow as tf
from pathlib import Path
from keras.models import Sequential
from typing import Optional
from keras.utils import image_dataset_from_directory

class Classification:

    def __init__(self, IMG_SIZE: tuple, batch_size,
                  train_dataset: Path, test_dataset: Path,
                  epochs: int = 10 ,validation_dataset: Optional[Path]=None):    
        
        self.IMG_SIZE=IMG_SIZE
        self.batch_size=batch_size
        self.train_dataset=train_dataset
        self.validation_dataset=validation_dataset
        self.test_dataset=test_dataset
        self.epochs=epochs

        train_ds=image_dataset_from_directory(
            directory=train_dataset,
            batch_size=batch_size,
            image_size=IMG_SIZE
        )

        validation_ds=image_dataset_from_directory(
            directory=validation_dataset,
            batch_size=batch_size,
            image_size=IMG_SIZE
        )

        test_ds=image_dataset_from_directory(
            directory=test_dataset,
            batch_size=batch_size,
            image_size=IMG_SIZE
        )

        model = Sequential([
            tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"),
            tf.keras.layers.MaxPooling2D((2,2)),

            tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"),
            tf.keras.layers.MaxPooling2D((2,2)),

            tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"),
            tf.keras.layers.MaxPooling2D((2,2)),

            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="softmax"),
            tf.keras.layers.Dense(3)
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam,
            loss=tf.keras.losses.SparseCategoricalCrossentropy,
            metrics=["accuracy"]
        )

        if validation_dataset is None:    
            model.fit(train_ds,
                    epochs=epochs)

        else:
            model.fit(train_ds,
                      validation_data=validation_ds,
                      epochs=epochs)

        model.evaluate(test_ds)
