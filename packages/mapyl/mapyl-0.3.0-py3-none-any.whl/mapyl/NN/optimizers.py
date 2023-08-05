import numpy as np

class SGDOptimizer:
    """
    Stochastic Gradient Descent optimizer

    Parameters:
        lr (float): The learning rate
        decay (float): The decay of the learning rate 
        momentum (float): The momentum of the learning rate
    """
    def __init__(self, lr=0.1, decay = 0, momentum = 0):
        self.lr = lr
        self.curr_lr = lr
        self.decay = decay
        self.iters = 0
        self.momentum = momentum

    def _pre_update_params(self):
        if self.decay:
            self.curr_lr = self.lr * (1. / (1. + self.decay * self.iters))

    def _update(self, layer):
        if self.momentum:
            if not hasattr(layer, 'weight_momentums'):
                layer.weight_momentums = np.zeros_like(layer.weights)
                layer.bias_momentums = np.zeros_like(layer.biases)
            weight_updates = self.momentum * layer.weight_momentums - self.curr_lr * layer.dweights
            layer.weight_momentums = weight_updates

            bias_updates = self.momentum * layer.bias_momentums - self.curr_lr * layer.dbiases
            layer.bias_momentums = bias_updates

        else:
            weight_updates = -self.curr_lr * layer.dweights
            bias_updates = -self.curr_lr * layer.dbiases
    
        layer.weights +=  weight_updates
        layer.biases +=  bias_updates

        
    def _post_update_params(self):
        self.iters += 1

