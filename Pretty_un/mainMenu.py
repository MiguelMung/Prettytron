from kivy.config import Config
#Esta linea es para impedir una función automática que tiene con el click derecho
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.floatlayout import FloatLayout


#Establece el tamaño de la pantalla--- un poco obvio
Window.size = (800, 600)

class mainMenu(FloatLayout):
    CH_class = True         #Si es true es clase uno si false clase dos
    Learning_rate=0.1
    Max_epochs=100
    Entry_x = []            #Listado de entradas
    Wish_y =[]              #Listado de labels o clase deseada

    #Constructor
    def __init__(self, **kwargs):
        super(mainMenu, self).__init__(**kwargs)
        #Crea las lineas del plano
        self.set_lines()

    #Limpia el plano y la variable de Entry_x
    def reset(self):
        with self.canvas:
            Color (1,1,1,1, mode ='rbg')
            Rectangle(pos =(42,550-370), size =(370,370), source= "Img/back2.jpg")
            self.set_lines()
        self.Entry_x.clear()

    #Agrega la entrada a la lista junto con la deseada *pasa el rango a (-5 a 5)*
    def add_to_entry(self, x, y, d):
        OldRangex = (412 - (412-370))
        NewRangex = (5 - (-5))
        NewValuex = str(round((((x - (412-370)) * NewRangex) / OldRangex) + (-5), 1))
        OldRangey = ((180 + 370) - 180)
        NewRangey = (5 - (-5))
        NewValuey = str(round((((y - 180) * NewRangey) / OldRangey) + (-5), 1))
        self.Entry_x.append((NewValuex, NewValuey))
        self.Wish_y.append(d)

    #(Referencia) para saber que todom se registro bien borrar luego O.o por que se puso azul?
    def pr_f(self):
        print(self.Entryx)

    #(La funcion que dibuja las lineas del plano)
    def set_lines(self):
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
                if self.CH_class:
                    nclass=0
                    s ="Img/fa.png"
                else:
                    nclass=1
                    s = "Img/tu.png"
                Color(1, 1, 1, mode='rgv')
                Rectangle(pos=(touch.pos[0] - 12, touch.pos[1] - 12), size=(25, 25), source=s, group="dot")
            self.add_to_entry(touch.pos[0], touch.pos[1],nclass)








class PerceptronApp(App):
    def build(self):
        return mainMenu()


PerceptronApp().run()
