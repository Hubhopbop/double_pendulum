import pygame 
import threading
from time import time
import matplotlib.pyplot as plt
import math
from collections import deque
import sys
import pygame.font
import pygame.event
import pygame.draw


m1 = (float(input("Mass 1 (Default is 10 units): ")))
m2 = (float(input("Mass 2 (Default is 10 units): ")))
t1 = (float(input("Angle 1 (Default is pi/2): ")))
t2 = (float(input("Angle 2 (Default is pi/2): ")))
o1 = (float(input("Acceleration of mass 1 (Default is 0): ")))
o2 = (float(input("Acceleration of mass 2 (Default is 0): ")))

class Double_Pendulum:
    def __init__(self, origin_x: float=300, origin_y: float=100, length_rod_1: float=120,
                  length_rod_2: float=120, mass_bob_1: float=10, mass_bob_2: float=10,
                    g: float=9.81, theta_1: float=math.pi/2, theta_2: float=math.pi/2,
                      omega_1: float=0.0, omega_2: float=0.0):
        self.paused = False
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
        if (self.paused): 
            return
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

    def toggle_pause(self):
        self.paused = not self.paused
    
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
screen_height = pygame.display.get_desktop_sizes()[0][1]
double_pendulum = Double_Pendulum(screen_width//2, screen_height//2, mass_bob_1= m1, mass_bob_2= m2, theta_1= t1, theta_2= t2, omega_1= o1, omega_2= o2 )

def run_simulation():
    while True:
        double_pendulum.step()
        threading.Event().wait(0.01)

threading.Thread(target=run_simulation, daemon=True).start()

times = []
omega1_data = []
omega2_data = []
theta1_data = []
theta2_data = []
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
fig1, ax1 = plt.subplots()
line3, = ax1.plot([], [], color= "#8A1515", label='θ1')
line4, = ax1.plot([], [], color= "#D3A117", label='θ2')
ax1.set_xlabel('Y')
ax1.set_ylabel('X')
ax1.legend()
ax1.grid(True)
fig2, ax2 = plt.subplots()
line5, = ax2.plot([], [], color= "#154C8A", label='ω1')
line6, = ax2.plot([], [], color= "#D35217", label='ω2')
ax2.set_xlabel('Y')
ax2.set_ylabel('X')
ax2.legend()
ax2.grid(True)

font = pygame.sysfont.SysFont("Arial", 25)

def draw_pause_menu():
    pause_text = font.render("SOCORRO AAAA", True, "#FFFFFF")

    text_rect = pause_text.get_rect(center=(screen_width// 2, screen_height//2))
    screen.blit(pause_text, text_rect)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                double_pendulum.toggle_pause()
    
    # fill the screen with a color to wipe away anything fr1om last frame
    screen.fill("#0C0B0B")

    coords = double_pendulum.get_coords()
  
    


    if len(times) > 2:
            line1.set_data(x_1_data,y_1_data)
            line2.set_data(x_2_data, y_2_data)
            ax.relim()
            ax.autoscale_view()
            line3.set_data(times, theta1_data)
            line4.set_data(times, theta2_data)
            ax1.relim()
            ax1.autoscale_view()
            line5.set_data(times, omega1_data)
            line6.set_data(times, omega2_data)
            ax2.relim()
            ax2.autoscale_view()
            plt.pause(0.01)

    t = time() - start_time
    times.append(t)
    x_1_data.append(double_pendulum.x_1)
    x_2_data.append(double_pendulum.x_2)
    y_1_data.append(double_pendulum.y_1)
    y_2_data.append(double_pendulum.y_2)
    theta1_data.append(double_pendulum.theta_1)
    theta2_data.append(double_pendulum.theta_2)
    omega1_data.append(double_pendulum.omega_1)
    omega2_data.append(double_pendulum.omega_2)


    if len(times) > 1000:  # limit to avoid memory growth
        times.pop(0)
        x_1_data.pop(0)
        x_2_data.pop(0)
        y_1_data.pop(0)
        y_2_data.pop(0)
        theta1_data.pop(0)
        theta2_data.pop(0)
        omega1_data.pop(0)
        omega2_data.pop(0)
  
    if double_pendulum.paused:
        draw_pause_menu()  # Draw pause indicator


    pygame.draw.circle(screen, "#F0DDD2", (screen_width//2, screen_height//2), 10)


    pygame.draw.line(screen, "#F0DDD2", (double_pendulum.origin_x, double_pendulum.origin_y), (coords[0]['x'], coords[0]['y']), 2)
    pygame.draw.line(screen, "#F0DDD2", (coords[0]['x'], coords[0]['y']), (coords[1]['x'], coords[1]['y']), 2)
   
    pygame.draw.circle(screen, "#34158A", (coords[0]['x'], coords[0]['y']), 10)
    pygame.draw.circle(screen, "#91D317", (coords[1]['x'], coords[1]['y']), 10)
    
    if len (double_pendulum.trail_1)>= 2:
        pygame.draw.lines(screen, "#34158A", False, double_pendulum.trail_1, width=1)

    if len (double_pendulum.trail_2)>= 2:
        pygame.draw.lines(screen, "#91D317", False, double_pendulum.trail_2, width=1)

    if len (double_pendulum.trail_1) > 300:
        double_pendulum.trail_1.popleft()

    if len (double_pendulum.trail_2) > 300:
        double_pendulum.trail_2.popleft()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
running = False

