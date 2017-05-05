import Box2D.b2


class Car:
    def __init__(self, context, x, y):
        self.context = context
        self.x = x
        self.y = y

        # create box2d car object

        # car body
        # bodyDef = Box2D.b2.bodyDef()
        # car = context.world.CreateBody(bodyDef)
        #
        # box = context.world.CreateDynamicBody(
        #     position=(x, y),
        #     shapes=Box2D.b2.polygonShape(density=2, friction=0.5, box=(2, 1))
        # )

        # car axles

        # car wheels

        # joints

    def update(self):
        pass

    def draw(self):
        pass
