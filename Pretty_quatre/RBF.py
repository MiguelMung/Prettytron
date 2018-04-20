import random
from math import sqrt

from numpy.core.defchararray import index
from numpy import sum, asarray


class Layer:
    def __init__(self, num, a):
        self.num_neurons = num
        self.nets = [0 for _ in range(num)]
        self.a_output = [0 for _ in range(num)]
        self.weights = [[0 for _ in range(a)] for _ in range(num)]
        self.range = [0 for _ in range(num)]

    # inicializando los pesos con valores random entre -5 y 5
    def set_weights(self, ant, ne):
        for n in range(ne):
            for m in range(ant):
                self.weights[n][m] = round(random.uniform(-3, 3), 3)


class RBF:
    # constructor
    def __init__(self, x, me, de, k):

        self.e = 2.71828182845904523536
        self.num_layers = 2
        self.max_epochs = me
        self.reachedMax = False
        self.desired_error = de
        self.num_neutrons = k
        self.k = k
        self.time_errors = []
        self.entries = x
        self.epochs = 0
        self.layer = []
        self.error = 0

        self.start()

    def set_weights(self):
        self.layer.append(Layer(self.k, 2))
        self.layer.append(Layer(1, self.k))
        self.layer[1].set_weights(self.k, 1)

    def start(self):
        self.epochs = 0
        self.set_weights()  # Inicializa las layers y los pesos de las neuronas de 5 a -5
        self.error = self.desired_error + 1

        self.k_means()

    def squareEuclideanDist(self, p_vec, q_vec):
        diff = p_vec - q_vec
        return max(sum(diff ** 2), self.e)

    def euclideanDistance(self, p_vec, q_vec):
        return max(sqrt(self.squareEuclideanDist(p_vec, q_vec)), self.e)

    def k_means(self):
        self.layer[0].set_weights(2, self.k)
        no_change = True
        centers = self.layer[0].weights
        distance_m = [[0 for _ in range(len(self.entries))] for _ in range(len(centers))]
        sum_d = [[] for _ in range(len(centers))]
        while no_change:
            no_change = False
        # Se calcula la distancia a los centros
        for i in range(len(self.entries)):
            d = []
            for j in range(len(centers)):
                d.append(self.euclideanDistance(asarray(centers[j]), asarray(self.entries[i])))
            m = d.index(min(d))
            distance_m[d.index(min(d))][i] = min(d)
            sum_d[d.index(min(d))].append(i)

        for i in range(len(centers)):
            sumx=0
            sumy = 0
            for j in range(len(sum_d[i])):
                auxx, auxy = self.entries[sum_d[i][j]]
                sumx += auxx
                sumy += auxy
            new_center = [sumy / len(sum_d[i]), sumx / len(sum_d[i])]
            if centers[i] != new_center:
                no_change = True
                centers[i] = new_center
        print(centers)
