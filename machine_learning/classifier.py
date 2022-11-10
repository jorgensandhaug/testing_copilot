"""
Neural network classifier for the MNIST dataset.
"""

import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



def xavier_init(size):
    in_dim = size[0]
    xavier_stddev = 1. / tf.sqrt(in_dim / 2.)
    return tf.random_normal(shape=size, stddev=xavier_stddev)

class NeuralNetwork:
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim

        self.build_model()

    def build_model(self):
        self.X = tf.placeholder(tf.float32, shape=[None, self.input_dim])
        self.y = tf.placeholder(tf.float32, shape=[None, self.output_dim])

        self.W1 = tf.Variable(xavier_init([self.input_dim, self.hidden_dim]))
        self.b1 = tf.Variable(tf.zeros(shape=[self.hidden_dim]))
        self.h1 = tf.nn.relu(tf.matmul(self.X, self.W1) + self.b1)

        self.W2 = tf.Variable(xavier_init([self.hidden_dim, self.output_dim]))
        self.b2 = tf.Variable(tf.zeros(shape=[self.output_dim]))
        self.logits = tf.matmul(self.h1, self.W2) + self.b2

        self.y_pred = tf.nn.softmax(self.logits)

        self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.y))
        self.optimizer = tf.train.AdamOptimizer().minimize(self.loss)

        self.correct_prediction = tf.equal(tf.argmax(self.y_pred, 1), tf.argmax(self.y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32))

    def train(self, X_train, y_train, X_test, y_test, batch_size=128, epochs=10, verbose=True):
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        num_batches = int(X_train.shape[0] / batch_size)
        for epoch in range(epochs):
            X_train, y_train = shuffle(X_train, y_train)
            for i in range(num_batches):
                X_batch = X_train[i*batch_size:(i+1)*batch_size]
                y_batch = y_train[i*batch_size:(i+1)*batch_size]
                _, loss = self.sess.run([self.optimizer, self.loss], feed_dict={self.X: X_batch, self.y: y_batch})

            if verbose and epoch % 10 == 0:
                train_accuracy = self.sess.run(self.accuracy, feed_dict={self.X: X_train, self.y: y_train})
                test_accuracy = self.sess.run(self.accuracy, feed_dict={self.X: X_test, self.y: y_test})
                print("Epoch: %d, loss: %f, train accuracy: %f, test accuracy: %f" % (epoch, loss, train_accuracy, test_accuracy))

    def predict(self, X):
        return self.sess.run(self.y_pred, feed_dict={self.X: X})

    def generate(self, z):
        return self.sess.run(self.y_pred, feed_dict={self.z: z})

    def close(self):
        self.sess.close()

# Allow the user to draw a digit using the mouse


if __name__ == '__main__':
    # Get data from MNIST dataset
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

    # Reshape and normalize images
    train_images = train_images.reshape(train_images.shape[0], 28*28).astype('float32') / 255
    test_images = test_images.reshape(test_images.shape[0], 28*28).astype('float32') / 255

    # One-hot encode labels
    train_labels = tf.keras.utils.to_categorical(train_labels, 10)
    test_labels = tf.keras.utils.to_categorical(test_labels, 10)

    # Split data into training and validation sets
    X_train, X_test, y_train, y_test = train_test_split(train_images, train_labels, test_size=0.2)

    # Create neural network
    nn = NeuralNetwork(input_dim=28*28, hidden_dim=128, output_dim=10)


    # Train neural network
    nn.train(X_train, y_train, X_test, y_test, epochs=10)


    # Test neural network
    test_accuracy = nn.sess.run(nn.accuracy, feed_dict={nn.X: test_images, nn.y: test_labels})
    print("Test accuracy: %f" % test_accuracy)

    # Visualize predictions, 10 at a time (change the index to see different predictions)
    index = 0
    predictions = nn.predict(test_images[index:index+10])
    for i in range(10):
        plt.subplot(2, 5, i+1)
        plt.imshow(test_images[index+i].reshape(28, 28), cmap='gray')
        plt.axis('off')
        plt.title(np.argmax(predictions[i]))

    plt.show()


    # Close session
    nn.close()




