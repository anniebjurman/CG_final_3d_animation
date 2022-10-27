import pygame
from OpenGL.GL import *


def load_texture(path_str):
    surface = pygame.image.load(path_str)
    tex_string = pygame.image.tostring(surface, "RGBA", 1)
    width = surface.get_width()
    height = surface.get_height()
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)

    return tex_id

def set_diffuse_tex(shader, tex_id):
        glActiveTexture(GL_TEXTURE0)                            # set active texture (0)
        glBindTexture(GL_TEXTURE_2D, tex_id)                    # bind texture to active texture
        shader.set_texture_diffuse(0)                           # set diffuse shader to 0

def set_specular_tex(shader, tex_id):
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        shader.set_texture_specular(1)