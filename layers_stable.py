# path = "/Users/sam/Documents/personalstuff/coding/python/neuralnetwork"
import sys

# sys.path.append(path)
import numpy as np
from functions_stable import *


class FC_Layer:
    def __init__(self, shape, bias_true=True, activation=sigmoid):
        self.weights = np.random.randn(shape[0], shape[1]) * 0.2
        self.bias_true = bias_true
        if self.bias_true == True:
            self.bias = np.random.randn(1, shape[1]) * 0.2
        print(self.weights.shape, f"bshape is {self.bias.shape}")

    def forward_prop(self, input, test=False):
        self.input = input
        #self.output = np.swapaxes(np.matmul(self.input, self.weights), 1, 0)
        self.output = np.array([np.matmul(self.input, self.weights)])
        print(f"weights is {self.weights.shape}, dot shape: {self.output.shape}, input is {self.input.shape}")# (150,4), (4,1), out = (150,1)
        if self.bias_true:
            self.output += self.bias
        return self.output

    def back_prop(self, dloss, LR=0.01):
        self.weights += LR * np.dot(self.input.T, dloss)
        if self.bias_true:
            self.bias += LR * np.sum(
                dloss, axis=0, keepdims=True
            )  # mess with sum vs mean here
        dloss = np.dot(dloss, self.weights.T)  # ????? is this line nessessary?
        return dloss


class Activation_Layer:
    def __init__(self, activation=sigmoid):
        self.activation = activation

    def forward_prop(self, input, test=False):
        self.input = input
        output = self.activation(self.input)
        return output

    def back_prop(self, dloss, LR=None):
        return dloss * self.activation(self.input, deriv=True)


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
    
