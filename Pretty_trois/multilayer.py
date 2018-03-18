import random
from math import exp
from numpy import transpose


class Layer:

    def __init__(self, num):

        self.num_neu = num
        self.weights = [[0 for x in range(3)] for y in range(num)]
        self.nets =[0 for x in range(num)]
        self.a_output =[0 for x in range(num)]
        self.sensibility=[0 for x in range(num)]

    def set_weigths(self):
        for n in range(self.num_neu):
            for m in range(3):
                self.weights[n][m] =(random.uniform(-5, 5))





class multilayer:
    # constructor
    def __init__(self, lr, me, x, y, de, num_layers, num ):
        self.desired_error = de
        self.error = 0
        self.layer = []
        self.learning_rate = lr
        self.max_epochs = me
        self.num_layers =num_layers+1 #Para agregar la capa de salida
        num.append(3)
        self.num_neu = num
        self.epochs = 0
        self.entries = x
        self.desired = y
        self.weights = []
        self.time_errors = []
        self.start()

    # sigmoid
    def F(self, y):
        return 1 / (1 + exp(-y))

    def set_error(self,e):
        self.time_errors.append(e)

    # funcion de transferencia del perceptron
    def wa(self, x,w):
        p = 0.0
        for i in range(0, len(w)):
            p += w[i] * x[i]
        return p

    def start(self):
        # inicializando los pesos con valores random entre -5 y 5
        for i in range(0, self.num_layers):
           self.layer.append(Layer(self.num_neu[i]))
           self.layer[i].set_weigths()

        self.epochs = 0
        # para que sea un error diferente al inicio#
        self.error = self.desired_error + 1
        while (self.error != self.desired_error and self.epochs < self.max_epochs):
            errAcumulado = 0
            for i in range(0, len(self.entries)):
                errAcumulado =self.forward(i, errAcumulado)
                self.backward_s(i)
                self.backward_a(i)
                self.error = errAcumulado / len(self.entries)
                self.set_error(errAcumulado)
                print(self.error)
                self.epochs+=1


    def forward(self,e,errAcumulado):
        a=self.entries[e]
        for i in range(self.num_layers):
            a2 = []
            a2.append(-1)
            for j in range(self.num_neu[i]):
                self.layer[i].nets[j]= self.wa(a, self.layer[i].weights[j])
                self.layer[i].a_output[j] = self.desired[e] - self.F(self.layer[i].nets[j])
                errAcumulado += self.layer[i].a_output[j]
                a2.append(self.layer[i].a_output[j])
            a=a2
        return errAcumulado

    def backward_s(self,e):
        for i in range((self.num_layers-1),0, -1):
            for j in range(self.num_neu[i]):
                if(i==self.num_layers-1):
                    M=self.layer[i]
                    M.sensibility[j]= -2*(self.F(M.nets[j]) * (1 - self.F(M.nets[j])))*(self.desired[e]-M.a_output[j])
                else:
                    m=self.layer[i]
                    df = self.F(m.nets[j]) * (1 - self.F(m.nets[j]))
                    for k in range (self.num_neu[i+1]):
                        m.sensibility[j] += df*(transpose(self.layer[i+1].weights[k][i]))* self.layer[i+1].sensibility[k]

    def backward_a(self,e):
        for i in range(self.num_layers):
            for j in range(self.num_neu[i]):
                for k in range(3):
                    if (i==0):
                        incW =  -self.learning_rate*self.layer[i].sensibility[j]*self.entries[e][k]
                        self.layer[i].weights[j][k]+= incW
                    else:
                        if(k==0):
                            incW = -self.learning_rate * self.layer[i].sensibility[j] * -1
                        else:
                            incW = -self.learning_rate * self.layer[i].sensibility[j] *self.layer[i-1].a_output[k-1]
                        self.layer[i].weights[j][k] += incW













