# This extra import:

from OpenGL.GLU import*


# This extra operation for the class Shader3D

    def set_attribute_buffers(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))


# and changed versions of setting the material, just to use the Color class:

    # def set_material_diffuse(self, red, green, blue):
    #     glUniform4f(self.materialDiffuseLoc, red, green, blue, 1.0)

    def set_material_diffuse(self, color):
        glUniform4f(self.materialDiffuseLoc, color.r, color.g, color.b, 1.0)

    # def set_material_specular(self, red, green, blue):
    #     glUniform4f(self.materialSpecularLoc, red, green, blue, 1.0)

    def set_material_specular(self, color):
        glUniform4f(self.materialSpecularLoc, color.r, color.g, color.b, 1.0)

    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)
