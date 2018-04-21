###---------Imports---------###
import math

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Color, Ellipse
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from Pretty_quatre.RBF import *
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.vertex_instructions import Rectangle, Line, Point

###---------PreConfig---------###
Window.size = (900, 600)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class MainMenu(BoxLayout):

    max_epochs = 100        #Numero default de epocas
    entry_x = []            #Listado de entradas de entrenamiento
    wish_y =[]              #Listado de labels o clase deseada
    anima = False           #Animacion Encendida
    vuelta = 0              #Vuelta de la animacion
    n_gauss = 10            #Numero default de epocas
    desired_error = 0.01    #Error deseado default
    rbf = None              #Objeto del RBF
    #funciones predefinidas
    #f1 = 2*sin(x)*cos(x)+cos(x)
    #f2 = 3*sin(x)^4+5*sin(x)^2+2*cos(x)^5
    #f3 = e+2*cos(x)^5+sin(x)
    #f4 = cos(x)

    # Limpia el plano y la variable de Entry_x y Wish_y
    def reset(self):
        self.soft_reset()
        self.set_lines()
        self.entry_x.clear()
        self.wish_y.clear()
        self.rbf = None
        self.anima = False

    def reset_graph(self):
        with self.canvas:
            Color(1, 1, 1, 1, mode='rbg')
            Rectangle(pos=(40, 21), size=(371, 108), source="Img/back2.jpg")
            self.set_other_lines()

    def changeRange(self, oxu, oxl, nxu, nxl, v):
        OldRangex = oxu - oxl
        NewRangex = nxu - nxl
        return round((((v - oxl) * NewRangex) / OldRangex) + nxl, 1)

    def soft_reset(self):
        #solo limpia las lineas
        graph = self.ids.functionGraph
        with graph.canvas:
            Color(0.78, 0.54, 0.64, 1, mode='rgb')
            Rectangle(pos=(graph.pos), size =(graph.size))
        graph = self.ids.errorGraph
        with graph.canvas:
            Color(0.78, 0.54, 0.84, 1, mode='rgb')
            Rectangle(pos=(graph.pos), size=(graph.size))
    #graficando funcion original
    def graphFunction(self, f):
        graph = self.ids.functionGraph
        with graph.canvas:
            x = 0
            while x < 50:
                if f == 'cos(x)':
                    y = math.cos(x)
                elif f == '2*sin(x)*cos(x)+cos(x)':
                    y = 2*math.sin(x)*math.cos(x)+math.cos(x)
                elif f == '3*sin(x)^4+5*sin(x)^2+2*cos(x)^5':
                    y = 3 * math.pow(math.sin(x), 4) + 5 * math.pow(math.sin(x), 2) + 2 * math.pow(math.cos(x), 5)
                else:
                    y = math.e + 2 * math.pow(math.cos(x), 5) + math.sin(x)
                d = 2
                xi = graph.pos[0]
                xf = graph.pos[0] + graph.width
                yi = graph.pos[1]
                yf = graph.pos[1] + graph.height
                NewValuex = self.changeRange(50, 0, xf, xi, x)
                NewValuey = self.changeRange(10, -10, yf, yi, y)
                Color(0.2, 0, 0.8, 1, mode='rgb')
                Ellipse(pos=(NewValuex - d / 2, NewValuey - d / 2), size=(d, d))
                x += 0.05

    #graficar error
    def draw_error(self, e, t, n):
        graph = self.ids.errorGraph
        with graph.canvas:
            Color(0.2, 0, 0.8, 1, mode='rgb')
            x = t
            y = e
            d = 2
            xi = graph.pos[0]
            xf = graph.pos[0] + graph.width
            yi = graph.pos[1]
            yf = graph.pos[1] + graph.height
            NewValuex = self.changeRange((n-1), 0, xf, xi, x)
            NewValuey = self.changeRange(self.rbf.highestError, 0, yf, yi, y)
            Ellipse(pos=(NewValuex - d/2, NewValuey - d/2), size=(d, d))

    ########################################
    ##------------Animacion---------------##
    def aminacion(self, *args):
        if self.anima:
            tam = len(self.rbf.time_weights)
            if tam > 0:
                #TODO como vas a devolver las gaussianas?
                self.draw_aprox(self.rbf.time_weights[0], [1, 0, 0])
                if 0 < self.vuelta < (tam - 1):
                    self.draw_w(self.rbf.time_weights[self.vuelta], [0, 0, 1])
                elif self.vuelta >= tam:
                    self.draw_w(self.rbf.time_weights[len(self.rbf.time_weights) - 1], [0, 1, 0])
                    self.anima = False
            #graficando el error
            if self.vuelta < len(self.rbf.time_errors):
                self.draw_error(self.rbf.time_errors[self.vuelta], self.vuelta, len(self.rbf.time_errors))
            self.vuelta += 1
    ########################################

    def draw_aprox(self, w, c):
        with self.canvas:
            Color(c[0], c[1], c[2], 1.0, mode='rgb')
            m = -(w[0]/w[2])/(w[0]/w[1])
            b = w[0]/w[2]
            xi = -5
            yi = m * xi + b
            if yi > 5:
                yi = 5
                xi = (b-yi) / (-m)
            elif yi < -5:
                yi = -5
                xi = (b-yi) / (-m)
            xf = 5
            yf = m*xf+b
            if yf > 5:
                yf = 5
                xf = (b-yf) / (-m)
            elif yf < -5:
                yf = -5
                xf = (b-yf) / (-m)
            NewValuexi = self.changeRange(5, -5, 412, (412 - 370), xi)
            NewValueyi = self.changeRange(5, -5, (180 + 370), 180, yi)
            NewValuexf = self.changeRange(5, -5, 412, (412 - 370), xf)
            NewValueyf = self.changeRange(5, -5, (180 + 370), 180, yf)
            Line(points=(NewValuexi, NewValueyi, NewValuexf, NewValueyf), width=.7)

    # (La funcion que dibuja las lineas de los planos)
    def set_lines(self):
        self.soft_reset()
        graph = self.ids.functionGraph
        with graph.canvas:
            x, y = graph.pos[0], graph.pos[1]
            aumx = graph.width/50
            aumy = graph.height/20
            Color(0.9, .8, 1, 1, mode='rgb')
            while x < graph.pos[0]+graph.width:
                Line(points=(x, graph.pos[1], x, graph.pos[1]+graph.height), width=1)
                x += aumx
            while y < graph.pos[1]+graph.height:
                Line(points=(graph.pos[0], y, graph.pos[0]+graph.width, y), width=1)
                y += aumy
            #dibujando axis
            Color(0, 0, 0, .5, mode='rgb')
            x = graph.pos[0]
            y = graph.pos[1] + graph.height/2
            Line(points=(graph.pos[0], y, graph.pos[0]+graph.width, y), width=1.2)
            Line(points=(x, graph.pos[1], x, graph.pos[1]+graph.height), width=1.2)
        #lineas del error
        graph = self.ids.errorGraph
        with graph.canvas:
            x, y = graph.pos[0], graph.pos[1]
            nlin = 20
            maxe = 10
            if self.rbf is not None:
                maxe = self.rbf.highestError
                nlin = maxe
                self.ids.maxError.text = str(maxe)
                self.ids.epochsg.text = str(self.rbf.reachedEpochs)
            aumy = graph.height / nlin
            Color(0.9, .8, 1, 1, mode='rgb')
            while y < graph.pos[1] + graph.height:
                Line(points=(graph.pos[0], y, graph.pos[0] + graph.width, y), width=1)
                y += aumy
            # dibujando axis
            Color(0, 0, 0, .5, mode='rgb')
            x = graph.pos[0]
            y = graph.pos[1]
            Line(points=(graph.pos[0], y, graph.pos[0] + graph.width, y), width=1.2)
            Line(points=(x, graph.pos[1], x, graph.pos[1] + graph.height), width=1.2)

    #para actualizar la funcion
    def changeFunction(self, button, selection):
        button.text = selection
        self.set_lines()
        self.graphFunction(selection)

    #cuando se da clic en entrenar
    def start_training(self, me, ng, de, f):
        self.reset_graph()
        #TODO agregar lo de rbf
        self.vuelta = 0

    #tomar datos del usuario
    def getData(self, mx, ngss, de, func, reachedEp, reachedEr, functionGraph, errorGraph):
        #limpiar lineas si hay
        self.soft_reset(True)
        if(len(self.entry_x) > 0):
            me = self.max_epochs
            ng = self.n_gauss
            des = self.desired_error
            f = func.text
            if mx.text != "":
                try:
                    me = int(mx.text)
                    if me < 1:
                        me = 100
                        mx.text = str(me)
                except ValueError:
                    print("Not Integer")
            if ngss.text != "":
                try:
                    ng = int(ngss.text)
                    if ng < 1:
                        ng = 10
                        ngss.text = str(ng)
                except ValueError:
                    print("Not Integer")
            if de.text != "":
                try:
                    des = float(de.text)
                    # el error solo va de 0 a 1
                    if des < 0.0 or des > 1.0:
                        des = 0.1
                        de.text = str(des)
                except ValueError:
                    print("Not Float")
            self.start_training(me, ng, de, f)
            #reachedEp.text = "Reached Epochs: " + str(rbf.epochs)
            #reachedEr.text = "Reached Error: " + str(rbf.error)
            #TODO dibujar funcion con las gaussianas

        else:
            popup = Popup(title='¡Error!',
                          content=Label(text='You need at least one entry to train '),
                          size_hint=(None, None), size=(300, 100))
            popup.open()

class RBFApp(App):
    def build(self):
        menu = MainMenu()
        #Clock.schedule_interval(menu.animacion, 0.05)
        return menu

RBFApp().run()