import numpy as np

# activation functions
def sigmoid(x, deriv=False):
    if deriv == True:
        return sigmoid(x) * (1 - sigmoid(x))
    return 1 / (1 + np.exp(-x))


def relu(x, deriv=False):
    if deriv == True:
        return (x > 0) * 1
    return np.maximum(0, x)


def tanh(x, deriv=False):
    if deriv == True:
        return 1 - np.power(np.tanh(x), 2)
    return np.tanh(x)


def softmax(x, deriv=False):
    if deriv == True:
        return 1
    e_x = np.exp(x)
    return e_x / e_x.sum(axis=1, keepdims=True)


# loss functions
def squared_loss(y_train, outputs):
    loss = 0.5 * np.power(y_train - outputs, 2)
    dloss = y_train - outputs
    return loss, dloss


def cross_entropy(y_train, outputs):
    x = np.log(1 - (y_train - outputs))
    loss = -np.sum(x) / y_train.shape[1]
    dloss = (y_train - outputs) / y_train.shape[1]
    return loss, dloss
