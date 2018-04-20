import random
from math import exp
from numpy import array, dot, eye, transpose
from numpy.linalg import inv


class Layer:
    def __init__(self, num, a):
        self.num_neurons = num
        self.nets = [0 for _ in range(num)]
        self.a_output = [0 for _ in range(num)]
        self.sensibility = [0 for _ in range(num)]
        self.weights = [[0 for _ in range(a)] for _ in range(num)]

    # inicializando los pesos con valores random entre -5 y 5
    def set_weights(self, ant):
        for n in range(self.num_neurons):
            for m in range(ant):
                self.weights[n][m] = round(random.uniform(-3, 3), 3)


# Cambia las deseadas 0, 1, 2 a [1,0,0], [0,1,0], [0,0,1]
def set_wish(entry):
    w = []
    for i in range(len(entry)):
        if entry[i] == 0:
            w.append([1, 0, 0])
        elif entry[i] == 1:
            w.append([0, 1, 0])
        elif entry[i] == 2:
            w.append([0, 0, 1])
    return w


# Cambia las salidas de [1,0,0], [0,1,0], [0,0,1] a 0, 1, 2
def get_wish(entry):
    w = entry.index(max(entry))
    return w


def d_o(d, o):
    e = []
    # "Resta de las listas"
    for i in range(len(d)):
        e.append(d[i] - o[i])
    return e


def take_of_bias(m):
    a = [0 for _ in range(len(m) - 1)]
    for j in range(1, len(m)):
        a[j - 1] = m[j]
    return a


