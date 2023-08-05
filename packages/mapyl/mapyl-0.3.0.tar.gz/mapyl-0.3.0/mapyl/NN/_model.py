import numpy as np
from .layers import _Input
from ._acc import _Accuracy
from .activations import SoftMax, _SoftMaxLoss
from .loss import CatCrossEntr

class Model:
    """
    Model for sequential, fully connected layers

    Returns:
        self:  The Model class
    """
    def __init__(self):
        self.layers = []
        self.acc = ClassAccuracy()
        self.softmax_classifier_output = None
    
    def add(self, layer):
        """adds a layer to the layer list"""
        self.layers.append(layer)

    def finalize(self,*,loss, optimizer):
        """
        Finalizes the model, adds loss and optimizer

        parameters:
            loss (Loss): Loss object
            
            optimizer (Optimizer): Optimizer object

        Returns:
            self: the finalized Model object
        """
        self.loss = loss
        self.optimizer = optimizer

        self.input_layer = _Input()
        layer_count = len(self.layers)

        self.train_layers = []

        for i in range(layer_count):
            if i == 0:
                self.layers[i].prev = self.input_layer
                self.layers[i].next = self.layers[i+1]

            elif i < layer_count - 1:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.layers[i+1]
            else:
                self.layers[i].prev = self.layers[i-1]
                self.layers[i].next = self.loss
                self.output_layer_activation = self.layers[i]
        
            if hasattr(self.layers[i], 'weights'):
                self.train_layers.append(self.layers[i])

            self.loss._train_layers(self.train_layers)

        if isinstance(self.layers[-1], SoftMax) and isinstance(self.loss, CatCrossEntr):
            self.softmax_classifier_output = _SoftMaxLoss()
        return self
    
    def fit(self,X, y, epochs, validation_data=None, verbose=0):
        """
        trains and validades the Model instance

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input

            y (ndarray): ndarray of shape (num_samples, num_features) of the input

            epochs (int): The number of epochs

            validation_data (tuple): Validation data of shape (X ndarray , y ndarray). Defaults to None.

            verbose (int): The verbose, can be 0, 1 and 2. Defaults to 0.

        Returns:
            self: The fitted instance
        """
        for epoch in range(1, epochs+1):
            output = self._forward(X, training = True)
            loss = self.loss._calculate(output, y)
            preds = self.output_layer_activation._preds(output)
            accuracy = self.acc._calc(preds, y)

            if verbose ==1:
                if not epoch% 10:
                    print(f'epoch: {epoch} ' + f'accuracy: {accuracy} ' + f'loss: {loss} ')
            elif verbose == 2:
                if not epoch% 10:
                    print(f'epoch: {epoch} ' + f'accuracy: {accuracy} ' + f'loss: {loss} ' + f'learning rate: {self.optimizer.curr_lr} ')

        
            self._backward(output, y)

            self.optimizer._pre_update_params()
            for layer in self.train_layers:
                self.optimizer._update(layer)
            self.optimizer._post_update_params()

        if validation_data is not None:
            X_val, y_val = validation_data

            output = self._forward(X_val, training=False)

            loss = self.loss._calculate(output, y_val)

            predictions = self.output_layer_activation._preds(output)

            accuracy = self.acc._calc(predictions, y_val)

            print(f'validation pass, ' + f'acc: {accuracy}, ' + f'loss: {loss}')

        return self
        

    def _forward(self, X, training):
        self.input_layer._forward(X, training)

        for layer in self.layers:

            layer._forward(layer.prev.output, training)

        return layer.output
    
    def _backward(self, output, y):
        if self.softmax_classifier_output is not None:

            self.softmax_classifier_output._backward(output, y)

            self.layers[-1].dinputs = self.softmax_classifier_output.dinputs

            for layer in reversed(self.layers[:-1]):
                layer._backward(layer.next.dinputs)

            return

        self.loss._backward(output, y)

        for layer in reversed(self.layers):
            layer._backward(layer.next.dinputs)

class ClassAccuracy(_Accuracy):
    def compare(self, preds, y):
        if len(y.shape) == 2:
            y = np.argmax(y, axis=1)
        
        return preds==y
