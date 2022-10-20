attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

// Matrices
uniform mat4 u_model_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

// light
uniform vec4 u_light_position;
uniform vec4 u_eye_position;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// UV coords sent into per-pixel use
	v_uv = a_uv;

	// local cordinates
	position = u_model_matrix * position;
	v_normal = normalize(u_model_matrix * normal);

	// global cordinates
	v_s = normalize(u_light_position - position);
	vec4 v = normalize(u_eye_position - position);
	v_h = normalize(v_s + v);

	// eye cordinates
	position = u_view_matrix * position;

	// clip cordinates
	position = u_projection_matrix * position;

	gl_Position = position;
}