class Multilayer:
    # constructor
    def __init__(self, lr, me, x, y, de, num_layers, num):

        self.num_layers = num_layers
        self.desired = set_wish(y)
        self.reachedMax = False
        self.desired_error = de
        self.learning_rate = lr
        self.num_neutrons = num
        self.time_errors = []
        self.max_epochs = me
        self.entries = x
        self.epochs = 0
        self.layer = []
        self.error = 0
        self.miow =0.01
        self.nu = 7.23
        #self.Levenberg_Marquart()
        self.start()

    # clasifica un nuevo set de puntos solo despues de ser entrenado
    def predict(self, test_set):
        outputs = self.forward(0, test_set)
        res = get_wish(outputs)
        return res

    # sigmoid
    def F(self, y):
        if y < 0:
            return 1 - 1 / (1 + exp(y))
        return 1 / (1 + exp(-y))

    def set_error(self, e):
        self.time_errors.append(e)

    # funcion de transferencia del perceptron
    def wa(self, x, w):
        p = 0.0
        for i in range(0, len(w)):
            p += w[i] * x[i]
        return p

    def set_weights(self):
        characteristics = 2
        for i in range(0, self.num_layers):
            self.layer.append(Layer(self.num_neutrons[i], characteristics + 1))
            self.layer[i].set_weights(characteristics + 1)
            characteristics = self.num_neutrons[i]

    def start(self):
        self.epochs = 0
        self.set_weights()  # Inicializa las layers y los pesos de las neuronas de 5 a -5
        self.error = self.desired_error + 1

        while self.error != self.desired_error and self.epochs < self.max_epochs:
            err_acumulado = 0
            for i in range(len(self.entries)):
                y = self.forward(i, self.entries)
                error = d_o(self.desired[i], y)
                err_acumulado += self.wa(error, error)
                self.backward_sensitivity(i)
                self.backward_weight_adjustment(i)
            self.error = err_acumulado / len(self.entries)
            self.set_error(err_acumulado)
            self.epochs = self.epochs + 1

        # si llego al maximo de epocas
        if self.epochs >= self.max_epochs:
            self.reachedMax = True
        else:
            self.reachedMax = False

    def forward(self, current, list_of_entries):
        a = list_of_entries[current]
        for i in range(self.num_layers):
            aux = []
            aux.append(-1)

            for j in range(self.num_neutrons[i]):
                self.layer[i].nets[j] = self.wa(a, self.layer[i].weights[j])
                self.layer[i].a_output[j] = self.F(self.layer[i].nets[j])
                aux.append(self.layer[i].a_output[j])
            a = aux
        return self.layer[i].a_output

    def backward_sensitivity(self, e):
        # Loop de capa de salida a la de entrada
        for i in range((self.num_layers - 1), -1, -1):
            # Loop de las neuronas en la capa
            for j in range(self.num_neutrons[i]):
                # Si es la capa de salida
                if i == self.num_layers - 1:
                    M = self.layer[i]
                    # Sensibility =    -2 * F'(n) * (d-a)
                    M.sensibility[j] = -2 * (self.F(M.nets[j]) * (1 - self.F(M.nets[j]))) * (
                            self.desired[e][j] - M.a_output[j])
                else:
                    s = 0
                    m = self.layer[i]
                    m_1 = self.layer[i + 1]
                    df = self.F(m.nets[j]) * (1 - self.F(m.nets[j]))
                    for k in range(self.num_neutrons[i + 1]):
                        w = take_of_bias(m_1.weights[k])
                        s += sum(m_1.sensibility[k] * array(df * array(w)))
                    m.sensibility[j] = s

    def backward_weight_adjustment(self, e):
        # Loop de las capas
        for i in range(self.num_layers):
            # Loop de las neuronas por capa
            for j in range(self.num_neutrons[i]):
                # Si es la primera capa
                if i == 0:
                    # Loop por pesos a ajustar
                    for k in range(3):
                        increment_of_weight = -self.learning_rate * self.layer[i].sensibility[j] * self.entries[e][k]
                        self.layer[i].weights[j][k] += increment_of_weight

                else:
                    # Loop por pesos a ajustar
                    for k in range(self.num_neutrons[i - 1] + 1):
                        if k == 0:
                            increment_of_weight = -self.learning_rate * self.layer[i].sensibility[j] * -1
                        else:
                            increment_of_weight = -self.learning_rate * self.layer[i].sensibility[j] * self.layer[i - 1].a_output[
                                k - 1]
                        self.layer[i].weights[j][k] += increment_of_weight

    def Levenberg_Marquart(self):
        self.epochs = 0
        self.set_weights()  # Inicializa las layers y los pesos de las neuronas
        self.error = self.desired_error + 1

        while self.error != self.desired_error and self.epochs < self.max_epochs:
            err_acumulado = 0
            for i in range(len(self.entries)):
                y = self.forward(i, self.entries)

                error = d_o(self.desired[i], y)
                e =self.wa(error, error)
                err_acumulado +=e

                if self.miow < 1:
                    self.Levenber_sensitivity(i,e)
                    y = self.forward(i, self.entries)
                    Enew = d_o(self.desired[i], y)
                    Enew = self.wa(Enew, Enew)
                else:
                    self.backward_sensitivity(i)
                    self.backward_weight_adjustment(i)
                    Enew = e+1



                if Enew < e:
                    # Optimization Step successful!
                    self.miow = self.miow / self.nu # adapt scale factor
                else:
                    # Optimization Step NOT successful!
                    self.miow = self.miow * self.nu  # adapt scale factor
                self.error = err_acumulado / len(self.entries)
                self.set_error(err_acumulado)
                self.epochs = self.epochs + 1



    def Levenber_sensitivity(self, e,error):
        # Loop de las capas
        for i in range(self.num_layers):
            # Loop de las neuronas por capa
            for j in range(self.num_neutrons[i]):
                M = self.layer[i]
                J = (self.F(M.nets[j]) * (1 - self.F(M.nets[j])))
                JJ = dot(transpose(J), J)
                g = dot(J,error)
                G = inv(JJ + self.miow* eye(len(M.weights[j]))) # scaled inverse hessian
                w_delta = dot(-G, g)
                lenm=len(M.weights[j])
                print("delta   ",w_delta)

                if i == 0:
                    for k in range(3):
                        self.layer[i].weights[j][k] += w_delta[k]
                else:
                    # Loop por pesos a ajustar
                    for k in range(self.num_neutrons[i - 1] + 1):
                        self.layer[i].weights[j][k] += w_delta[k]

