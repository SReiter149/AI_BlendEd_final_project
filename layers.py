# path = "/Users/sam/Documents/personalstuff/coding/python/neuralnetwork"
import sys

# sys.path.append(path)
import numpy as np
from scipy.signal import convolve
import math

print(f"seed is {np.random.get_state()[1][0]}")
from functions import *


class FC_Layer:
    # fully connected layer
    def __init__(self, shape, bias_true=True, activation=sigmoid):
        # setting up the network based on size
        # using a bias is still broken so not being used
        self.weights = np.random.randn(shape[0], shape[1]) * 0.2
        self.bias_true = bias_true
        if self.bias_true == True:
            self.bias = np.random.randn(shape[1]) * 0.2
        self.activation = activation

    def forward_prop(self, input, test=False):
        # saving input to use in back_prop
        self.input = input

        # dotting the input and weights
        self.output = np.array(np.matmul(self.input, self.weights))

        # adding bias BROKEN
        if self.bias_true:
            self.output = np.add(self.output, self.bias)

        # activating output
        self.output = self.activation(self.output)
        return self.output

    def back_prop(self, dloss, LR=0.01):
        # setting up the shapes of the matrixes for back_prop
        self.input = self.input.reshape(-1, 1)
        dloss = np.array(dloss).reshape(-1, 1)

        # back_prop through activation layer
        dloss = np.multiply(
            dloss, self.activation(self.output, deriv=True).reshape(-1, 1)
        )

        # adding loss to weights
        self.weights += np.dot(self.input, dloss.T) * LR

        # adding loss to weights
        if self.bias_true:
            self.bias = np.add(np.sum(dloss, axis=0, keepdims=True), self.bias)

        # returning updated dloss for next layer
        dloss = np.dot(self.weights, dloss)
        return dloss


# not used because we just lumped this all into the FC_layer
class Activation_Layer:
    def __init__(self, activation=sigmoid):
        self.activation = activation

    def forward_prop(self, input, test=False):
        self.input = input
        output = self.activation(self.input)
        return output

    def back_prop(self, dloss, LR=None):
        temp = self.activation(self.input, deriv=True).reshape(-1, 1)

        output = np.multiply(temp, dloss)

        return output


# not enough connections to make this nessessay, used it a bit when we had a larger network
class Drop_Out_Layer:
    def __init__(self, keep_prob=0.8):
        self.keep_prob = keep_prob

    def forward_prop(self, input, test=False):
        if test == True:
            return input
        else:
            self.mask = np.random.random((1, input.shape[1]))
            self.mask = self.mask < self.keep_prob
            output = np.multiply(input, self.mask) / self.keep_prob
            return output

    def back_prop(self, dloss, LR=None):
        dloss = np.multiply(dloss, self.mask) / self.keep_prob
        return dloss


# attempt at a convolutional approach by just showing it the screen and allowing the neural network to identify what was happening, but became too complex
class Conv_Layer:
    def __init__(
        self, filt_shape, weights, bias
    ):  # filt_shape = [num_filts,num_channels, filt_x, filt_y]
        self.weights = weights
        self.bias = bias

    def forward_prop(
        self, input, test=False
    ):  # inputs = [num_images, num_layers, layer_x, layer_y]
        output = np.zeros(
            (
                input.shape[0],
                self.weights.shape[0],
                input.shape[2] - self.weights.shape[1] + 1,
                input.shape[3] - self.weights.shape[2] + 1,
            )
        )
        for i in range(input.shape[0]):
            for j in range(self.weights.shape[0]):
                for k in range(input.shape[1]):
                    output[i, k] += convolve(input[i, k], self.weights[j], mode="valid")
                output[i, k] /= input.shape[1]
        return output


class Max_pooling:
    def __init__(self, size, step_size=2):
        """
        size = 2d array (x,y)
        step_size = int
        """
        self.size = size
        self.step_size = step_size

    def forward_prop(self, input, test=False):
        output = np.zeros(
            (
                input.shape[0],
                input.shape[1],
                int(math.ceil(input.shape[2] / 2)),
                int(math.ceil(input.shape[3] / 2)),
            )
        )
        for i in range(0, input.shape[2], self.step_size):
            for j in range(0, input.shape[3], self.step_size):
                subsection = input[:, :, i : i + self.size[0], j : j + self.size[1]]
                output[:, :, i // self.step_size, j // self.step_size] = np.amax(
                    subsection, axis=(2, 3)
                )
        return output


class flattening:
    def __init__(self):
        self.shape = None

    def forward_prop(self, input, test=False):
        self.shape = input.shape
        return input.reshape((input.shape[0], -1))

    def back_prop(self):
        pass
