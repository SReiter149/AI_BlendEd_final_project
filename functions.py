# import nessessary files
import numpy as np

# activation function of choice
def tanh(x, deriv=False):
    # function of choice because it reduces the magnitude of the numbers whiles preserving their sign
    if deriv == True:
        return 1 - np.power(np.tanh(x), 2)
    return np.tanh(x)


# loss function of choice
def pong_loss(state, move):
    # state: [paddle x, paddle y, ball x, ball y, ball direction x, ball direction y, moves]

    # get magnitude of the error
    error = abs(state[1] - state[3])

    # get the expected move
    # I realize this isn't supposed to be allowed, you are supposed to give it rewards based off tasks not give it the exact move but this is a good first step
    expected = np.sign(state[1] - state[3])

    # get the sign of the actual move
    move = np.sign(move)

    # I realize this isn't the exact integral of dloss but its close enough and fine for visualization purposes
    loss = 2 * error**2

    # our best guess at a good dloss
    if expected == move:
        # reward on correct move
        dloss = error
    else:
        # punishment on incorrect move
        dloss = error * -1

    # return dloss as a matrix
    dloss = np.array([dloss])

    return loss, dloss


# other activation functions we tried
def sigmoid(x, deriv=False):
    if deriv == True:
        return sigmoid(x) * (1 - sigmoid(x))
    return 1 / (1 + np.exp(-x))


def relu(x, deriv=False):
    if deriv == True:
        return (x > 0) * 1
    return np.maximum(0, x)


def softmax(x, deriv=False):
    if deriv == True:
        return 1
    e_x = np.exp(x)
    return e_x / e_x.sum(axis=1, keepdims=True)


# other loss functions we tried
def squared_loss(y_train, outputs):
    loss = 0.5 * np.power(y_train - outputs, 2)
    dloss = y_train - outputs
    return loss, dloss


def cross_entropy(y_train, outputs):
    x = np.log(1 - (y_train - outputs))
    loss = -np.sum(x) / y_train.shape[1]
    dloss = (y_train - outputs) / y_train.shape[1]
    return loss, dloss
