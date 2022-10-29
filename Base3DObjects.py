from OpenGL.GL import *
from OpenGL.GLU import *

import math
import numpy

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def to_string(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.zf * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def to_string(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class Material:
    def __init__(self, diffuse = None, specular = None, shininess = None, ambient = None, tex_map = None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse == None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular == None else specular
        self.shininess = 1 if shininess == None else shininess
        self.ambient = Color(0.0, 0.0, 0.0) if specular == None else ambient
        self.tex_map = tex_map

class Cube:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]
        self.uv_array = [0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0,
                         0.0, 0.0,
                         0.0, 1.0,
                         1.0, 1.0,
                         1.0, 0.0]

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)

class Sphere:
    def __init__(self, stacks = 12, slices = 12):
        self.vertex_array = []
        self.slices = slices

        stack_interval = math.pi / stacks
        slice_interval = 2.0 * math.pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                self.vertex_array.append(math.sin(stack_angle) * math.cos(slice_angle))
                self.vertex_array.append(math.cos(stack_angle))
                self.vertex_array.append(math.sin(stack_angle) * math.sin(slice_angle))

                self.vertex_array.append(math.sin(stack_angle + stack_interval) * math.cos(slice_angle))
                self.vertex_array.append(math.cos(stack_angle + stack_interval))
                self.vertex_array.append(math.sin(stack_angle + stack_interval) * math.sin(slice_angle))

                self.vertex_count += 2

    def set_vertices(self, shader):
        shader.set_position_attribute(self.vertex_array)
        shader.set_normal_attribute(self.vertex_array)

    def draw(self):
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)

class OptimizedSphere:
    def __init__(self, stacks = 12, slices = 12):
        vertex_array = []
        self.slices = slices

        stack_interval = math.pi / stacks
        slice_interval = 2.0 * math.pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval

                for _ in range(2):
                    vertex_array.append(math.sin(stack_angle) * math.cos(slice_angle))
                    vertex_array.append(math.cos(stack_angle))
                    vertex_array.append(math.sin(stack_angle) * math.sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append(stack_count / stacks)

                for _ in range(2):
                    vertex_array.append(math.sin(stack_angle + stack_interval) * math.cos(slice_angle))
                    vertex_array.append(math.cos(stack_angle + stack_interval))
                    vertex_array.append(math.sin(stack_angle + stack_interval) * math.sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append((stack_count + 1) / stacks)

                self.vertex_count += 2

        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0) # unbind to be able to draw other objects that dont use this metod of binding
        vertex_array = None

    def set_vertices(self, shader):
        shader.set_attribute_buffer_with_uv(self.vertex_buffer_id)

    def draw(self):
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

class MeshModel:
    def __init__(self):
        self.vertex_arrays = dict()
        # self.index_arrays = dict()
        self.mesh_materials = dict()
        self.materials = dict()
        self.vertex_counts = dict()
        self.vertex_buffer_ids = dict()

    def add_vertex(self, mesh_id, position, normal, uv = None):
        if mesh_id not in self.vertex_arrays:
            self.vertex_arrays[mesh_id] = []
            self.vertex_counts[mesh_id] = 0
        self.vertex_arrays[mesh_id] += [position.x, position.y, position.z, normal.x, normal.y, normal.z]
        self.vertex_counts[mesh_id] += 1

    def set_mesh_material(self, mesh_id, mat_id):
        self.mesh_materials[mesh_id] = mat_id

    def add_material(self, mat_id, mat):
        self.materials[mat_id] = mat

    def set_opengl_buffers(self):
        for mesh_id in self.mesh_materials.keys():
            self.vertex_buffer_ids[mesh_id] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_ids[mesh_id])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertex_arrays[mesh_id], dtype='float32'), GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)


    def draw(self, shader):
        for mesh_id, mesh_material in self.mesh_materials.items():
            material = self.materials[mesh_material]
            # print("MAT DIFFUSE: ", material.diffuse.r, material.diffuse.g, material.diffuse.b)
            # print("MAT SPEC: ", material.specular.r, material.specular.g, material.specular.b)
            # print("MAT AMB: ", material.ambient.r, material.ambient.g, material.ambient.b)
            # print("MAT SHINE: ", material.shininess)
            # print("TEX MAP: ", material.tex_map)
            # if (material.tex_map):
            #     tex_id = Texture.load_texture(sys.path[0] + "/textures/" + tex_folder_name + "/" + material.tex_map)
            #     Texture.set_diffuse_tex(shader, tex_id)
            shader.set_mat_diffuse(material.diffuse)
            shader.set_mat_specular(material.specular)
            shader.set_mat_shine(material.shininess)
            amb = Color(material.diffuse.r * 0.2, material.diffuse.g * 0.2, material.diffuse.b * 0.2)
            shader.set_mat_ambient(amb)
            shader.set_attribute_buffer(self.vertex_buffer_ids[mesh_id])
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[mesh_id])
            glBindBuffer(GL_ARRAY_BUFFER, 0)

class BeizerObject:
    def __init__(self, beizer_motion):
        self.beizer_motion = beizer_motion
        self.position_array = self.beizer_motion.get_vertex_list()

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        # shader.set_normal_attribute(self.normal_array)
        # shader.set_uv_attribute(self.uv_array)