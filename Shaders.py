
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        # Matrices
        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")

        # Lights
        self.lightPosLoc = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDifLoc = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.lightAmbLoc = glGetUniformLocation(self.renderingProgramID, "u_light_ambient")

        self.matDifLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.matSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.matShineLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")
        self.matAmbLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_ambient")

        self.globalAmbLoc = glGetUniformLocation(self.renderingProgramID, "u_global_ambient")
        self.matEmiLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_emission")
        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        self.texDiffLoc = glGetUniformLocation(self.renderingProgramID, "u_tex01")
        self.texSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_tex02")
        self.usingTexLoc = glGetUniformLocation(self.renderingProgramID, "u_using_texture")


    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    # Matrices
    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    # Position and normal
    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    def set_attribute_buffer(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

    # def set_attribute_buffer(self, vertex_buffer_id):
    #     glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
    #     glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, None)
    #     glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, None)

    # Lights
    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_diffuse(self, r, g, b):
        glUniform4f(self.lightDifLoc, r, g, b, 1.0)

    def set_light_ambient(self, r, g, b):
        glUniform4f(self.lightAmbLoc, r, g, b, 1.0)

    def set_light_specular(self, r, g, b):
        glUniform4f(self.lightSpecLoc, r, g, b, 1.0)


    def set_mat_diffuse(self, color: Color):
        glUniform4f(self.matDifLoc, color.r, color.g, color.b, 1.0)

    def set_mat_specular(self, color: Color):
        glUniform4f(self.matSpecLoc, color.r, color.g, color.b, 1.0)

    def set_mat_shine(self, s: float):
        glUniform1f(self.matShineLoc, s)

    def set_mat_ambient(self, color: Color):
        glUniform4f(self.matAmbLoc, color.r, color.g, color.b , 1.0)

    def set_mat_emission(self, r, g, b):
        glUniform4f(self.matEmiLoc, r, g, b, 1.0)


    def set_global_ambient(self, r, g, b):
        glUniform4f(self.globalAmbLoc, r, g, b, 1.0)

    def set_eye_location(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    # texture
    def set_texture_diffuse(self, num):
        glUniform1i(self.texDiffLoc, num)

    def set_texture_specular(self, num):
        glUniform1i(self.texSpecLoc, num)

    def set_using_texture(self, num: float):
        glUniform1f(self.usingTexLoc, num)

