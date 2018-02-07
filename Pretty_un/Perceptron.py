import random

import time
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Point, Line

class Perceptron:
    #constructor
    def __init__(self,lr,me,x,y,window):
        self.learning_rate = lr
        self.max_epochs = me
        self.epochs = 0
        self.entries = x
        self.desired = y
        self.weights = []
        self.nonlinear = False
        self.start(window)

    #funcion de transferencia
    def Pw(self,x):
        pw = 0
        wx = 0.0
        for i in range(0, len(self.weights)):
            wx += round(self.weights[i]*x[i], 2)
                #umbral
        if wx >= self.weights[0]:
            pw = 1
        return pw
    #dibujando el umbral
    def draw_um(self,window):
        with window.canvas:
            #centro x=228 y=365
            Color(0, 0, 1, 1.0, mode='rgb')
            xi = -5
            yi = xi * (-(self.weights[0] / self.weights[2])/(-(self.weights[0] / self.weights[1]))) + (-self.weights[0]/self.weights[2])
            if yi > 5:
                yi = 5
            elif yi < -5:
                yi = -5
            xf = 5
            yf = xf * (-(self.weights[0] / self.weights[2])/(-(self.weights[0] / self.weights[1]))) + (-self.weights[0]/self.weights[2])
            if yf > 5:
                yf = 5
            elif yf < -5:
                yf = -5
            OldRangex = (5 - (-5))
            NewRangex = (412 - (412 - 370))
            NewValuexi = round((((xi - (-5)) * NewRangex) / OldRangex) + (412 - 370), 1)
            NewValuexf = round((((xf - (-5)) * NewRangex) / OldRangex) + (412 - 370), 1)
            OldRangey = (5 - (-5))
            NewRangey = ((180 + 370) - 180)
            NewValueyi = round((((yi - (-5)) * NewRangey) / OldRangey) + 180, 1)
            NewValueyf = round((((yf - (-5)) * NewRangey) / OldRangey) + 180, 1)
            Line(points= (NewValuexi, NewValueyi, NewValuexf, NewValueyf),width= 1.2)
        window.canvas

    def start(self, window):
        #inicializando los pesos con valores random entre -5 y 5
        self.weights = []
        for i in self.entries[0]:
            self.weights.append(round(random.uniform(-5, 5), 2))
        done = False
        self.epochs = 0
        while(not done and self.epochs < self.max_epochs):
            # dibujando umbral
            self.draw_um(window)
            done = True
            for i in range(0,len(self.entries)):
                #obteniendo el error
                error = self.desired[i] - self.Pw(self.entries[i])
                if error != 0:
                    done = False
                    #ajustando los pesos
                    for j in range(0, len(self.weights)):
                        self.weights[j] = round(self.weights[j] + self.learning_rate*error*self.entries[i][j],2)
            self.epochs += 1
            time.sleep(2)
        if not done:
            self.nonlinear = True
        else:
            self.nonlinear = False