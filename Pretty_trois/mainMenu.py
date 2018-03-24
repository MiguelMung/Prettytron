###---------Imports---------###
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Color, Ellipse
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from Pretty_trois.Adaline import *
from Pretty_trois.multilayer import *
from Pretty_trois.Perceptron import *
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.vertex_instructions import Rectangle, Line, Point

###---------PreConfig---------###
Window.size = (800, 600)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class mainMenu(FloatLayout):
    CH_class = 0            #Clase actual
    Learning_rate=0.1       #Learnig Rate
    Max_epochs=100          #Numero Maximo de epocas
    Entry_x = []            #Listado de entradas de entrenamiento
    Entry_test =[]          #Listado de entradas de prueba
    Wish_y =[]              #Listado de labels o clase deseada
    adaline = None          #declarando el adaline
    anima = False           #Animacion Encendida
    perceptron =None        #declarando el simple
    vuelta = 0              #Vuelta de la animacion
    ada = True              #Define si usar el adaline o el perceptron
    mlp = False             #Define si usar el MLP
    S= False
    A= False
    Sw=[]
    Aw=[]

    # Constructor
    def __init__(self, **kwargs):
        super(mainMenu, self).__init__(**kwargs)
        #Crea las lineas del plano
        self.set_lines()
        self.set_other_lines()

    # Limpia el plano y la variable de Entry_x y Wish_y
    def reset(self):
        self.S=self.A=False
        self.clean_labels()
        with self.canvas:
            Color(1, 1, 1, 1, mode='rbg')
            Rectangle(pos =(42,550-370), size =(370,370), source= "Img/back2.jpg")
            self.set_lines()
            self.set_other_lines()
        self.Entry_x.clear()
        self.Wish_y.clear()
        self.Entry_test.clear()
        self.adaline = None
        self.anima = False

    def reset_graph(self):
        with self.canvas:
            Color(1, 1, 1, 1, mode='rbg')
            Rectangle(pos=(40, 121 - 100), size=(370, 100), source="Img/back2.jpg")
            self.set_other_lines()

    def changeRange(self, oxu, oxl, nxu, nxl, v):
        OldRangex = oxu - oxl
        NewRangex = nxu - nxl
        return round((((v - oxl) * NewRangex) / OldRangex) + nxl, 1)

    def soft_reset(self, sec):
        if sec:
            self.adaline = None
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
                NewValuex = self.changeRange(5, -5, 412, (412 - 370), self.Entry_x[i][1])
                NewValuey = self.changeRange(5, -5, (180 + 370), 180, self.Entry_x[i][2])
                Rectangle(pos=(NewValuex - 10, NewValuey - 10), size=(20, 20), source=s, group="dot")

    # Agrega la entrada a la lista junto con la deseada *pasa el rango a (-5 a 5)*
    def add_to_entry(self, x, y, d):
        NewValuex = self.changeRange(412, (412-370), 5, -5, x)
        NewValuey = self.changeRange((180 + 370), 180, 5, -5, y)
        #entrada fantasma de -1 para el umbral
        if d==3:
            self.Entry_test.append((-1.0, float(NewValuex), float(NewValuey)))
        else:
            self.Entry_x.append((-1.0, float(NewValuex), float(NewValuey)))
            self.Wish_y.append(d)

    # (Referencia) para saber que todom se registro bien borrar luego O.o por que se puso azul?
    def pr_f(self):
        m = 0
        m= multilayer(.5, 20, self.Entry_x, self.Wish_y, 1, 2,[2,3])



    #graficar error
    def draw_error(self, e, t, n):
        with self.canvas:
            #40,21 100,370
            Color(0, 0, 1, 1.0, mode='rgb')
            x = t
            y = e
            d = 2
            NewValuex = self.changeRange((n-1), 0, 410, (410 - 370), x)
            NewValuey = self.changeRange(5, -5, (21 + 100), 21, y)
            Ellipse(pos=(NewValuex - d/2, NewValuey - d/2), size=(d, d))

    ########################################
    ##------------Animacion---------------##
    def draw_umbral(self, *args):
        if self.anima:
            tam = len(self.adaline.time_weights)
            self.soft_reset(False)
            if tam > 0:
                self.draw_w(self.adaline.time_weights[0], [1, 0, 0])
                if 0 < self.vuelta < (tam - 1):
                    self.draw_w(self.adaline.time_weights[self.vuelta], [0, 0, 1])
                elif self.vuelta >= tam:
                    self.draw_w(self.adaline.time_weights[len(self.adaline.time_weights) - 1], [0, 1, 0])
                    self.anima = False
            #graficando el error en adaline
            if self.ada or self.mlp:
                if self.vuelta < len(self.adaline.time_errors):
                    self.draw_error(self.adaline.time_errors[self.vuelta], self.vuelta, len(self.adaline.time_errors))
            self.vuelta += 1
    ########################################

    def draw_w(self, w, c):
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

    def change_image(self, c, i):
        with self.canvas:
            if c == 0:
                s = "Img/fa2.png"
            else:
                s = "Img/tu2.png"
            Color(1, 1, 1, mode='rgv')
            NewValuex = self.changeRange(5, -5, 412, (412 - 370), self.Entry_test[i][1])
            NewValuey = self.changeRange(5, -5, (180 + 370), 180, self.Entry_test[i][2])
            Rectangle(pos=(NewValuex - 10, NewValuey - 10), size=(20, 20), source=s, group="dot")

    def makeItColorfull(self):
        with self.canvas:
            x = 42
            y = 180
            while x <= 412:
                while y <= 550:
                    xa = self.changeRange(412, 42, 5, -5, x)
                    ya = self.changeRange(550, 180, 5, -5, y)
                    cls = self.adaline.clasify([xa, ya])
                    d = 2
                    if cls == 0:
                        Color(228, 124, 232, 0.5, mode='rgb')
                    elif cls == 1:
                        Color(114, 240, 240, 0.5, mode='rgb')
                    else:
                        Color(114, 240, 147, 0.5, mode='rgb')
                    Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d))
                    y *= 2
                x *= 2
            #poner de nuevo las imagenes

    def changeClass3(self, cl3, tabs):
        if tabs.current_tab.text == "MLP":
            cl3.disabled = False
        else:
            self.CH_class = 0
            cl3.disabled = True

    def test(self):
        if self.adaline is not None:
            if self.mlp:
                self.makeItColorfull()
            else:
                clases = self.adaline.clasify(self.Entry_test)
                if len(clases) != 0:
                    i = 0
                    for c in clases:
                        self.change_image(c, i)
                        i += 1
                else:
                    popup = Popup(title='¡Error!',
                                  content=Label(text='No new entries.'),
                                  size_hint=(None, None), size=(200, 100))
                    popup.open()
        else:
            popup = Popup(title='¡Error!',
                          content=Label(text='Untrained!'),
                          size_hint=(None, None), size=(200, 100))
            popup.open()

    # lineas de la grafica del error
    def set_other_lines(self):
        with self.canvas:
            c = 0
            for x in range(10):
                Color(0, 0, 0, .2, mode='rgb')
                Line(points=(40, 121 - c, 40 + 370, 121 - c), width=1)
                c += 10
        Color(1, 0, 0, .5, mode='rgb')
        Line(points=(40, 121 - 50, 40 + 370, 121 - 50), width=1.2)

    # (La funcion que dibuja las lineas del plano)
    def set_lines(self):
        with self.canvas:
            cont = 0
            for x in range(10):
                Color(0, 0, 0, .2, mode='rgb')
                Line(points=(42+cont, 550, 42+cont, 184), width=1)
                Line(points=(42, 550-cont, 42+370, 550-cont), width=1)
                #cont+=18.6
                cont += 37.2
        Color( 1, 0, 0, .5, mode='rgb')
        Line(points= (43 + 185, 550, 43 + 185, 184),width= 1.2)
        Line(points= (43, 550 - 185, 43 + 370, 550 - 185),width= 1.2)

    # La funcion del click
    def on_touch_up(self, touch):
        # Si fue en el plano
        if 42 < touch.pos[0] < 43+370 and 550 > touch.pos[1] > 180:
            with self.canvas:
                if self.CH_class ==0:
                    nclass=0
                    s ="Img/fa.png"
                elif self.CH_class ==1:
                    nclass=1
                    s = "Img/tu.png"
                elif self.CH_class ==2:
                    nclass=2
                    s = "Img/lu.png"
                elif self.CH_class == 3:
                    nclass = 3
                    s = "Img/te.png"
                Color(1, 1, 1, mode='rgv')
                Rectangle(pos=(touch.pos[0] - 10, touch.pos[1] - 10), size=(20, 20), source=s, group="dot")
            self.add_to_entry(touch.pos[0], touch.pos[1], nclass)

    #cuando se da clic en entrenar
    def start_training(self, lr, me, de, nhl, nnr1, nnr2):
        self.reset_graph()
        if self.ada:
            print(self.Entry_x)
            self.adaline = Adaline(lr, me, self.Entry_x, self.Wish_y, de)
            self.get_Compare(1)
        elif self.mlp:
            self.adaline = multilayer(lr, me, self.Entry_x, self.Wish_y, de, nhl, [nnr1, nnr2])
        else:
            self.adaline = Perceptron(lr, me, self.Entry_x, self.Wish_y)
            self.get_Compare(2)
        self.anima = True
        self.vuelta = 0

    #para adaline
    def get_data(self, lrn, mx, es, ep, de):
        #limpiar lineas si hay
        self.soft_reset(True)
        des = 0
        if(len(self.Entry_x) > 0):
            lr = self.Learning_rate
            me = self.Max_epochs
            if lrn.text != "":
                try:
                    lr = float(lrn.text)
                    if lr <= 0.0:
                        lr = 0.1
                        lrn.text=str(lr)
                except ValueError:
                    print("Not Float")
            if mx.text != "":
                try:
                    me = int(mx.text)
                    if me < 1:
                        me = 100
                        mx.text = str(me)
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
            es.text = "Training..."
            self.ada = True
            self.start_training(lr, me, des, 0, 0, 0)
            if self.adaline.nonlinear:
                es.text = "State: "+"Reached Max. Epochs"
            else:
                es.text = "State: "+"Trained!"
            ep.text = "Number of Epochs: "+str(self.adaline.epochs)
        else:
            popup = Popup(title='¡Error!',
                          content=Label(text='You need at least one entry to train '),
                          size_hint=(None, None), size=(300, 100))
            popup.open()

    def changeSliderStatus(self, no, slider):
        if no == 2:
            slider.disabled = False
        else:
            slider.disabled = True

    def get_dataMLP(self, lrn, mx, es, ep, de, nhl, nnr1, nnr2):
        # limpiar lineas si hay
        self.soft_reset(True)
        des = 0
        if (len(self.Entry_x) > 0):
            lr = self.Learning_rate
            me = self.Max_epochs
            if lrn.text != "":
                try:
                    lr = float(lrn.text)
                    if lr <= 0.0:
                        lr = 0.1
                        lrn.text = str(lr)
                except ValueError:
                    print("Not Float")
            if mx.text != "":
                try:
                    me = int(mx.text)
                    if me < 1:
                        me = 100
                        mx.text = str(me)
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
            es.text = "Training..."
            self.mlp = True
            self.start_training(lr, me, des, nhl, nnr1, nnr2)
            if self.adaline.reachedMax:
                es.text = "State: " + "Reached Max. Epochs"
            else:
                es.text = "State: " + "Trained!"
            ep.text = "Number of Epochs: " + str(self.adaline.epochs)
        else:
            popup = Popup(title='¡Error!',
                          content=Label(text='You need at least one entry to train '),
                          size_hint=(None, None), size=(300, 100))
            popup.open()
    #para perceptron
    def get_datas(self, lrn, mx, es, ep):
        #limpiar lineas si hay
        self.soft_reset(True)
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
            self.ada = False
            self.start_training(lr, me, 0, 0, 0, 0)
            if self.adaline.nonlinear == True:
                es.text = "Non Linear"
            else:
                es.text = "Trained!"
                ep.text = "Number of Epochs: "+str(self.adaline.epochs)
                #
        else:
            popup = Popup(title='¡Error!',
                          content=Label(text='You need at least one entry to train '),
                          size_hint=(None, None), size=(300, 100))
            popup.open()

    def get_Compare(self,type):
        if type ==1:
            self.A=True
            self.Aw = self.adaline.time_weights
            if self.adaline.nonlinear:
                self.ids.a_s.text = "[b]State:[/b] " + "Reached Max. Epochs"
            else:
                self.ids.a_s.text = "[b]State:[/b] " + "Trained!"
            self.ids.a_l.text="[b]Learning rate:[/b] "+str(self.adaline.learning_rate)
            self.ids.a_m.text="[b]Max Epochs:[/b] " + str(self.adaline.max_epochs)
            self.ids.a_n.text="[b]Number Epochs:[/b] "+str(self.adaline.epochs)
            self.ids.a_d.text="[b]Desired error:[/b] "+str(self.adaline.desired_error)
            self.ids.a_f.text = "[b]Final error:[/b] " + str(round(self.adaline.error,6))
            l=len(self.adaline.time_weights) - 1
            self.ids.a_iw.text="[ "+str(round(self.adaline.time_weights[0][0],2))+", "+str(round(self.adaline.time_weights[0][1],2))+", "+str(round(self.adaline.time_weights[0][2],2))+"]"
            self.ids.a_fw.text="[ "+str(round(self.adaline.time_weights[l][0],2))+", "+str(round(self.adaline.time_weights[l][1],2))+", "+str(round(self.adaline.time_weights[l][2],2))+"]"
        elif type ==2:
            self.S = True
            self.Sw=self.adaline.time_weights
            if self.adaline.nonlinear:
                self.ids.s_s.text = "[b]State:[/b] " + "Non linear"
            else:
                self.ids.s_s.text = "[b]State:[/b] " + "Trained!"
            self.ids.s_l.text="[b]Learning rate:[/b] "+str(self.adaline.learning_rate)
            self.ids.s_m.text="[b]Max Epochs:[/b] " + str(self.adaline.max_epochs)
            self.ids.s_n.text="[b]Number Epochs:[/b] "+str(self.adaline.epochs)
            l=len(self.adaline.time_weights) - 1
            self.ids.s_iw.text="[ "+str(round(self.adaline.time_weights[0][0],2))+", "+str(round(self.adaline.time_weights[0][1],2))+", "+str(round(self.adaline.time_weights[0][2],2))+"]"
            self.ids.s_fw.text="[ "+str(round(self.adaline.time_weights[l][0],2))+", "+str(round(self.adaline.time_weights[l][1],2))+", "+str(round(self.adaline.time_weights[l][2],2))+"]"

    def comparar(self):
        if self.S ==False:
            popup = Popup(title='¡Error!',
                          content=Label(text='First train with Simple'),
                          size_hint=(None, None), size=(300, 100))
            popup.open()
        if self.A == False:
            popup = Popup(title='¡Error!',
                          content=Label(text='First train with Adaline'),
                          size_hint=(None, None), size=(300, 100))
            popup.open()
        if self.A and self.S :
            we=[]
            we.append(self.Aw[0])
            we.append(self.Aw[len(self.Aw)-1])
            we.append(self.Sw[0])
            we.append(self.Sw[len(self.Sw)-1])
            self.draw_com(we)


    def draw_com(self,we):
        self.soft_reset(False)
        print(we[0])
        self.draw_w(we[0], [1, 1, 0])
        self.draw_w(we[1], [1, .5, 0])
        self.draw_w(we[2], [0, 1, 1])
        self.draw_w(we[3], [0, 1, .5])

    def clean_labels(self):
        self.ids.a_s.text = "[b]State:[/b] "
        self.ids.a_l.text = "[b]Learning rate:[/b] "
        self.ids.a_m.text = "[b]Max Epochs:[/b] "
        self.ids.a_n.text = "[b]Number Epochs:[/b] "
        self.ids.a_d.text = "[b]Desired error:[/b] "
        self.ids.a_iw.text = " "
        self.ids.a_fw.text = " "
        self.ids.s_s.text = "[b]State:[/b] "
        self.ids.s_l.text = "[b]Learning rate:[/b] "
        self.ids.s_m.text = "[b]Max Epochs:[/b] "
        self.ids.s_n.text = "[b]Number Epochs:[/b] "
        self.ids.s_iw.text = " "
        self.ids.s_fw.text = " "

class AdalineApp(App):
    def build(self):
        menu = mainMenu()
        Clock.schedule_interval(menu.draw_umbral, 0.05)
        return menu

AdalineApp().run()
