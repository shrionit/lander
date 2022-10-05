#version 400

in vec2 position;
in vec2 texCoord;

out vec2 oTexCoord;

void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    oTexCoord = texCoord;
}
