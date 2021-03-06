import threading

import time
from kivy.config import Config
#Esta linea es para impedir una función automática que tiene con el click derecho
from kivy.graphics.instructions import Callback
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.floatlayout import FloatLayout
from Pretty_un.Perceptron import *
##
#Establece el tamaño de la pantalla--- un poco obvio
Window.size = (800, 600)



class mainMenu(FloatLayout):
    CH_class = 0         #Si es true es clase uno si false clase dos
    Learning_rate=0.1
    Max_epochs=100
    Entry_x = []            #Listado de entradas
    Entry_test =[]
    Wish_y =[]    #Listado de labels o clase deseada
    button_train = ObjectProperty(None)
    perceptron = None
    anima = False
    vuelta = 0



    #Constructor
    def __init__(self, **kwargs):
        super(mainMenu, self).__init__(**kwargs)
        #Crea las lineas del plano
        self.set_lines()

    #Limpia el plano y la variable de Entry_x y Wish_y
    def reset(self):

        with self.canvas:
            Color(1, 1, 1, 1, mode='rbg')
            Rectangle(pos =(42,550-370), size =(370,370), source= "Img/back2.jpg")
            self.set_lines()
        self.Entry_x.clear()
        self.Wish_y.clear()
        self.Entry_test.clear()
        self.perceptron = None
        self.anima = False

    def soft_reset(self):
        self.perceptron = None
        #solo limpia las lineas deja de nuevo los puntos
        with self.canvas:
            Color(1, 1, 1, 1, mode='rbg')
            Rectangle(pos=(42, 550 - 370), size=(370, 370), source="Img/back2.jpg")
            self.set_lines()
            for i in range(0, len(self.Wish_y)):
                if self.Wish_y[i] == 0:
                    s = "Img/fa.png"
                else:
                    s = "Img/tu.png"
                Color(1, 1, 1, mode='rgv')
                OldRangex = (5 - (-5))
                NewRangex = (412 - (412 - 370))
                NewValuex = round((((self.Entry_x[i][1] - (-5)) * NewRangex) / OldRangex) + (412 - 370), 1)
                OldRangey = (5 - (-5))
                NewRangey = ((180 + 370) - 180)
                NewValuey = round((((self.Entry_x[i][2] - (-5)) * NewRangey) / OldRangey) + 180, 1)
                Rectangle(pos=(NewValuex - 12, NewValuey - 12), size=(25, 25), source=s, group="dot")

    #Agrega la entrada a la lista junto con la deseada *pasa el rango a (-5 a 5)*
    def add_to_entry(self, x, y, d):
        OldRangex = (412 - (412-370))
        NewRangex = (5 - (-5))
        NewValuex = round((((x - (412-370)) * NewRangex) / OldRangex) + (-5), 1)
        OldRangey = ((180 + 370) - 180)
        NewRangey = (5 - (-5))
        NewValuey = round((((y - 180) * NewRangey) / OldRangey) + (-5), 1)
        #entrada fantasma de -1 para el umbral
        if d==3:
            self.Entry_test.append((-1.0, float(NewValuex), float(NewValuey)))
        else:
            self.Entry_x.append((-1.0, float(NewValuex), float(NewValuey)))
            self.Wish_y.append(d)

    #(Referencia) para saber que todom se registro bien borrar luego O.o por que se puso azul?
    def pr_f(self):
        print(self.Entry_x)

    def draw_um(self,*args):

        if self.anima:
            tam = len(self.perceptron.time_weights)
            if tam>0:
                if self.vuelta ==0:
                    self.draw_w(self.perceptron.time_weights[0],[1,0,0])
                elif self.vuelta >0 and self.vuelta<(tam-1) :
                    self.draw_w(self.perceptron.time_weights[self.vuelta], [0, 0, 1])
                elif self.vuelta == tam:
                    self.draw_w(self.perceptron.time_weights[len(self.perceptron.time_weights)-1], [0, 1, 0])
            self.vuelta+=1


    def draw_w(self,w, c):
        with self.canvas:
            Color(c[0], c[1], c[2], 1.0, mode='rgb')
            m = -(w[0]/w[2])/(w[0]/w[1])
            b = w[0]/w[2]
            xi = -5
            yi = m * xi + b
            if yi > 5:
                yi = 5
                xi = (yi-b) / (-m)
            elif yi < -5:
                yi = -5
                xi = (b-yi) / (-m)

            if xi < 0 and yi < 0:
                yi += b
            xf = 5
            yf = m*xf+b
            if yf > 5:
                yf = 5
                xf = (b-yf) / (-m)
            elif yf < -5:
                yf = -5
                xf = (b-yf) / (-m)
            if xf < 0 and yf < 0:
                yf += b
            OldRangex = (5 - (-5))
            NewRangex = (412 - (412 - 370))
            NewValuexi = round((((xi - (-5)) * NewRangex) / OldRangex) + (412 - 370), 1)
            NewValuexf = round((((xf - (-5)) * NewRangex) / OldRangex) + (412 - 370), 1)
            OldRangey = (5 - (-5))
            NewRangey = ((180 + 370) - 180)
            NewValueyi = round((((yi - (-5)) * NewRangey) / OldRangey) + 180, 1)
            NewValueyf = round((((yf - (-5)) * NewRangey) / OldRangey) + 180, 1)
            Line(points=(NewValuexi, NewValueyi, NewValuexf, NewValueyf), width=1.2)

    def change_image(self, c, i):
        with self.canvas:
            if c == 0:
                s = "Img/fa2.png"
            else:
                s = "Img/tu2.png"
            Color(1, 1, 1, mode='rgv')
            OldRangex = (5 - (-5))
            NewRangex = (412 - (412 - 370))
            NewValuex = round((((self.Entry_test[i][1] - (-5)) * NewRangex) / OldRangex) + (412 - 370), 1)
            OldRangey = (5 - (-5))
            NewRangey = ((180 + 370) - 180)
            NewValuey = round((((self.Entry_test[i][2] - (-5)) * NewRangey) / OldRangey) + 180, 1)
            Rectangle(pos=(NewValuex - 12, NewValuey - 12), size=(26, 26), source=s, group="dot")

    def test(self):
        if self.perceptron != None:
            clases = self.perceptron.clasify(self.Entry_test)
            if len(clases) != 0:
                i = 0
                for c in clases:
                    self.change_image(c,i)
                    i += 1
            else:
                popup = Popup(title='¡Error!',
                              content=Label(text='Untrained perceptron.'),
                              size_hint=(None, None), size=(200, 100))
                popup.open()
        else:
            popup = Popup(title='¡Error!',
                          content=Label(text='Untrained perceptron.'),
                          size_hint=(None, None), size=(200, 100))
            popup.open()
    #(La funcion que dibuja las lineas del plano)
    def set_lines(self):
        with self.canvas.after:
            Color(1,1,1,1, mode ='rbg')
            Rectangle(pos = (0,0), size=(800,600), source= "Img/b2.png")
        with self.canvas:
            cont=0
            for x in range(10):
                Color(0, 0, 0, .2, mode='rgb')
                Line(points=(43+cont, 550, 43+cont, 184), width=1)
                Line(points=(43, 550-cont, 43+370, 550-cont), width=1)
                #cont+=18.6
                cont+=37.2
        Color( 1, 0, 0, .5, mode='rgb')
        Line(points= (43 + 185, 550, 43 + 185, 184),width= 1.2)
        Line(points= (43, 550 - 185, 43 + 370, 550 - 185),width= 1.2)

    #La funcion del click
    def on_touch_up(self, touch):
        #Si fue en el plano
        if(touch.pos[0]>42 and touch.pos[0]<43+370 and touch.pos[1]<550 and touch.pos[1]>180):

            with self.canvas:
                if self.CH_class ==0:
                    nclass=0
                    s ="Img/fa.png"
                elif self.CH_class ==1:
                    nclass=1
                    s = "Img/tu.png"
                elif self.CH_class == 3:
                    nclass = 3
                    s = "Img/te.png"
                Color(1, 1, 1, mode='rgv')
                Rectangle(pos=(touch.pos[0] - 12, touch.pos[1] - 12), size=(25, 25), source=s, group="dot")
            self.add_to_entry(touch.pos[0], touch.pos[1],nclass)

    #cuando se da clic en entrenar
    def start_training(self, lr, me):
        self.perceptron = Perceptron(lr,me,self.Entry_x,self.Wish_y,self)
        self.anima = True
        self.vuelta = 0

    def get_data(self, lrn, mx, es, ep):
        #limpiar lineas si hay
        self.soft_reset()
        if(len(self.Entry_x)>0):
            lr = self.Learning_rate
            me = self.Max_epochs
            if lrn.text != "":
                try:
                    lr = float(lrn.text)
                    if lr < 0.1 or lr > 0.9:
                        lr = 0.1
                        lrn.text=str(lr)
                except ValueError:
                    print("No es Flotante")
            if mx.text != "":
                try:
                    me = int(mx.text)
                    if me < 1:
                        me = 100
                        mx.text=str(me)
                except ValueError:
                    print("No es Entero")
            es.text = "Training..."
            self.start_training(lr,me)
            if self.perceptron.nonlinear:
                es.text = "Non Linear"
            else:
                es.text = "Trained!"
                ep.text = "Number of Epochs: "+str(self.perceptron.epochs)
        else:
            popup = Popup(title='¡Error!',
                          content=Label(text='You need at least one entry to train '),
                          size_hint=(None, None), size=(300, 100))
            popup.open()


class PerceptronApp(App):
    def build(self):
        menu = mainMenu()
        Clock.schedule_interval(menu.draw_um, 0.2)
        return menu


PerceptronApp().run()