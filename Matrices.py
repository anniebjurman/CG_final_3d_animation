import math
import Base3DObjects

class ModelMatrix:
    def __init__(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]
        self.stack = []
        self.stack_count = 0
        self.stack_capacity = 0

    def load_identity(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]

    def copy_matrix(self):
        new_matrix = [0] * 16
        for i in range(16):
            new_matrix[i] = self.matrix[i]
        return new_matrix

    def add_transformation(self, matrix2):
        counter = 0
        new_matrix = [0] * 16
        for row in range(4):
            for col in range(4):
                for i in range(4):
                    new_matrix[counter] += self.matrix[row*4 + i]*matrix2[col + 4*i]
                counter += 1
        self.matrix = new_matrix

    def add_scale(self, x = 1, y = 1, z = 1):
        other_matrix = [x, 0, 0, 0,
                        0, y, 0, 0,
                        0, 0, z, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_translation(self, x = 0, y = 0, z = 0):
        other_matrix = [1, 0, 0, x,
                        0, 1, 0, y,
                        0, 0, 1, z,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_rotation(self, angle, axis):
        if axis == 'x':
            other_matrix = [1, 0, 0, 0,
                            0, math.cos(angle * math.pi / 180), -math.sin(angle * math.pi / 180), 0,
                            0, math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180), 0,
                            0, 0, 0, 1]
        elif axis == 'y':
            other_matrix = [math.cos(angle * math.pi / 180), 0, math.sin(angle * math.pi / 180), 0,
                            0, 1, 0, 0,
                            -math.sin(angle * math.pi / 180), 0, math.cos(angle * math.pi / 180), 0,
                            0, 0, 0, 1]
        elif axis == 'z':
            other_matrix = [math.cos(angle * math.pi / 180), -math.sin(angle * math.pi / 180), 0, 0,
                            math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180), 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1]
        else:
            other_matrix = [1, 0, 0, 0,
                            0, 1, 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1]

        self.add_transformation(other_matrix)

    def push_matrix(self):
        self.stack.append(self.copy_matrix())

    def pop_matrix(self):
        self.matrix = self.stack.pop()

    def __str__(self):
        ret_str = ""
        counter = 0
        for _ in range(4):
            ret_str += "["
            for _ in range(4):
                ret_str += " " + str(self.matrix[counter]) + " "
                counter += 1
            ret_str += "]\n"
        return ret_str



# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation

