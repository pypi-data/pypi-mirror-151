import numpy as np

class _Accuracy:
    def _calc(self, preds, y):
        comparison = self.compare(preds, y)
        acc = np.mean(comparison)
        return acc