import Box2D.b2
import math


class Car:
    def __init__(self, context, x, y):
        self.context = context
        self.x = x
        self.y = y

        car, wheels, springs = create_car(context.world, offset=(
            0.0, 1.0), wheel_radius=0.4, wheel_separation=2.0, scale=(1, 1))
        self.car = car
        self.wheels = wheels
        self.springs = springs


    def update(self):
        pass

    def draw(self):
        pass


def create_car(world, offset, wheel_radius, wheel_separation, density=1.0,
               wheel_friction=0.9, scale=(1.0, 1.0), chassis_vertices=None,
               wheel_axis=(0.0, 1.0), wheel_torques=[20.0, 10.0],
               wheel_drives=[True, False], hz=4.0, zeta=0.7, **kwargs):
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