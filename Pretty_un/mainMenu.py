from kivy.config import Config
#
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.uix.floatlayout import FloatLayout

Window.size = (800, 600)

class mainMenu(FloatLayout):

    chclass = True
    Learning_rate=0.1
    Max_Epochs=100
    Entryx = []
    Wish =[]

    def __init__(self, **kwargs):
        super(mainMenu, self).__init__(**kwargs)
        self.set_lines()

    def reset(self):
        with self.canvas:
            Color (1,1,1,1, mode ='rbg')
            Rectangle(pos =(42,550-370), size =(370,370), source= "Img/back2.jpg")
            self.set_lines()

    def add_to_entry(self, x, y, d):
        OldRangex = (412 - (412-370))
        NewRangex = (5 - (-5))
        NewValuex = str(round((((x - (412-370)) * NewRangex) / OldRangex) + (-5), 1))
        OldRangey = ((180 + 370) - 180)
        NewRangey = (5 - (-5))
        NewValuey = str(round((((y - 180) * NewRangey) / OldRangey) + (-5), 1))

        print(NewValuex, "=>", NewValuey)
        self.Entryx.append((NewValuex, NewValuey))
        self.Wish.append(d)


    def pr_f(self):
        print(self.Entryx)

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


#


    def on_touch_up(self, touch):
        if(touch.pos[0]>42 and touch.pos[0]<43+370 and touch.pos[1]<550 and touch.pos[1]>180):
            nclass=0
            with self.canvas:
                if self.chclass:
                    nclass=0
                    Color(1,1,1, mode='rgv')
                    Rectangle(pos=(touch.pos[0]-12,touch.pos[1]-12), size=(25, 25), source ="Img/fa.png", group ="dot")
                else:
                    nclass=1
                    Color(1, 1, 1, mode='rgv')
                    Rectangle(pos=(touch.pos[0] - 12, touch.pos[1] - 12), size=(25, 25), source="Img/tu.png", group ="dot")
            self.add_to_entry(touch.pos[0], touch.pos[1],nclass)








class PerceptronApp(App):
    def build(self):
        return mainMenu()


PerceptronApp().run()
