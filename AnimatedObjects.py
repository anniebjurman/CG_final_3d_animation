import Base3DObjects

class ASphere:
    def __init__(self, size):
        self.smallest_height = 0.02
        self.object = Base3DObjects.Sphere(20, 20)
        self.height = self.smallest_height
        self.width = size
        self.movement_speed = 0.005

    def increase_height(self):
        if self.height < self.width:
            if self.height < self.width - 1:
                self.height += self.movement_speed
            else:
                self.height += self.movement_speed / 2
        else:
            return False

    def decrease_height(self):
        if self.height > self.smallest_height:
            self.height -= self.movement_speed
        else:
            return False
