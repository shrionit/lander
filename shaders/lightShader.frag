#version 400

in vec2 oTexCoord;
in vec2 oPos;
in mat4 mvp;
uniform sampler2D frame;

struct Light{
    vec3 position;
    vec4 color;
};

uniform Light lights[500];


void main() {
    vec4 color = texture(frame, oTexCoord);
    float radius = 50;
    float falloff = 2;
    Light light = lights[0];
    vec3 lightPos = vec3(mvp * vec4(light.position, 1.0));
    float d = 1.0 / distance(lightPos, vec3(oPos, 0));
    vec4 finalColor = (color * d);
    gl_FragColor = finalColor;
}
