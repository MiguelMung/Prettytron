import random
from math import exp


class Adaline:
    # constructor
    def __init__(self, lr, me, x, y, de):
        self.desired_error = de
        self.error = 0
        self.learning_rate = lr
        self.max_epochs = me
        self.epochs = 0
        self.entries = x
        self.desired = y
        self.weights = []
        self.time_weights = []
        self.time_errors = []
        self.nonlinear = False
        self.start()

    # funcion de transferencia del perceptron
    def wx(self, x):
        p = 0.0
        for i in range(0, len(self.weights)):
            p += self.weights[i] * x[i]
        return p

    def incW(self, E, y, x):
        inc = (self.learning_rate * 2) * E * self.F(y) * (1 - self.F(y)) * x
        return inc
    # sigmoid
    def F(self, y):
        return 1 / (1 + exp(-y))

    # funcion de transferencia
    def Pw(self, x):
        pw = 0
        if self.wx(x) >= 0:
            pw = 1
        return pw

    # clasifica un nuevo set de puntos solo despues de ser entrenado
    def clasify(self, new_points):
        clases = []
        if len(self.weights) != 0:
            for p in new_points:
                clases.append(self.Pw(p))
        return clases

    def set_time(self, a, b, c):
        self.time_weights.append((a, b, c))

    def set_error(self,e):
        self.time_errors.append(e)

    def start(self):
        # inicializando los pesos con valores random entre -5 y 5
        self.weights = []
        for i in self.entries[0]:
            self.weights.append(random.uniform(-5, 5))
        self.time_weights = []
        print("Pesos iniciales:")
        print(self.weights)
        self.epochs = 0
        #para que sea un error diferente al inicio#
        self.error = self.desired_error+1
        while (self.error != self.desired_error and self.epochs < self.max_epochs):
            self.set_time(self.weights[0], self.weights[1], self.weights[2])
            errAcumulado = 0
            for i in range(0, len(self.entries)):
                # obteniendo el error
                y = self.wx(self.entries[i])
                error = self.desired[i] - self.F(y)
                errAcumulado += error

                # ajustando los pesos
                for j in range(0, len(self.weights)):
                    self.weights[j] = self.weights[j] + self.incW(error, y, self.entries[i][j])

            self.error = errAcumulado/len(self.entries)
            self.set_error(errAcumulado)
            self.epochs += 1
        print("Pesos Finales:")
        print(self.weights)
        self.set_time(self.weights[0], self.weights[1], self.weights[2])
        if self.epochs >= self.max_epochs:
            self.nonlinear = True
        else:
            self.nonlinear = False
