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
        self.static = False

        if self.p1.is_same_as(self.p2) and self.p2.is_same_as(self.p3) and self.p3.is_same_as(self.p4):
            self.static = True

    def get_current_pos(self, curr_time: float):
        if self.static:
            out_pos = self.p1
        elif (curr_time < self.start_time):
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
    def __init__(self, control_points, start_time, end_time,
                 start_scale = None, end_scale = None, rot_angle = None, rot_axis = None):
        self.beizer_motions = []
        self.times = []
        self.start_scale = start_scale
        self.end_scale = end_scale
        self.start_time = start_time
        self.end_time = end_time
        self.rot_angle = rot_angle
        self.rot_axis = rot_axis

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
            v = control_points[3].__sub__(control_points[2])
            v_scaled = v.__mul__(0.7)
            b2 = control_points[3].__add__(v_scaled)

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
        if self.start_scale is None:
            return 1.0
        else:
            if curr_time < self.start_time:
                return self.start_scale
            elif curr_time > self.end_time:
                return self.end_scale
            else:
                tot_time = self.end_time - self.start_time
                part_time = (curr_time - self.start_time) / tot_time

                curr_scale = (1 - part_time) * self.start_scale + part_time * self.end_scale
                return curr_scale

    def get_curr_rot_angle(self, curr_time):
        if self.rot_angle is None:
            return 0
        else:
            if curr_time < self.start_time:
                return 0
            elif curr_time > self.end_time:
                return self.rot_angle
            else:
                tot_time = self.end_time - self.start_time
                part_time = (curr_time - self.start_time) / tot_time

                curr_rot_angle = part_time * self.rot_angle
                return curr_rot_angle

class CameraTurn:
    def __init__(self, start_time: float, end_time: float, dir: str, angle_speed: float):
        self.start_time = start_time
        self.end_time = end_time
        self.dir = dir
        self.angle_speed = angle_speed

    def turn_camera(self, curr_time: float, shader, view_matrix):
        if curr_time > self.start_time and curr_time < self.end_time:
            if self.dir == "right":
                view_matrix.turn(-self.angle_speed)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "left":
                view_matrix.turn(self.angle_speed)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "up":
                view_matrix.pitch(-self.angle_speed)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "down":
                view_matrix.pitch(self.angle_speed)
                shader.set_view_matrix(view_matrix.get_matrix())

class CameraWalk:
    def __init__(self, start_time: float, end_time: float, dir: str, speed: float):
        self.start_time = start_time
        self.end_time = end_time
        self.dir = dir
        self.walk_speed = speed

    def walk_camera(self, curr_time: float, shader, view_matrix):
        if curr_time > self.start_time and curr_time < self.end_time:
            if self.dir == "forward":
                view_matrix.walk(0, 0, -self.walk_speed)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "backward":
                view_matrix.walk(0, 0, self.walk_speed)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "left":
                view_matrix.walk(-self.walk_speed, 0, 0)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "right":
                view_matrix.walk(self.walk_speed, 0, 0)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "up":
                view_matrix.slide(0, self.walk_speed, 0)
                shader.set_view_matrix(view_matrix.get_matrix())
            if self.dir == "down":
                view_matrix.slide(0, -self.walk_speed, 0)
                shader.set_view_matrix(view_matrix.get_matrix())