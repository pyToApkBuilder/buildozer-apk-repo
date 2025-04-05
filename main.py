from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Line, Ellipse, Color
from kivy.core.image import Image as CoreImage
import random


class BallGame(RelativeLayout):
    ball_x = NumericProperty(500)  
    ball_y = NumericProperty(200)  
    velocity = [0, 0]  
    ball_size = 50 

    target_x = NumericProperty(random.randint(100,800))  
    target_y = NumericProperty(random.randint(100,1800))  
    target_size = 80  

    ball_inside_target = BooleanProperty(False) 
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = (0, 0)
        
        with self.canvas.before:
            self.bg = Rectangle(source="bg.png", pos=self.pos, size=self.size)
        self.bind(size=self._update_bg, pos=self._update_bg)

        with self.canvas:
            Color(1,1,1,1)
            self.target_outline = Ellipse(pos=(self.target_x - 5, self.target_y - 5), size=(self.target_size + 10, self.target_size + 10))

            Color(0, 1, 0, 0.6)
            self.target = Ellipse(pos=(self.target_x, self.target_y), size=(self.target_size, self.target_size))
            
            Color(1,0,1,0.8)
            self.ball = Ellipse(pos=(self.ball_x,self.ball_y),size=(self.ball_size, self.ball_size))

        self.score = 0
        self.tries = 0

        self.score_l = Label(text=f"Score: 0  Tries: 0",font_size = 40)

        self.add_widget(self.score_l)

        Clock.schedule_interval(self.update, 1 / 60.0)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_touch_down(self, touch):
        self.start_pos = touch.pos
        with self.canvas:
            Color(0, 1, 1) 
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points = [touch.ud['line'].points[0],
                                       touch.ud['line'].points[1],
                                       touch.x, touch.y]

    def on_touch_up(self, touch):
        if 'line' in touch.ud:
            self.canvas.remove(touch.ud['line'])
            
        end_pos = touch.pos
        swipe_vector = Vector(end_pos) - Vector(self.start_pos)
        self.velocity = swipe_vector * 0.05 
        
        self.tries += 1
        self.score_l.text = f"Score: {self.score}  Tries: {self.tries}"

    def update(self, dt):
        
        self.ball_x -= self.velocity[0]
        self.ball_y -= self.velocity[1]

        
        screen_width, screen_height = self.width, self.height

        if self.ball_x <= 0:
            self.ball_x = 0
            self.velocity[0] = -self.velocity[0]
        if self.ball_x + self.ball_size >= screen_width:
            self.ball_x = screen_width - self.ball_size
            self.velocity[0] = -self.velocity[0]
        if self.ball_y <= 0:
            self.ball_y = 0
            self.velocity[1] = -self.velocity[1]
        if self.ball_y + self.ball_size >= screen_height:
            self.ball_y = screen_height - self.ball_size
            self.velocity[1] = -self.velocity[1]

        
        self.velocity = [v * 0.98 for v in self.velocity]

        
        self.ball.pos = (self.ball_x, self.ball_y)
       
        self.check_target_collision()

    def check_target_collision(self):
       
        ball_center_x = self.ball_x + self.ball_size / 2
        ball_center_y = self.ball_y + self.ball_size / 2

        target_center_x = self.target_x + self.target_size / 2
        target_center_y = self.target_y + self.target_size / 2

        
        distance = ((ball_center_x - target_center_x) ** 2 + (ball_center_y - target_center_y) ** 2) ** 0.5

        if distance < (self.target_size / 2) - (self.ball_size / 2):
            self.ball_inside_target = True
            self.success_message()
        else:
            self.ball_inside_target = False

    def success_message(self):
        self.score +=1
        self.score_l.text = f"Score: {self.score}  Tries: {self.tries}"

        self.ball_x, self.ball_y = (self.width / 2) - 25, (self.height / 2) - 100
        self.velocity = [0, 0]

        self.target_x = random.randint(50, self.width - 100)
        self.target_y = random.randint(50, self.height - 100)

        self.target.pos = (self.target_x, self.target_y)
        self.target_outline.pos = (self.target_x - 5, self.target_y - 5)

class BallGameApp(App):
    def build(self):
        return BallGame()

if __name__ == "__main__":
    BallGameApp().run()
