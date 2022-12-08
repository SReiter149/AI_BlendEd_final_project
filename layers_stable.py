# path = "/Users/sam/Documents/personalstuff/coding/python/neuralnetwork"
import sys

# sys.path.append(path)
import numpy as np
print(f"seed is {np.random.get_state()[1][0]}")
from functions_stable import *


class FC_Layer:
    def __init__(self, shape, bias_true=True, activation=sigmoid):
        self.weights = np.random.randn(shape[0], shape[1]) * 0.2
        self.bias_true = bias_true
        if self.bias_true == True:
            self.bias = np.random.randn(shape[1]) * 0.2

        #print(self.weights.shape, f"bshape is {self.bias.shape}")

    def forward_prop(self, input, test=False):
        self.input = input
        #self.output = np.swapaxes(np.matmul(self.input, self.weights), 1, 0)
        self.output = np.array(np.matmul(self.input, self.weights))
        # print(f"weights is {self.weights.shape}, dot shape: {self.output.shape}, input is {self.input.shape}, bias is {self.bias.shape}")# (150,4), (4,1), out = (150,1)

        if self.bias_true:
            self.output = np.add(self.output, self.bias)
        # print(f"weights is {self.weights.shape}, dot shape: {self.output.shape}, input is {self.input.shape}, output is {self.output.shape}")# (150,4), (4,1), out = (150,1)
        return self.output

    def back_prop(self, dloss, LR=0.01):
        self.input = self.input.reshape(-1,1)
        dloss = np.array(dloss).reshape(-1,1)
        # print(self.weights.shape, dloss.shape, self.input.shape)
        self.weights +=np.dot(self.input, dloss.T)
        if self.bias_true:
            self.bias = np.add(np.sum( #add LR back here, took it out bc its a matrix not a scalar for some reason
                dloss, axis=0, keepdims=True
            ), self.bias)  # mess with sum vs mean here

        dloss = np.dot(self.weights,dloss)
        # print(self.weights.shape, dloss.shape, self.input.shape)  
        return dloss


class Activation_Layer:
    def __init__(self, activation=sigmoid):
        self.activation = activation

    def forward_prop(self, input, test=False):
        self.input = input
        output = self.activation(self.input)
        return output

    def back_prop(self, dloss, LR=None):
        temp = self.activation(self.input, deriv=True).reshape(-1,1)

        output = np.multiply(temp, dloss)

        return  output

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
    
