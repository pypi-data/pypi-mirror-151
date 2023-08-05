import numpy as np
from .loss import CatCrossEntr
from .loss import _Loss


class ReLU:
    """Rectified Linear Unit activation funtion"""
    def _forward(self, inputs, training):
        self.inputs = inputs
        self.output = np.maximum(0, inputs)

    def _backward(self, dvalues):
        self.dinputs = dvalues.copy()
        self.dinputs[self.inputs <= 0] = 0

class SoftMax:
    """
    SoftMax activation function, classifies the inputs
    and returns confidence scores for each class
    """
    def _forward(self, inputs, training=None):
        self.inputs = inputs
        exp = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probs = exp/np.sum(exp, axis=1, keepdims=True)
        self.output = probs
    
    def _backward(self, dvalues):
        self.dinputs = np.empty_like(dvalues)

        for index, (single_output, single_dvalues) in enumerate(zip(self.output, dvalues)):
            single_output = single_output.reshape(-1, 1)
            jacobian_matrix = np.diagflat(single_output) - np.dot(single_output, single_output.T)
            self.dinputs[index] = np.dot(jacobian_matrix, single_dvalues)
    
    def _preds(self, outputs):
        return np.argmax(outputs, axis=1)


class _SoftMaxLoss():
    """Classifier activation function along with loss calculator, internal use"""
    def _backward(self, dvalues, y):
        samples = len(dvalues)
        if len(y.shape) == 2:
            y = np.argmax(y, axis=1)
        self.dinputs = dvalues.copy()
        self.dinputs[range(samples), y] -= 1
        self.dinputs = self.dinputs / samples