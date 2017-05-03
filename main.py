import pygame
import Box2D

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS

pygame.display.set_caption('Reinforcement Learning 2D Driving Car')

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create the world
world = Box2D.b2.world(gravity=(0, -10), doSleep=True)

done = False
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        screen.fill((0, 0, 0, 0))

        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))

        pygame.display.flip()
