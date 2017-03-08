import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from kivy.graphics import *
from kivy.properties import ListProperty, ObjectProperty,NumericProperty, ReferenceListProperty
from constants import *
from kivy.vector import Vector
import math

def perpendicular(a):
    return [a[1], -1*a[0]]

def mag(a):
    return math.sqrt(sum(a[i]*a[i] for i in range(len(a))))

def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))

def scalar_mult(a, b):
    return [b*a for a in a]

def sub(a,b):
    return [a[i]-b[i] for i in range(len(a))]

def normalize(a):
    m = mag(a)
    return [a[i]/m for i in range(len(a))]

class GameWidget(Widget):
    balls = ListProperty([])
    walls = ListProperty([])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.draw_ball(touch.pos)
            self.draw_walls()
            return True
        return super(GameWidget, self).on_touch_down(touch)

    def draw_walls(self):
        w = Wall([100,100,300,600])
        with self.canvas:
            Color(0,0,0,1)
            Line(points=w.pt1+w.pt2)
        self.walls.append(w)

    def collide_wall(self, ball, wall):
        x1 = wall.pt1[0]
        y1 = wall.pt1[1]
        x2 = wall.pt2[0]
        y2 = wall.pt2[1]
        x0 = ball.x + ball.vx
        y0 = ball.y + ball.vy
        top = abs((y2 - y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        bot = math.sqrt(((y2-y1)**2) + ((x2-x1)**2))
        dist = top/bot
        time = dist/abs(math.sqrt(ball.vx**2+ball.vy**2))
        return time <= 1 and x1 <= x0+BALL_SIZE and x2 >= x0+BALL_RADIUS

    def draw_ball(self, pos):
        if len(self.balls) > NUM_BALLS - 1:
            self.clear_widgets(children=[self.balls[0]])
            self.balls = self.balls[1:]
        newBall = Ball()
        newBall.center = pos
        self.add_widget(newBall)
        self.balls.append(newBall)

    def animate(self, dt):
        for ball in self.balls:
            ball.move()
            for wall in self.walls:
                if ball.bounce_timer == 0 and self.collide_wall(ball ,wall):
                    ball.bounce(wall)
                    ball.bounce_timer = 1


            if ball.bounce_timer == 0 and ball.y-ball.r <= 0:
                ball.bounce_timer = 5
                ball.y = 0
                ball.vy *= -.9
            if  ball.x < 0 or ball.x > self.width - BALL_SIZE:
                ball.vx *= -1

class Ball(Widget):
    bounce_timer = 0
    vx = NumericProperty(0)
    vy = NumericProperty(0)
    vel = ReferenceListProperty(vx, vy)
    acc = Vector(0,GRAVITY)
    d = BALL_SIZE
    r = d/2
    disabled = False

    def move(self):
        if not self.disabled:
            if self.bounce_timer > 0:
                self.bounce_timer -= 1
            self.pos = Vector(*self.vel) + self.pos
            self.vy -= GRAVITY

    def bounce(self, wall):
        n = perpendicular(normalize([wall.pt2[0]-wall.pt1[0],wall.pt2[1]-wall.pt1[1]]))
        v = [self.vx,self.vy]
        new = sub(scalar_mult(n, (2*dot(n, v))),v)
        self.vx = -.9*new[0]
        self.vy = -.9*new[1]

class Wall():

    def __init__(self, pts):
        self.pts = pts
        self.pt1 = pts[:2]
        self.pt2 = pts[2:]
        self.length = math.sqrt(((self.pt1[0]-self.pt2[0])**2)+((self.pt1[1]-self.pt2[1])**2))
        self.slope = (self.pt2[1]-self.pt1[1])/(self.pt2[0]-self.pt1[0])

class BallFallApp(App):
    def build(self):
        self.root = root = GameWidget()
        Clock.schedule_interval(root.animate, 1.0/60.0)
        return root

    def update_rect(self,instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    BallFallApp().run()
