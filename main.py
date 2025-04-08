from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.label import Label
from random import random

class Ball(Widget):
    velocity = ListProperty([0, 0])
    friction = NumericProperty(0.90)
    is_ball1 = BooleanProperty(False)

class Target(Widget):
    pass

class GameWidget(Widget):
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    target = ObjectProperty(None)
    touch_start = ListProperty([0, 0])
    current_touch = ListProperty([0, 0])
    is_aiming = BooleanProperty(False)
    score = NumericProperty(0)
    tries = NumericProperty(0)
    points = NumericProperty(100)

    def on_touch_down(self, touch):
        if self.is_aiming:  # Ignore new touches while aiming
            return False
        self.touch_start = touch.pos
        self.current_touch = touch.pos
        self.is_aiming = True
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.current_touch = touch.pos
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            delta = Vector(self.current_touch) - Vector(self.touch_start)
            self.ball1.velocity = -delta * 0.3
            self.tries += 1
            self.points = int(100/(self.tries+1))
            self.is_aiming = False
            touch.ungrab(self)
        return super().on_touch_up(touch)

    def update(self, dt):
        for ball in [self.ball1, self.ball2]:
            ball.velocity = Vector(ball.velocity) * ball.friction
            ball.pos = Vector(ball.velocity) + ball.pos

            # Wall collisions
            if ball.x < 0:
                ball.x = 0
                ball.velocity[0] *= -1
            if ball.right > self.width:
                ball.right = self.width
                ball.velocity[0] *= -1
            if ball.y < 0:
                ball.y = 0
                ball.velocity[1] *= -1
            if ball.top > self.height:
                ball.top = self.height
                ball.velocity[1] *= -1

        # Ball collision
        distance = Vector(self.ball1.center).distance(self.ball2.center)
        if distance <= (self.ball1.width/2 + self.ball2.width/2):
            normal = Vector(self.ball2.center) - Vector(self.ball1.center)
            if normal.length() == 0:
                return
            normal = normal.normalize()

            # Only resolve collision if balls are moving towards each other
            relative_velocity = Vector(self.ball2.velocity) - Vector(self.ball1.velocity)
            if normal.dot(relative_velocity) > 0:
                return

            # Mass ratio (assuming equal mass)
            mass_ratio = 2.0
            v1 = Vector(self.ball1.velocity)
            v2 = Vector(self.ball2.velocity)

            new_v1 = v1 - normal * normal.dot(v1 - v2) * mass_ratio
            new_v2 = v2 - normal * normal.dot(v2 - v1) * mass_ratio

            self.ball1.velocity = new_v1
            self.ball2.velocity = new_v2

            # Position correction
            overlap = (self.ball1.width/2 + self.ball2.width/2) - distance
            if overlap > 0:
                correction = normal * (overlap * 1.1)
                self.ball1.pos = Vector(self.ball1.pos) - correction
                self.ball2.pos = Vector(self.ball2.pos) + correction

        # Target check
        if self.ball2.collide_widget(self.target):
            self.score = self.score + int(100/self.tries)
            self.tries = 0
            self.points = 100
            self.reset_game()

    def reset_game(self):
        self.ball1.center = (
            self.width * 0.1 + random() * self.width * 0.8,
            self.height * 0.1 + random() * self.height * 0.8
        )
        
        self.ball2.center = (
            self.width * 0.1 + random() * self.width * 0.8,
            self.height * 0.1 + random() * self.height * 0.8
        )
        
        self.ball1.velocity = [0, 0]
        self.ball2.velocity = [0, 0]
        self.target.center = (
            self.width * 0.1 + random() * self.width * 0.8,
            self.height * 0.1 + random() * self.height * 0.8
        )

class PoolGameApp(App):
    def build(self):
        game = GameWidget()
        Clock.schedule_interval(game.update, 1/60.)
        return game

if __name__ == '__main__':
    PoolGameApp().run()