class ViewMatrix:
    def __init__(self):
        self.eye = Base3DObjects.Point(0, 0, 0)
        self.u = Base3DObjects.Vector(1, 0, 0)
        self.v = Base3DObjects.Vector(0, 1, 0)
        self.n = Base3DObjects.Vector(0, 0, 1)

    def look(self, eye: Base3DObjects.Vector, center: Base3DObjects.Vector, up: Base3DObjects.Vector):
        self.eye = eye
        self.n = Base3DObjects.Vector(eye[0] - center[0], eye[1] - center[1], eye[2] - center[2])
        self.u = up.cross(self.n)
        self.v = self.n.cross(self.u)

    def slide(self, del_u, del_v, del_n):
        self.eye.x += del_u * self.u.x + del_v * self.v.x + del_n * self.n.x
        self.eye.y += del_u * self.u.y + del_v * self.v.y + del_n* self.n.y
        self.eye.z += del_u * self.u.z + del_v * self.v.z + del_n * self.n.z

    # Does not change or use the y-coordinates of the camera’s coordinate frame.
    def walk(self, del_u, del_v, del_n):
        self.eye.x += del_u * self.u.x + del_v * self.v.x + del_n * self.n.x
        self.eye.z += del_u * self.u.z + del_v * self.v.z + del_n * self.n.z

    # rotate camera about the n-axis
    def roll(self, angle):
        ang_cos = math.cos(angle * math.pi/180.0)
        ang_sin = math.sin(angle * math.pi/180.0)
        u_org = self.u # store original u

        self.u = Base3DObjects.Vector(ang_cos * u_org.x + ang_sin * self.v.x,
                        ang_cos * u_org.y + ang_sin * self.v.y,
                        ang_cos * u_org.z + ang_sin * self.v.z)

        self.v = Base3DObjects.Vector(- ang_sin * u_org.x + ang_cos * self.v.x,
                        - ang_sin * u_org.y + ang_cos * self.v.y,
                        - ang_sin * u_org.z + ang_cos * self.v.z)

    # rotate camera about the u-axis
    def pitch(self, angle):
        ang_cos = math.cos(angle * math.pi/180.0)
        ang_sin = math.sin(angle * math.pi/180.0)
        n_org = self.n # store original n

        self.n = Base3DObjects.Vector(ang_cos * n_org.x + ang_sin * self.v.x,
                        ang_cos * n_org.y + ang_sin * self.v.y,
                        ang_cos * n_org.z + ang_sin * self.v.z)

        self.v = Base3DObjects.Vector(- ang_sin * n_org.x + ang_cos * self.v.x,
                        - ang_sin * n_org.y + ang_cos * self.v.y,
                        - ang_sin * n_org.z + ang_cos * self.v.z)

    # rotate camera about the v-axis
    def yaw(self, angle):
        ang_cos = math.cos(angle * math.pi/180.0)
        ang_sin = math.sin(angle * math.pi/180.0)
        n_org = self.n # store original n

        self.n = Base3DObjects.Vector(ang_cos * n_org.x + ang_sin * self.u.x,
                        ang_cos * n_org.y + ang_sin * self.u.y,
                        ang_cos * n_org.z + ang_sin * self.u.z)

        self.u = Base3DObjects.Vector(- ang_sin * n_org.x + ang_cos * self.u.x,
                        - ang_sin * n_org.y + ang_cos * self.u.y,
                        - ang_sin * n_org.z + ang_cos * self.u.z)

    # rotate all the vectors (u, v and n) about the base y-axis
    def turn(self, angle):
        self.u = self.rotate_around_y(self.u, angle * math.pi / 180)
        self.v = self.rotate_around_y(self.v, angle * math.pi / 180)
        self.n = self.rotate_around_y(self.n, angle * math.pi / 180)

    def rotate_around_y(self, v, angle):
        return Base3DObjects.Vector(v.x * math.cos(angle) + v.z * math.sin(angle),
                      v.y,
                      v.x * -math.sin(angle) + v.z * math.cos(angle))

    def get_matrix(self):
        minusEye = Base3DObjects.Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0,        0,        0,        1]

    def to_string(self):
        matrix = self.get_matrix()
        string = "[ " + str(matrix[0]) + ", " + str(matrix[1]) + ", " + str(matrix[2]) + ", " + str(matrix[3]) + ",\n" \
                      + str(matrix[4]) + ", " + str(matrix[5]) + ", " + str(matrix[6]) + ", " + str(matrix[7]) + ",\n" \
                      + str(matrix[8]) + ", " + str(matrix[9]) + ", " + str(matrix[10]) + ", " + str(matrix[11]) + " ]"
        return string

    def values_to_string(self):
        return "View matrix:\n" + "\teye: " + self.eye.to_string() + "\n\tu: " + \
                self.u.to_string() + "\n\tn: " + self.n.to_string() + "\n\tv: " + \
                self.v.to_string()


# The ProjectionMatrix class builds transformations concerning
# the camera's "lens"

class ProjectionMatrix:
    def __init__(self):
        self.left = -1
        self.right = 1
        self.bottom = -1
        self.top = 1
        self.near = -1
        self.far = 1

        self.is_orthographic = True

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.is_orthographic = True
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far

    def get_matrix(self):
        if self.is_orthographic:
            A = 2 / (self.right - self.left)
            B = -(self.right + self.left) / (self.right - self.left)
            C = 2 / (self.top - self.bottom)
            D = -(self.top + self.bottom) / (self.top - self.bottom)
            E = 2 / (self.near - self.far)
            F = (self.near + self.far) / (self.near - self.far)

            return [A,0,0,B,
                    0,C,0,D,
                    0,0,E,F,
                    0,0,0,1]
        else:
            # matrix for a Perspective projection
            A = (2 * self.near) / (self.right - self.left)
            B = (self.right + self.left) / (self.right - self.left)
            C = (2 * self.near) / (self.top - self.bottom)
            D = (self.top + self.bottom) / (self.top - self.bottom)
            E = -(self.far + self.near) / (self.far - self.near)
            F = -(2 * self.far * self.near) / (self.far - self.near)

            return [A, 0, B, 0,
                    0, C, D, 0,
                    0, 0, E, F,
                    0, 0, -1, 0]

    def set_perspective(self, fov, aspect, near, far):
        self.is_orthographic = False
        fov_rad = (fov * math.pi) / 180.0

        self.top = near * math.tan(fov_rad / 2)
        self.bottom = -self.top
        self.right = self.top * aspect
        self.left = -self.right
        self.near = near
        self.far = far