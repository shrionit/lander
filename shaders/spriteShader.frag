#version 400
in vec2 TexCoords;
uniform sampler2D image;
uniform vec2 texOffset = vec2(0.0);
void main() {
    vec2 texCoord = texOffset + TexCoords;
    gl_FragColor = texture(image, texCoord);
}