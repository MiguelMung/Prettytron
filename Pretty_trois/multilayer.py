import random
from math import exp
from numpy import array

class Layer:
    def __init__(self, num, ant):
        a=ant+1
        self.num_neu = num
        self.weights = [[0 for x in range(a)] for y in range(num)]
        self.nets =[0 for x in range(num)]
        self.a_output =[0 for x in range(num)]
        self.sensibility=[0 for x in range(num)]

    def set_weigths(self,ant):
        for n in range(self.num_neu):
            for m in range(ant+1):
                self.weights[n][m] =round(random.uniform(-5, 5),5)

class multilayer:
    # constructor
    def __init__(self, lr, me, x, y, de, num_layers, num):
        self.reachedMax = False
        self.desired_error = de
        self.error = 0
        self.layer = []
        self.learning_rate = lr
        self.max_epochs = me
        self.num_layers = num_layers + 1 #Para agregar la capa de salida
        num.append(3)
        self.num_neu = num
        self.epochs = 0
        self.entries = x
        self.desired = self.set_whist(y)
        self.weights = []
        self.time_weights = []
        self.time_errors = []
        self.start()

    def set_whist(self, entry):
        w = []
        for i in range(len(entry)):
            if entry[i] == 0:
                w.append([1, 0, 0])
            elif entry[i] == 1:
                w.append([0, 1, 0])
            elif entry[i] == 2:
                w.append([0, 0, 1])
        return (w)

    def get_whist(self, entry):
        w=entry.index(max(entry))
        return w



    # clasifica un nuevo set de puntos solo despues de ser entrenado
    def predict(self,set):
        outputs = self.forward(0, set)
        res=self.get_whist(outputs)
        #print(self.desired)
        return res

    def d_o(self, d,o):
        e=[]
        #"Resta de las listas"
        for i in range(len(d)):
            e.append(d[i] - o[i])
        return e

    def _bias(self,m):
        a = [0 for x in range(len(m) - 1)]
        for j in range(1, len(m)):
            a[j - 1] = m[j]
        return a

    # sigmoid
    def F(self, y):
        if y < 0:
            return 1 - 1 / (1 + exp(y))
        return 1 / (1 + exp(-y))

    def set_error(self,e):
        self.time_errors.append(e)

    # funcion de transferencia del perceptron
    def wa(self, x, w):
        p = 0.0
        for i in range(0, len(w)):
            p += w[i] * x[i]
        return p

    def start(self):
        # inicializando los pesos con valores random entre -5 y 5
        car =2
        for i in range(0, self.num_layers):
           self.layer.append(Layer(self.num_neu[i],car))
           self.layer[i].set_weigths(car)
           car=self.num_neu[i]




        self.epochs = 0
        # para que sea un error diferente al inicio#
        self.error = self.desired_error + 1
        u=0
        while self.error != self.desired_error and self.epochs < self.max_epochs:
            errAcumulado = 0
            for i in range(0, len(self.entries)):
                y=self.forward(i, self.entries)
                e=self.d_o(self.desired[i],y)
                errAcumulado+=self.wa(e,e)
                self.backward_s(i)
                self.backward_a(i)
            self.error = errAcumulado / len(self.entries)
            self.set_error(errAcumulado)
            self.epochs = self.epochs + 1
        #si llego al maximo de epocas
        if self.epochs >= self.max_epochs:
            self.reachedMax = True
        else:
            self.reachedMax = False

    def forward(self, e, entries):
        a = entries[e]
        for i in range(self.num_layers):
            a2 = []
            a2.append(-1)
            for j in range(self.num_neu[i]):
                self.layer[i].nets[j]= self.wa(a, self.layer[i].weights[j])
                self.layer[i].a_output[j] = self.F(self.layer[i].nets[j])
                a2.append(self.layer[i].a_output[j])
            a = a2
        return self.layer[i].a_output

    def backward_s(self, e):
        for i in range((self.num_layers-1),-1,-1):
      #  for i in range((self.num_layers - 1), 0, -1):
            for j in range(self.num_neu[i]):
                if i == self.num_layers - 1:
                    M = self.layer[i]
                    M.sensibility[j] = -2*(self.F(M.nets[j]) * (1 - self.F(M.nets[j])))*(self.desired[e][j]-M.a_output[j])
                else:
                    s=0
                    m = self.layer[i]
                    df = round(self.F(m.nets[j]) * (1 - self.F(m.nets[j])), 15)
                    for k in range(self.num_neu[i + 1]):
                        w = self._bias(self.layer[i + 1].weights[k])
                        s +=sum(self.layer[i+1].sensibility[k]*array(df*array(w)))
                    m.sensibility[j]=s

    def backward_a(self, e):
        for i in range(self.num_layers):
            for j in range(self.num_neu[i]):
                    if i == 0:
                        for k in range(3):
                            incW = -self.learning_rate*self.layer[i].sensibility[j]*self.entries[e][k]
                            self.layer[i].weights[j][k] = self.layer[i].weights[j][k]+ incW

                    else:
                        for k in range(self.num_neu[i-1]+1):
                            if k == 0:
                                incW = -self.learning_rate * self.layer[i].sensibility[j] * -1
                            else:
                                incW = -self.learning_rate * self.layer[i].sensibility[j] *self.layer[i-1].a_output[k-1]
                            self.layer[i].weights[j][k] += incW
