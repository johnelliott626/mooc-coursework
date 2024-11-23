import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    images = list()
    labels = list()

    for category in range(NUM_CATEGORIES):
        current_category_dir = os.path.join(data_dir, str(category))

        for image in os.listdir(current_category_dir):
            image_path = os.path.join(current_category_dir, image)
            raw_image = cv2.imread(image_path)
            processed_image = cv2.resize(raw_image, (IMG_WIDTH, IMG_HEIGHT))

            images.append(processed_image)
            labels.append(category)

    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a sequential model
    model = tf.keras.models.Sequential([

        # Add the input shape of the first layer (width, height, 3 values for each pixel -- RGB)
        tf.keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # Add the first layer as a convolutional layer. Learn 32 filters using a 3x3 kernel.
        tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation="relu"),
    ])

    # Add the second layer as a max pooling layer with a 2x2 filter size
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Add another convolutional layer with 64 filters
    model.add(tf.keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation="relu"))
    # Add another max pooling layer with a 2x2 filter size
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

    # Flatten the units (pixels) to serve as input to the traditional neural network
    model.add(tf.keras.layers.Flatten())

    # Add a hidden layer with dropout that connects to all neurons of previous layer (all pixels)
    model.add(tf.keras.layers.Dense(units=128, activation="relu"))
    model.add(tf.keras.layers.Dropout(rate=0.25))


    # Add the output layer with the number of image categories as units
    model.add(tf.keras.layers.Dense(units=NUM_CATEGORIES, activation="softmax"))


    # compile the model so it is ready for training
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
