from lib2to3.pytree import Base
import math
from multiprocessing import current_process
import sys
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *
import random

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

        self.sphere_width = 100

        self.projection_matrix = Matrices.ProjectionMatrix()
        self.projection_matrix.set_perspective(60, 1920/1080, 0.8, 150)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.view_matrix = Matrices.ViewMatrix()

        # set camera
        self.view_matrix.eye = Base3DObjects.Point(self.sphere_width/2, self.sphere_width/2 + 3, self.sphere_width/2 + 15)             #make 5 a variable dependent on the floor dim
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        # set light
        self.shader.set_light_position(Base3DObjects.Point(self.sphere_width/4, self.sphere_width/2, self.sphere_width/2))

        # General objects
        self.cube = Base3DObjects.Cube()
        self.opt_sphere = Base3DObjects.OptimizedSphere(24, 48)
        self.sphere = Base3DObjects.Sphere(20, 20)

        # Time
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.time_elapsed = 0

        # Motion
        # Rocket
        control_points = [Base3DObjects.Point(-30, -10, -60),
                          Base3DObjects.Point(-50, -10, -50),
                          Base3DObjects.Point(-50, -5, -40),
                          Base3DObjects.Point(0, 0, -30),
                          Base3DObjects.Point(50, 5, -10),
                          Base3DObjects.Point(10, 0, -15)]

        self.beizer_obj_rocket = Motion.BeizerObject(control_points, 5.0, 20.0, 0.001, 0.5)

        # camera
        control_points = [Base3DObjects.Point(0, 0, 10),
                          Base3DObjects.Point(-10, 20, 0),
                          Base3DObjects.Point(-40, 20, 0),
                          Base3DObjects.Point(0, 0, -20)]
        self.beizer_obj_camera = Motion.BeizerObject(control_points, 5.0, 20.0)

        # particles
        self.num_particles = 60
        self.linjear_motions_1, self.last_start_particle_time = self.generate_linjear_motions(self.num_particles, 0)
        self.linjear_motions_2 = []
        self.model_pos_bez = Base3DObjects.Point(0,0,0)

        # Other objects
        self.obj_model_person_idea = obj3DLoading.load_obj_file(sys.path[0] + "/models", "person_idea.obj")
        self.obj_model_person_sitting = obj3DLoading.load_obj_file(sys.path[0] + "/models", "person_sitting.obj")
        self.obj_model_spikeball = obj3DLoading.load_obj_file(sys.path[0] + "/models", "spikeball_3.obj")
        self.obj_model_negative_text = obj3DLoading.load_obj_file(sys.path[0] + "/models", "negative_text.obj")
        self.obj_model_positive_text = obj3DLoading.load_obj_file(sys.path[0] + "/models", "positive_text.obj")
        self.obj_model_rocket = obj3DLoading.load_obj_file(sys.path[0] + "/models", "rocket.obj")

        # Angles
        self.angle = 0
        self.angle_turn = 0.7
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
        # Planets
        self.texture_sun = Texture.load_texture(sys.path[0] + "/textures/tex_sun.jpeg")
        self.texture_mercury = Texture.load_texture(sys.path[0] + "/textures/tex_mercury.jpeg")
        self.texture_venus = Texture.load_texture(sys.path[0] + "/textures/tex_venus.jpeg")
        self.texture_earth = Texture.load_texture(sys.path[0] + "/textures/tex_earth.jpeg")
        self.texture_mars = Texture.load_texture(sys.path[0] + "/textures/tex_mars.jpeg")
        self.texture_jupiter = Texture.load_texture(sys.path[0] + "/textures/tex_jupiter.jpeg")
        self.texture_saturn = Texture.load_texture(sys.path[0] + "/textures/tex_saturn.jpeg")
        self.texture_neptune = Texture.load_texture(sys.path[0] + "/textures/tex_neptune.jpeg")
        self.texture_uranus = Texture.load_texture(sys.path[0] + "/textures/tex_uranus.jpeg")
        self.texture_moon = Texture.load_texture(sys.path[0] + "/textures/tex_moon.jpeg")

    def update(self):
        self.time_elapsed = pygame.time.get_ticks() / 1000
        self.delta_time = self.clock.tick() / 1000
        # self.angle += math.pi * self.delta_time
        self.angle = math.pi * self.time_elapsed / 10
        self.angle_deg = self.angle * 57.2957795

        if self.time_elapsed > self.last_start_particle_time:
            self.linjear_motions_2 = self.linjear_motions_1
            self.linjear_motions_1, self.last_start_particle_time = self.generate_linjear_motions(self.num_particles,
                                                                                                  self.time_elapsed)

        # Camera
        # new_pos = self.beizer_obj_camera.get_current_pos(self.time_elapsed)
        # self.view_matrix.eye = Base3DObjects.Point(self.sphere_width/2 + new_pos.x,
        #                                            self.sphere_width / 2 + new_pos.y,
        #                                            - self.sphere_width / 2 + new_pos.z)
        # self.shader.set_view_matrix(self.view_matrix.get_matrix())


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
        walk_speed = self.delta_time * 12
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
        self.model_matrix.add_translation(self.sphere_width / 2, self.sphere_width / 2, self.sphere_width / 2)

        self.draw_floor()
        self.draw_solar_system()

        self.draw_model_person_idea()
        self.draw_model_person_sitting()
        self.draw_model_negative_text()
        self.draw_model_positive_text()
        self.draw_lin_moving_particles()
        # self.draw_model_rocket()
        self.draw_bez_moving_rocket()

        self.model_matrix.pop_matrix()
        ######### Translated to middle of sphere #########

        # Sky sphere
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_sphere)
        self.draw_sky_sphere()

        glViewport(0, 0, 800, 600)
        self.model_matrix.load_identity()

        pygame.display.flip()

    def generate_linjear_motions(self, num, start_time):
        start_time = start_time
        end_time = start_time + 15
        rand = random.Random()
        linjear_motions = []

        for _ in range(num):
            rand_y = rand.uniform(-40, 40)
            rand_z = rand.uniform(40, -40)

            # while rand_y < 10 and rand_y > -10:
            #     rand_y = rand.uniform(-80, 80)

            # while rand_z < 10 and rand_z > -10:
            #     rand_z = rand.uniform(-80, 80)

            pos1 = Base3DObjects.Point(-100, rand_y, rand_z)
            pos2 = Base3DObjects.Point(100, rand_y, rand_z)
            motion = Motion.LinearMotion(pos1, pos2, start_time, end_time)

            linjear_motions.append(motion)
            start_time += 0.3
            end_time += 0.3

        return linjear_motions, start_time

    def draw_bez_moving_rocket(self):
        curr_pos = self.beizer_obj_rocket.get_current_pos(self.time_elapsed)
        curr_scale = self.beizer_obj_rocket.get_current_scale(self.time_elapsed)
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(curr_pos.x, curr_pos.y, curr_pos.z)
        self.model_matrix.add_scale(curr_scale, curr_scale, curr_scale)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_rocket.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_lin_moving_particles(self):
        self.shader.set_using_texture(0.0)
        for motion in self.linjear_motions_1:
            curr_pos = motion.get_current_pos(self.time_elapsed)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(curr_pos.x, curr_pos.y, curr_pos.z)
            self.model_matrix.add_scale(0.1, 0.1, 0.1)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.obj_model_spikeball.draw(self.shader)
            self.model_matrix.pop_matrix()

        for motion in self.linjear_motions_2:
            curr_pos = motion.get_current_pos(self.time_elapsed)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(curr_pos.x, curr_pos.y, curr_pos.z)
            self.model_matrix.add_scale(0.1, 0.1, 0.1)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.obj_model_spikeball.draw(self.shader)
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
        self.model_matrix.add_translation(self.sphere_width/2, self.sphere_width/2, self.sphere_width/2)
        self.model_matrix.add_scale(self.sphere_width, self.sphere_width, self.sphere_width)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.shader.set_mat_ambient(Base3DObjects.Color(0.2, 0.2, 0.2))

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_model_person_idea(self):
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 3)
        self.model_matrix.add_rotation(90, "y")
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.obj_model_person_idea.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_model_person_sitting(self):
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-2, 0, 4.4)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.obj_model_person_sitting.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_model_negative_text(self):
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-2, 2.5, 4.7)
        self.model_matrix.add_scale(0.3, 0.3, 0.3)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.obj_model_negative_text.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_model_positive_text(self):
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(3, 5, 0)
        self.model_matrix.add_scale(0.3, 0.3, 0.3)
        self.model_matrix.add_rotation(90, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.obj_model_positive_text.draw(self.shader)
        self.model_matrix.pop_matrix()

    def draw_model_rocket(self):
        self.shader.set_using_texture(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 20)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.obj_model_rocket.draw(self.shader)
        self.model_matrix.pop_matrix()


    # Planets
    def draw_solar_system(self):
        #sun
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-20, -5, -50)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_sun()

        #mercury
        self.model_matrix.add_rotation(self.angle_deg * 3, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_mercury()

        #venus
        self.model_matrix.add_rotation(- self.angle_deg / 2 , "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_venus()

        #earth
        self.model_matrix.add_rotation(- self.angle_deg / 2, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_earth()

        #mars
        self.model_matrix.add_rotation(- self.angle_deg, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_mars()

        #jupiter
        self.model_matrix.add_rotation(- self.angle_deg * 0.3, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_jupiter()

        #saturn
        self.model_matrix.add_rotation(- self.angle_deg * 0.3, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_saturn()

        #neptune
        self.model_matrix.add_rotation(self.angle_deg * 0.2, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_neptune()

        #uranus
        self.model_matrix.add_rotation(self.angle_deg * 0.2, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.draw_uranus()

        self.model_matrix.pop_matrix()

    def draw_mercury(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_mercury)
        Texture.set_specular_tex(self.shader, self.texture_mercury)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 5)
        self.model_matrix.add_scale(0.3, 0.3, 0.3)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_venus(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_venus)
        Texture.set_specular_tex(self.shader, self.texture_venus)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 7)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_earth(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_earth)
        Texture.set_specular_tex(self.shader, self.texture_earth)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 11)
        self.model_matrix.add_scale(0.7, 0.7, 0.7)
        self.model_matrix.add_rotation(self.angle_deg, "y")
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_mars(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_mars)
        Texture.set_specular_tex(self.shader, self.texture_mars)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 14)
        self.model_matrix.add_scale(0.5, 0.5, 0.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_jupiter(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_jupiter)
        Texture.set_specular_tex(self.shader, self.texture_jupiter)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 20)
        self.model_matrix.add_scale(2.5, 2.5, 2.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_saturn(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_saturn)
        Texture.set_specular_tex(self.shader, self.texture_saturn)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 26.5)
        self.model_matrix.add_scale(2, 2, 2)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_uranus(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_uranus)
        Texture.set_specular_tex(self.shader, self.texture_uranus)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 31.6)
        self.model_matrix.add_scale(0.9, 0.9, 0.9)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_neptune(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_neptune)
        Texture.set_specular_tex(self.shader, self.texture_neptune)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(x = 34.5)
        self.model_matrix.add_scale(0.9, 0.9, 0.9)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_sun(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_sun)
        Texture.set_specular_tex(self.shader, self.texture_sun)
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(4, 4, 4)
        self.shader.set_model_matrix(self.model_matrix.matrix)

        self.opt_sphere.set_vertices(self.shader)
        self.opt_sphere.draw()
        self.model_matrix.pop_matrix()

    def draw_moon(self):
        self.shader.set_using_texture(1.0)
        Texture.set_diffuse_tex(self.shader, self.texture_moon)
        Texture.set_specular_tex(self.shader, self.texture_moon)
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(0.3, 0.3, 0.3)
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