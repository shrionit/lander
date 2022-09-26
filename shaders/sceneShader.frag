#version 400

in vec2 oTexCoords;

uniform sampler2D frame;

void main() {
    gl_FragColor = texture(frame, oTexCoords);
}
