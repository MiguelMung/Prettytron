import random

from numpy.ma import dot


class Perceptron:
    #constructor
    def __init__(self,lr,me,x,y,window):
        self.learning_rate = lr
        self.max_epochs = me
        self.epochs = 0
        self.entries = x
        self.desired = y
        self.weights = []
        self.time_weights = []
        self.nonlinear = False
        self.start(window)

    #funcion de transferencia
    def Pw(self,x):
        pw = 0
        wx = 0.0
        re = dot(self.weights, x)

        '''for i in range(0, len(self.weights)):
            wx += self.weights[i]*x[i]
                #umbral
        print(pw)'''

        if re >= 0:
            pw = 1
        return pw
    #clasifica un nuevo set de puntos solo despues de ser entrenado
    def clasify(self, new_points):
        clases = []
        if len(self.weights) != 0:
            for p in new_points:
                clases.append(self.Pw(p))
        return clases

    def set_time(self, a,b,c):
        self.time_weights.append((a,b,c))

    def start(self, window):
        #inicializando los pesos con valores random entre -5 y 5
        self.weights = []
        for i in self.entries[0]:
            self.weights.append(random.uniform(-5, 5))
        done = False
        self.time_weights = []
        print("Pesos iniciales:")
        print(self.weights)
        self.epochs = 0
        while(not done and self.epochs < self.max_epochs):
            done = True
            self.set_time(self.weights[0],self.weights[1],self.weights[2])
            for i in range(0,len(self.entries)):
                #obteniendo el error
                error = self.desired[i] - self.Pw(self.entries[i])
                if error != 0:
                    done = False
                    #ajustando los pesos
                    for j in range(0, len(self.weights)):
                        self.weights[j] = self.weights[j] + self.learning_rate*error*self.entries[i][j]
            self.epochs += 1
        print("Pesos Finales:")
        print(self.weights)
        self.time_weights.append(self.weights)
        if not done:
            self.nonlinear = True
        else:
            self.nonlinear = False