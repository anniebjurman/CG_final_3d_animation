uniform vec4 u_global_ambient;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;
uniform vec4 u_light_ambient;

uniform vec4 u_mat_diffuse; //light that scatters
uniform vec4 u_mat_specular; //light that reflects
uniform float u_mat_shininess; //shininess of light reflection
uniform vec4 u_mat_ambient; //light that fills the environment
uniform vec4 u_mat_emission; //self-illumination of material

uniform sampler2D u_tex01;
uniform sampler2D u_tex02;

uniform float u_using_texture;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

void main(void)
{
    vec4 mat_diffuse = u_mat_diffuse;
    vec4 mat_ambient = u_mat_ambient;
    vec4 mat_specular = u_mat_specular;

    if (u_using_texture == 1.0) {
        mat_diffuse *= texture2D(u_tex01, v_uv);
        mat_ambient *= texture2D(u_tex01, v_uv);
        mat_specular *= texture2D(u_tex02, v_uv);
    }

    float lambert = max(dot(v_normal, v_s), 0.0);
    float phong = max(dot(v_normal, v_h), 0.0);

    vec4 light_calculated_color = u_light_diffuse * mat_diffuse * lambert + // Diffuse color
                             u_light_specular * mat_specular * pow(phong, u_mat_shininess) + // Specular color
                             u_light_ambient * u_mat_ambient; //Ambient color

    gl_FragColor = u_global_ambient * mat_ambient +
                   light_calculated_color +
                   u_mat_emission;
}