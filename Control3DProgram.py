import math
import sys
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

import Matrices
import Shaders
import Base3DObjects
import Motion
import Texture
import obj3DLoading

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shaders.Shader3D()
        self.shader.use()
        self.shader.set_using_texture(0.0)

        self.model_matrix = Matrices.ModelMatrix()

        self.sphere_width = 80

        self.projection_matrix = Matrices.ProjectionMatrix()
        self.projection_matrix.set_perspective(60, 1920/1080, 0.8, 150)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix = Matrices.ViewMatrix()

        # set camera
        self.view_matrix.eye = Base3DObjects.Point(self.sphere_width/2, self.sphere_width/2 + 3, -self.sphere_width/2 + 15)             #make 5 a variable dependent on the floor dim
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # set light
        self.shader.set_light_position(Base3DObjects.Point(20, 50, -20))

        # General objects
        self.cube = Base3DObjects.Cube()
        self.opt_sphere = Base3DObjects.OptimizedSphere(24, 48)
        self.sphere = Base3DObjects.Sphere(20, 20)

        # Time
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.time_elapsed = 0

        #motion
        control_points = [Base3DObjects.Point(-20, 1, 0),
                          Base3DObjects.Point(-5, 10, -20),
                          Base3DObjects.Point(15, 10, -20),
                          Base3DObjects.Point(20, 1, 0),
                          Base3DObjects.Point(-5, 10, 20),
                          Base3DObjects.Point(-20, 1, 0)]
        self.beizer_obj = Motion.BeizerObject(control_points, 5.0, 20.0)
        self.model_pos_bez = Base3DObjects.Point(0,0,0)

        # Other objects
        self.obj_model_person = obj3DLoading.load_obj_file(sys.path[0] + "/models", "person.obj")
        self.obj_model_ghost = obj3DLoading.load_obj_file(sys.path[0] + "/models", "ghost2.obj")

        # Angles
        self.angle = 0
        self.angle_turn = 0.1
        self.delta_time = None
        self.angle_deg = None

        # Camera controll
        self.UP_key_right = False
        self.UP_key_left = False
        self.UP_key_up = False
        self.UP_key_down = False

        self.UP_key_w = False
        self.UP_key_s = False
        self.UP_key_a = False
        self.UP_key_d = False

        # textures
        self.texture_id_01 = Texture.load_texture(sys.path[0] + "/textures/tex_01.png")
        self.texture_floor = Texture.load_texture(sys.path[0] + "/textures/tex_metallic_floor_2.jpeg")
        self.texture_sphere = Texture.load_texture(sys.path[0] + "/textures/tex_sphere_6.png")
        self.texture_box = Texture.load_texture(sys.path[0] + "/textures/tex_metallic.jpeg")
        self.texture_mars = Texture.load_texture(sys.path[0] + "/textures/tex_mars.jpeg")
        self.texture_mercury = Texture.load_texture(sys.path[0] + "/textures/tex_mercury.jpeg")
        self.texture_jupiter = Texture.load_texture(sys.path[0] + "/textures/tex_jupiter.jpeg")
        self.texture_moon = Texture.load_texture(sys.path[0] + "/textures/tex_moon.jpeg")

    def update(self):
        self.time_elapsed = pygame.time.get_ticks() / 1000
        self.delta_time = self.clock.tick() / 1000
        self.angle += math.pi * self.delta_time
        self.angle_deg = self.angle * 57.2957795

        self.model_pos_bez= self.beizer_obj.get_current_pos(self.time_elapsed)

        # specific_time = 7.5
        # self.model_pos_lin = self.lin_motion.get_current_pos(specific_time)
        # self.model_pos_bez= self.bez_motion.get_current_pos(specific_time)

        # look up/down/left/right
        if self.UP_key_right:
            self.view_matrix.turn(-self.angle_turn)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_left:
            self.view_matrix.turn(self.angle_turn)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_up:
            self.view_matrix.pitch(-self.angle_turn)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_down:
            self.view_matrix.pitch(self.angle_turn)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # Walk forward/backwards/left/right
        walk_speed = self.delta_time * 6
        if self.UP_key_w:
            self.view_matrix.walk(0, 0, -walk_speed)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_s:
            self.view_matrix.walk(0, 0, walk_speed)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_a:
            self.view_matrix.walk(-walk_speed, 0, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())
        if self.UP_key_d:
            self.view_matrix.walk(walk_speed, 0, 0)
            self.shader.set_view_matrix(self.view_matrix.get_matrix())

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Lights
        self.shader.set_light_diffuse(1, 1, 1)
        self.shader.set_light_ambient(0.2, 0.2, 0.2)
        self.shader.set_light_specular(1, 1, 1)
        self.shader.set_global_ambient(1, 1, 1)
        self.shader.set_eye_location(self.view_matrix.eye)

        ######### Translated to middle of sphere #########
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.sphere_width / 2, self.sphere_width / 2, - self.sphere_width / 2)

        self.draw_floor()
        self.draw_mars()
        self.draw_mercury()
        self.draw_jupiter()
        self.draw_moon()
        self.draw_bez_moving_cube()
        self.draw_model_person()

        self.model_matrix.pop_matrix()
        ######### Translated to middle of sphere #########

        # Sky sphere
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_sphere)
        self.draw_sky_sphere()

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        pygame.display.flip()


    def draw_bez_moving_cube(self):
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.model_pos_bez.x, self.model_pos_bez.y, self.model_pos_bez.z)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_mat_diffuse(Base3DObjects.Color(1.0, 0.0, 0.0))
        self.shader.set_mat_shine(13)
        self.shader.set_mat_ambient(Base3DObjects.Color(0.1, 0.0, 0.0))
        self.cube.set_vertices(self.shader)
        self.cube.draw()
        self.model_matrix.pop_matrix()

    def draw_floor(self):
        floor_dim = 10
        floor_thickness = 0.2
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_floor)
        Texture.set_specular_tex(self.shader, self.texture_floor)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(y = - floor_thickness / 2)
        self.model_matrix.add_scale(floor_dim, floor_thickness, floor_dim)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.shader.set_mat_diffuse(Base3DObjects.Color(1.0, 1.0, 1.0))
        self.shader.set_mat_shine(13)
        self.shader.set_mat_ambient(Base3DObjects.Color(0.1, 0.1, 0.1))

        self.cube.set_vertices(self.shader)
        self.cube.draw()
        self.model_matrix.pop_matrix()

    def draw_sky_sphere(self):
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.sphere_width/2, self.sphere_width/2, -self.sphere_width/2)
        self.model_matrix.add_scale(self.sphere_width, self.sphere_width, self.sphere_width)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.shader.set_mat_ambient(Base3DObjects.Color(0.2, 0.2, 0.2))

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_model_person(self):
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 3)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.obj_model_person.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_mars(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_mars)
        Texture.set_specular_tex(self.shader, self.texture_mars)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = -5, y = 10)
        self.model_matrix.add_scale(1.5, 1.5, 1.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_mercury(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_mercury)
        Texture.set_specular_tex(self.shader, self.texture_mercury)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = -1, y = 10)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_jupiter(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_jupiter)
        Texture.set_specular_tex(self.shader, self.texture_jupiter)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 3, y = 10)
        self.model_matrix.add_scale(2, 2, 2)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_moon(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_moon)
        Texture.set_specular_tex(self.shader, self.texture_moon)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(y = 5)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def program_loop(self):
        exiting = False
        while not exiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        exiting = True
                    elif event.key == K_RIGHT:
                        self.UP_key_right = True
                    elif event.key == K_LEFT:
                        self.UP_key_left = True
                    elif event.key == K_UP:
                        self.UP_key_up = True
                    elif event.key == K_DOWN:
                        self.UP_key_down = True

                    elif event.key == K_w:
                        self.UP_key_w = True
                    elif event.key == K_s:
                        self.UP_key_s = True
                    elif event.key == K_a:
                        self.UP_key_a = True
                    elif event.key == K_d:
                        self.UP_key_d = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_RIGHT:
                        self.UP_key_right = False
                    elif event.key == K_LEFT:
                        self.UP_key_left = False
                    elif event.key == K_UP:
                        self.UP_key_up = False
                    elif event.key == K_DOWN:
                        self.UP_key_down = False

                    elif event.key == K_w:
                        self.UP_key_w = False
                    elif event.key == K_s:
                        self.UP_key_s = False
                    elif event.key == K_a:
                        self.UP_key_a = False
                    elif event.key == K_d:
                        self.UP_key_d = False

            self.update()
            self.display()

        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()