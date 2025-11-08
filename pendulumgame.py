import pygame
import threading
from time import time
import matplotlib.pyplot as plt
import math
from collections import deque

class Double_Pendulum:
    def __init__(self, origin_x: float=300, origin_y: float=100, length_rod_1: float=120,
                  length_rod_2: float=120, mass_bob_1: float=10, mass_bob_2: float=10,
                    g: float=9.81, theta_1: float=math.pi/2, theta_2: float=math.pi/2,
                      omega_1: float=0.0, omega_2: float=0.0):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.length_rod_1 = length_rod_1
        self.length_rod_2 = length_rod_2
        self.mass_bob_1 = mass_bob_1
        self.mass_bob_2 = mass_bob_2
        self.g = g # Gravitational Acceleration
        # inital conditions
        self.theta_1 = theta_1 # Theta refers to the angle of the respective bob from vertical
        self.theta_2 = theta_2
        self.omega_1 = omega_1 # Omega refers to the angular velocity of the respective bob
        self.omega_2 = omega_2   
        self.trail_1 = deque([])
        self.trail_2 = deque([])
    
        self.x_1 = self.origin_x + self.length_rod_1 * math.sin(self.theta_1)
        self.y_1 = self.origin_y + self.length_rod_1 * math.cos(self.theta_1)
        self.x_2 = self.x_1 + self.length_rod_2 * math.sin(self.theta_2)
        self.y_2 = self.y_1 + self.length_rod_2 * math.cos(self.theta_2)

    def step(self, dt: float=0.06):
        delta = self.theta_2 - self.theta_1 # Difference in angles
        denominator_1 = (self.mass_bob_1 + self.mass_bob_2) * self.length_rod_1 - self.mass_bob_2 * self.length_rod_1 * math.cos(delta) ** 2
        denominator_2 = (self.length_rod_2 / self.length_rod_1) * denominator_1

        acceleration_1 = (self.mass_bob_2 * self.length_rod_1 * self.omega_1 ** 2 * math.sin(delta) * math.cos(delta) +
              self.mass_bob_2 * self.g * math.sin(self.theta_2) * math.cos(delta) +
              self.mass_bob_2 * self.length_rod_2 * self.omega_2 ** 2 * math.sin(delta) -
              (self.mass_bob_1 + self.mass_bob_2) * self.g * math.sin(self.theta_1)) / denominator_1

        acceleration_2 = (-self.mass_bob_2 * self.length_rod_2 * self.omega_2 ** 2 * math.sin(delta) * math.cos(delta) +
              (self.mass_bob_1 + self.mass_bob_2) * self.g * math.sin(self.theta_1) * math.cos(delta) -
              (self.mass_bob_1 + self.mass_bob_2) * self.length_rod_1 * self.omega_1 ** 2 * math.sin(delta) -
              (self.mass_bob_1 + self.mass_bob_2) * self.g * math.sin(self.theta_2)) / denominator_2

        self.omega_1 += acceleration_1 * dt
        self.omega_2 += acceleration_2 * dt
        self.theta_1 += self.omega_1 * dt
        self.theta_2 += self.omega_2 * dt

        self.x_1 = self.origin_x + self.length_rod_1 * math.sin(self.theta_1)
        self.y_1 = self.origin_y + self.length_rod_1 * math.cos(self.theta_1)
        self.x_2 = self.x_1 + self.length_rod_2 * math.sin(self.theta_2)
        self.y_2 = self.y_1 + self.length_rod_2 * math.cos(self.theta_2)
        self.trail_1.append((self.x_1, self.y_1))
        self.trail_2.append((self.x_2, self.y_2))


    def get_coords(self):
        return [
            {'x': self.x_1, 'y': self.y_1},
            {'x': self.x_2, 'y': self.y_2}
        ]
    
    
pygame.init()
screen = pygame.display.set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0)
clock = pygame.time.Clock()
running = True
screen_width = pygame.display.get_desktop_sizes()[0][0]
double_pendulum = Double_Pendulum(screen_width//2, 100)

times = []
omega1_data = []
omega2_data = []
x_1_data = []
x_2_data = []
y_1_data = []
y_2_data = []
start_time = time()


plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [], color= '#34158A', label='B1')
line2, = ax.plot([], [], color= '#91D317', label='B2')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    double_pendulum.step()
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#0C0B0B")

    coords = double_pendulum.get_coords()
    

    if len(times) > 2:
            line1.set_data(x_1_data,y_1_data)
            line2.set_data(x_2_data, y_2_data)
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.01)

    t = time() - start_time
    times.append(t)
    x_1_data.append(double_pendulum.x_1)
    x_2_data.append(double_pendulum.x_2)
    y_1_data.append(double_pendulum.y_1)
    y_2_data.append(double_pendulum.y_2)


    if len(times) > 1000:  # limit to avoid memory growth
        times.pop(0)
        x_1_data.pop(0)
        x_2_data.pop(0)
        y_1_data.pop(0)
        y_2_data.pop(0)


    pygame.draw.circle(screen, "#F0DDD2", (screen_width//2, 100), 10)


    pygame.draw.line(screen, "#F0DDD2", (double_pendulum.origin_x, double_pendulum.origin_y), (coords[0]['x'], coords[0]['y']), 2)
    pygame.draw.line(screen, "#F0DDD2", (coords[0]['x'], coords[0]['y']), (coords[1]['x'], coords[1]['y']), 2)
   
    pygame.draw.circle(screen, "#34158A", (coords[0]['x'], coords[0]['y']), 10)
    pygame.draw.circle(screen, "#91D317", (coords[1]['x'], coords[1]['y']), 10)
    
    if len (double_pendulum.trail_1)>= 2:
        pygame.draw.lines(screen, "#34158A", False, double_pendulum.trail_1, width=1)

    if len (double_pendulum.trail_2)>= 2:
        pygame.draw.lines(screen, "#91D317", False, double_pendulum.trail_2, width=1)

    if len (double_pendulum.trail_1) > 400:
        double_pendulum.trail_1.popleft()

    if len (double_pendulum.trail_2) > 400:
        double_pendulum.trail_2.popleft()
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
running = False

