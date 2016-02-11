#!/usr/bin/env python
import pygame
import random
import math
### Started with the code from http://www.petercollingridge.co.uk/pygame-physics-simulation/collisions

pygame.init()
background_colour = (255,255,255)
(width, height) = (800, 800)
elasticity = 1

def detectCollide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    if not (p1.alive and p2.alive):
        return False

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed*elasticity
        speed2 = p1.speed*elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)
        return True
    return False


def agentCollide(agent1, agent2):
    if (agent1.size == agent2.size):
        return 

    transAmt = 50 * (agent1.size - agent2.size)/abs((agent1.size - agent2.size))


    deltaR1 = ((math.pi * math.pow(agent1.size, 2)) + transAmt)
    deltaR1 = deltaR1 / math.pi
    if (deltaR1 >= 0):
        if (transAmt>0):
            agent1.size = int(math.ceil(math.sqrt(deltaR1)))
        else:
            agent1.size = int(math.floor(math.sqrt(deltaR1)))
    else:
        agent1.alive = False

    deltaR2 = ((math.pi * math.pow(agent2.size, 2)) - transAmt)
    deltaR2 = deltaR2 / math.pi
    if (deltaR2 >= 0):
        if (transAmt<0):
            agent2.size = int(math.ceil(math.sqrt(deltaR2)))
        else:
            agent2.size = int(math.floor(math.sqrt(deltaR2)))            
    else:
        agent2.alive = False
    



class Agent():
    def __init__(self, (x, y), size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.alive = True

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Circle Muncher')

number_of_agents = 200
my_agents = []

for n in range(number_of_agents):
    size = random.randint(1, 2)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)

    agent = Agent((x, y), size)
    agent.speed = random.random()
    agent.angle = random.uniform(0, 0)#math.pi*2)

    my_agents.append(agent)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_colour)


    for i, agent in enumerate(my_agents):
        agent.move()
        agent.bounce()
        for agent2 in my_agents[i+1:]:
            if (detectCollide(agent, agent2)):
                agentCollide(agent, agent2)
    for i, agent in enumerate(my_agents):
        if not agent.alive:
            my_agents.pop(i)
            number_of_agents -= 1
        agent.display()


#     human = my_agents[0]
#     vel_x = human.speed* math.cos(human.angle)
#     vel_y = human.speed* math.sin(human.angle)
#     vec = [vel_x, vel_y]
#     deltaVec = [0, 0]
#     change = 1

#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_LEFT:
#             print "left"
#             deltaVec = [x * change for x in [-1,0]]
#         elif event.key == pygame.K_RIGHT:
#             print "right"
#             deltaVec = [x * change for x in [1,0]]
#         elif event.key == pygame.K_UP:
#             print "up"
#             deltaVec = [x * change for x in [0,1]]
#         elif event.key == pygame.K_DOWN:
#             print "down"
#             deltaVec = [x * change for x in [0,1]]
# #    if event.type == pygame.KEYUP:
# #        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

#     vec = [deltaVec[0]*vec[0], deltaVec[1]*vec[1]]
#     my_agents[0].speed = math.sqrt(vec[0]**2 +vec[1]**2)
#     #my_agents[0].angle = angle_wrt_x()
#     print vec
    pygame.display.flip()
