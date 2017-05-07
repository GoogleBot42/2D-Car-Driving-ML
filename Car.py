import Box2D.b2
import math
import pygame


class Car:
    def __init__(self, context, x, y, controller):
        self.context = context
        self.x = x
        self.y = y
        self.controller = controller

        car, wheels, springs = create_car(context.world, offset=(
            x, y), wheel_radius=0.5, wheel_separation=2.0, scale=(1.5, 1.5), density=2.0)
        self.car = car
        self.wheels = wheels
        self.springs = springs

    def update(self):
        self.context.offset[0] = self.car.position[0] * self.context.PPM - self.context.SCREEN_WIDTH/2
        self.context.offset[1] = self.car.position[1] * self.context.PPM - self.context.SCREEN_HEIGHT/2
        self.context.offset[1] *= -1
        # print(self.context.offset[0], self.context.offset[1], self.car.position)
        
        action = self.controller.getNextAction(self.car.position)
        
        if abs(action) < 1:
            self.springs[0].motorSpeed = 0
            self.springs[1].motorSpeed = 0
        else:
            self.springs[0].motorSpeed = -action
            self.springs[1].motorSpeed = -action

    def draw(self):
        for wheel in self.wheels:
            worldPos = wheel.worldCenter
            fixture = wheel.fixtures[0]
            shape = fixture.shape
            
            pos = (shape.pos[0] + worldPos[0], shape.pos[1] + worldPos[1])
            pos = (pos[0] * self.context.PPM, pos[1] * self.context.PPM)
            pos = (pos[0], self.context.SCREEN_HEIGHT - pos[1])
            pos = (pos[0] - self.context.offset[0], pos[1] - self.context.offset[1])
            pos = (math.floor(pos[0]), math.floor(pos[1]))
            radius = math.floor(shape.radius * self.context.PPM)
            pygame.draw.circle(self.context.screen, (127, 127, 255, 255), pos, radius)
            
            circleOutter = (math.cos(-wheel.angle) * radius + pos[0], (math.sin(-wheel.angle) * radius + pos[1]))
            circleOutter = (math.floor(circleOutter[0]), math.floor(circleOutter[1]))
            pygame.draw.line(self.context.screen, (255,255,255,255), pos, circleOutter)
            
        for fixture in self.car.fixtures:
            shape = fixture.shape
            vertices = [(self.car.transform * v) * self.context.PPM for v in shape.vertices]
            vertices = [(v[0], self.context.SCREEN_HEIGHT - v[1]) for v in vertices]
            vertices = [(v[0] - self.context.offset[0], v[1] - self.context.offset[1]) for v in vertices]
            pygame.draw.polygon(self.context.screen, (127, 255, 127, 255), vertices)
     
    def destroy(self):
        self.context.world.DestroyBody(self.car)
        for wheel in self.wheels:
            self.context.world.DestroyBody(wheel)


def create_car(world, offset, wheel_radius, wheel_separation, density=1.0,
               wheel_friction=0.9, scale=(1.0, 1.0), chassis_vertices=None,
               wheel_axis=(0.0, 1.0), wheel_torques=[150.0, 150.0],
               wheel_drives=[True, True], hz=4.0, zeta=0.7, **kwargs):
    """
    """
    x_offset, y_offset = offset
    scale_x, scale_y = scale
    if chassis_vertices is None:
        chassis_vertices = [
            (-1.5, -0.5),
            (1.5, -0.5),
            (1.5, 0.0),
            (0.0, 0.9),
            (-1.15, 0.9),
            (-1.5, 0.2),
        ]

    chassis_vertices = [(scale_x * x, scale_y * y)
                        for x, y in chassis_vertices]
    radius_scale = math.sqrt(scale_x ** 2 + scale_y ** 2)
    wheel_radius *= radius_scale

    chassis = world.CreateDynamicBody(
        position=(x_offset, y_offset),
        fixtures=Box2D.b2.fixtureDef(
            shape=Box2D.b2.polygonShape(vertices=chassis_vertices),
            density=density,
        )
    )

    wheels, springs = [], []
    wheel_xs = [-wheel_separation * scale_x /
                2.0, wheel_separation * scale_x / 2.0]
    for x, torque, drive in zip(wheel_xs, wheel_torques, wheel_drives):
        wheel = world.CreateDynamicBody(
            position=(x_offset + x, y_offset - wheel_radius),
            fixtures=Box2D.b2.fixtureDef(
                shape=Box2D.b2.circleShape(radius=wheel_radius),
                density=density,
                friction=wheel_friction,
            )
        )

        spring = world.CreateWheelJoint(
            bodyA=chassis,
            bodyB=wheel,
            anchor=wheel.position,
            axis=wheel_axis,
            motorSpeed=0.0,
            maxMotorTorque=torque,
            enableMotor=drive,
            frequencyHz=hz,
            dampingRatio=zeta
        )

        wheels.append(wheel)
        springs.append(spring)

    return chassis, wheels, springs