import pygame
from Context import Context

pygame.display.set_caption('Reinforcement Learning 2D Driving Car')

context = Context()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    context.update()
    context.draw()
