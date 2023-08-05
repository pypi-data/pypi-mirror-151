import numpy as np

class Dense:
    """
    Dense layer instance
    
    Parameters:
        num_inputs (int): The number of inputs (neurons of the previous layer or the model inputs)

        num_neurons (int): The number of neurons of the layer (also teh number of outputs)
    """
    def __init__(self, num_inputs, num_neurons):
        self.weights = 0.01*np.random.randn(num_inputs,num_neurons)
        self.biases = np.zeros((1, num_neurons))

    def _forward(self, inputs, training):
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases

    def _backward(self, dvalues):
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = np.dot(dvalues, self.weights.T)

class Dropout:
    """
    Dropout layer class, deactivates neurons according to rate

    Parameter: 
        rate (float): the percentage of deactivated neurons
    """
    def __init__(self, rate):
        self.rate = 1-rate

    def _forward(self, inputs, training):
        self.inputs = inputs

        if not training:
            self.output = inputs.copy()
            return

        self.bin_mask = np.random.binomial(1, self.rate, inputs.shape) / self.rate
        self.output = inputs * self.bin_mask

    def _backward(self, dvalues):
        self.dinputs = dvalues * self.bin_mask

class _Input:
    """Placeholder input class, internal use"""
    def _forward(self, inputs, training):
        self.output = inputs