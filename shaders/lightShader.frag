#version 400

in vec2 oTexCoord;
uniform sampler2D frame;

struct Light{
    vec3 position;
    vec4 color;
};

uniform Light lights[500];

void main() {
    vec4 color = texture(frame, oTexCoord);
    vec4 finalColor = color;
    gl_FragColor = finalColor;
}
