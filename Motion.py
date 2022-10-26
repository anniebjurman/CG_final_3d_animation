import Base3DObjects
import math

class LinearMotion:
    def __init__(self,
                 p1: Base3DObjects.Point,
                 p2: Base3DObjects.Point,
                 start_time: float,
                 end_time: float):
        self.p1 = p1
        self.p2 = p2
        self.start_time = start_time
        self.end_time = end_time

    def get_current_pos(self, curr_time: float):
        if (curr_time < self.start_time):
            out_pos = self.p1
        elif (curr_time > self.end_time):
            out_pos = self.p2
        else:
            t = (curr_time - self.start_time) / (self.end_time - self.start_time)
            x = (1.0 - t) * self.p1.x + t * self.p2.x
            y = (1.0 - t) * self.p1.y + t * self.p2.y
            z = (1.0 - t) * self.p1.z + t * self.p2.z

            out_pos = Base3DObjects.Point(x, y, z)
        return out_pos

class BeiserMotion:
    def __init__(self,
                 p1: Base3DObjects.Point,
                 p2: Base3DObjects.Point,
                 p3: Base3DObjects.Point,
                 p4: Base3DObjects.Point,
                 start_time: float,
                 end_time: float):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.start_time = start_time
        self.end_time = end_time

    def get_current_pos(self, curr_time: float):
        if (curr_time < self.start_time):
            out_pos = self.p1
        elif (curr_time > self.end_time):
            out_pos = self.p4
        else:
            t = (curr_time - self.start_time) / (self.end_time - self.start_time)

            x = math.pow((1.0 - t), 3) * self.p1.x + \
                3 * t * math.pow((1.0 - t), 2) * self.p2.x + \
                3 * math.pow(t, 2) * (1.0 - t) + \
                math.pow(t, 3) * self.p4.x

            y = math.pow((1.0 - t), 3) * self.p1.y + \
                3 * t * math.pow((1.0 - t), 2) * self.p2.y + \
                3 * math.pow(t, 2) * (1.0 - t) + \
                math.pow(t, 3) * self.p4.y

            z = math.pow((1.0 - t), 3) * self.p1.z + \
                3 * t * math.pow((1.0 - t), 2) * self.p2.z + \
                3 * math.pow(t, 2) * (1.0 - t) + \
                math.pow(t, 3) * self.p4.z

            out_pos = Base3DObjects.Point(x, y, z)
        return out_pos
