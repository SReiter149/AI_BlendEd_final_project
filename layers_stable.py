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
        self.activation = activation
        print(self.activation)


    def forward_prop(self, input, test=False):
        self.input = input
       
        self.output = np.array(np.matmul(self.input, self.weights))
        
        if self.bias_true:
            self.output = np.add(self.output, self.bias)
        self.output = self.activation(self.output)
        return self.output

    def back_prop(self, dloss, LR=0.01):
        self.input = self.input.reshape(-1,1)
        dloss = np.array(dloss).reshape(-1,1)
        dloss = np.multiply(dloss, self.activation(self.output, deriv = True).reshape(-1,1))
        # print(dloss.T)

        #print(f"update: {np.dot(self.input, dloss.T).reshape(1,-1) * LR}")
        self.weights +=np.dot(self.input, dloss.T) * LR
        # print(f"weights {self.weights.reshape(1,-1)}")
        # print(f"update {np.dot(self.input, dloss.T) * LR}")
        if self.bias_true:
            self.bias = np.add(np.sum( #add LR back here, took it out bc its a matrix not a scalar for some reason
                dloss, axis=0, keepdims=True
            ), self.bias)  # mess with sum vs mean here
        dloss = np.dot(self.weights,dloss)
        return dloss


class Activation_Layer:
    def __init__(self, activation=sigmoid):
        self.activation = activation

    def forward_prop(self, input, test=False):
        self.input = input
        output = self.activation(self.input)
        return output

    def back_prop(self, dloss, LR=None):
        return dloss
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
    
