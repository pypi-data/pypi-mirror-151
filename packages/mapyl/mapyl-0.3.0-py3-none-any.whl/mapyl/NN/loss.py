import numpy as np

class _Loss:
    def _train_layers(self, train_layers: np.ndarray):
        self.train_layers = train_layers

    def _calculate(self, output, y):
        sample = self._forward(output, y)
        data_loss = np.mean(sample)
        return data_loss

class CatCrossEntr(_Loss):
    """Categorical Cross Entropy loss object"""
    def _forward(self, y_hat, y, training=None):
        num_samples = len(y_hat)
        y_hat_clip = np.clip(y_hat, 1.0e-7,1- 1.0e-7)
        if len(y.shape) == 1:
            confidence = y_hat_clip[range(num_samples), y]
        elif len(y.shape) >= 2:
            confidence = np.sum(
            y_hat_clip * y, axis=1)
        neg_log_prob = -np.log(confidence)
        return neg_log_prob
    
    def _backward(self, dvalues, y):
        samples = len(dvalues)
        labels = len(dvalues[0])
        if len(y.shape) == 1:
            y = np.eye(labels)[y]
        self.dinputs = -y / dvalues
        self.dinputs = self.dinputs / samples