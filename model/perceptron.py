import numpy as np

class Perceptron:

    def __init__(self, activation_function='sigmoid', weights=None, bias=0):
        self.weights = np.array(weights) if weights is not None else None
        self.bias = bias
        self.set_activation_function(activation_function)  

    def set_activation_function(self, activation_function):
        # Validate and set the activation function
        activation_functions = {
            'sigmoid': self.sigmoid_function,
            'heaviside': self.hs_function
        }
        self.activation_function = activation_functions.get(activation_function)

    def set_weights(self, weights):
        self.weights = np.array(weights)

    def set_bias(self, b):
        self.bias = b

    # Sigmoid activation function
    def sigmoid_function(self, y):
        return 1 / (1 + np.exp(-y))

    # Heaviside step activation function
    def hs_function(self, y):
        return np.where(y >= 0, 1, 0)

    def predict(self, values):
        print(f"Predicting with values: {values}")
        # Turn input values to a numpy array
        vector = np.array(values)
        # Calculate the linear output
        linear_output = np.dot(vector, self.weights) + self.bias
        y_predicted = self.activation_function(linear_output)
        return y_predicted

    def get_output(self, vectors):
        # Get predictions for a list of vectors
        outputs = []
        for vector in vectors:
            outputs.append(self.predict(vector))
        return outputs