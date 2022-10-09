#version 400
in vec2 oTexCoord;

uniform sampler2D image;

void main() {
    gl_FragColor = texture(image, oTexCoord);
}