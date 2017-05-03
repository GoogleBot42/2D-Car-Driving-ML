import pygame
import Box2D
from Context import Context

pygame.display.set_caption('Reinforcement Learning 2D Driving Car')

# Create the world
world = Box2D.b2.world(gravity=(0, -9.81), doSleep=True)

context = Context(world)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    context.update()
    context.draw()
