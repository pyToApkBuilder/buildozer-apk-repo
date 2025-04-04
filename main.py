from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Ellipse, Color
import random

kivy.require('1.9.1')

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

        with self.canvas:
            
            Color(0, 1, 0, 0.4)  
            self.target = Ellipse(pos=(self.target_x, self.target_y), size=(self.target_size, self.target_size))

            
            Color(1, 0, 0, 1) 
            self.ball = Ellipse(pos=(self.ball_x, self.ball_y), size=(self.ball_size, self.ball_size))

        
        Clock.schedule_interval(self.update, 1 / 60.0)

    def on_touch_down(self, touch):
        self.start_pos = touch.pos

    def on_touch_up(self, touch):
        end_pos = touch.pos
        swipe_vector = Vector(end_pos) - Vector(self.start_pos)
        self.velocity = swipe_vector * 0.05 

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
       
        self.ball_x, self.ball_y = self.width / 2, self.height / 2
        self.velocity = [0, 0]  

        
        self.target_x = random.randint(50, self.width - 100)
        self.target_y = random.randint(50, self.height - 100)

        self.target.pos = (self.target_x, self.target_y)

class BallGameApp(App):
    def build(self):
        return BallGame()

if __name__ == "__main__":
    BallGameApp().run()
