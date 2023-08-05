import numpy as np
from NN.layers import Dense, Dropout
from NN.activations import ReLU, SoftMax
from NN.loss import CatCrossEntr
from NN import Model
from NN.optimizers import SGDOptimizer
from data import SplitData
from sklearn import datasets

# from keras.datasets import mnist
# (train_X, train_y), (test_X, test_y) = mnist.load_data()
# Keep these commented when not used, they take too much time to load
X, y = datasets.make_blobs(n_samples = 500, centers = 3)

"""
This is a test file

Here all the tests are done for the library

it is a mess, but dont worry about it
"""
