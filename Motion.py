from distutils.util import convert_path
from lib2to3.pytree import Base
from tracemalloc import start
import Base3DObjects
import math
import numpy

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

class BezierMotion:
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

    def get_vertex_list(self):
        v_list = []
        for x in numpy.linspace(self.start_time, self.end_time, 30):
            pos = self.get_current_pos(x)
            v_list.extend([pos.x/10, pos.y/10, pos.z/10])
        v_list = [0.3, 0.4, 0.1, 0.0, 0.2, 0.4]
        print(v_list)
        return v_list

class BeizerObject:
    def __init__(self, control_points, start_time, end_time, start_scale = None, end_scale = None):
        self.beizer_motions = []
        self.times = []
        self.start_scale = start_scale
        self.end_scale = end_scale
        self.start_time = start_time
        self.end_time = end_time

        if len(control_points) == 4:
            self.beizer_motions.append(BezierMotion(control_points[0],
                                              control_points[1],
                                              control_points[2],
                                              control_points[3],
                                              start_time,
                                              end_time))
            self.times.extend([start_time, end_time])

        elif len(control_points) == 6:
            middle_time = start_time + ((end_time - start_time) / 2)
            self.times.extend([start_time, middle_time, end_time])

            self.beizer_motions.append(BezierMotion(control_points[0],
                                              control_points[1],
                                              control_points[2],
                                              control_points[3],
                                              start_time,
                                              middle_time))

            # calc b2
            v  = control_points[2].__sub__(control_points[3])
            v_scalar = v.__mul__(1)
            b2 = Base3DObjects.Point(control_points[3].x + v_scalar.x,
                                     control_points[3].y + v_scalar.y,
                                     control_points[3].z + v_scalar.z)

            self.beizer_motions.append(BezierMotion(control_points[3],
                                                    b2,
                                                    control_points[4],
                                                    control_points[5],
                                                    middle_time,
                                                    end_time))

    def get_current_pos(self, curr_time: float):
        if len(self.beizer_motions) == 1:
            return self.beizer_motions[0].get_current_pos(curr_time)
        elif len(self.beizer_motions) == 2:
            if curr_time <= self.times[1]:
                return self.beizer_motions[0].get_current_pos(curr_time)
            elif curr_time > self.times[1]:
                return self.beizer_motions[1].get_current_pos(curr_time)

    def get_current_scale(self, curr_time):
        if curr_time < self.start_time:
            return self.start_scale
        elif curr_time > self.end_time:
            return self.end_scale
        else:
            tot_time = self.end_time - self.start_time
            part_time = (curr_time - self.start_time) / tot_time

            curr_scale = (1 - part_time) * self.start_scale + part_time * self.end_scale
            return curr_scale