import random
class perceptron:
    def __init__(self,lr,me,x,y):
        self.learning_rate = lr
        self.max_epochs = me
        self.entries = x
        self.desired = y
        self.start()

    #funcion de transferencia
    def Pw(self,x):
        pw = 0
        return pw

    def start(self):
        #inicializando los pesos con valores random entre -5 y 5
        weights = []
        #ingresado w0 = umbral = -1
        weights.append(-1)
        for i in self.entries:
            weights.append(random.uniform(-5, 5))
        done = False
        while(not done):
            done = True
            for i in self.entries:
                #obteniendo el error
                error = self.desired[i] - self.Pw(self.entries[i])
                if error != 0:
                    done = False
                    for j in weights:
                        j = j + self.learning_rate*error*self.entries[i]
