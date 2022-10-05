#version 400
layout (location = 0) in vec4 position;

out vec2 TexCoords;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 transformationMatrix;

void main() {
    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(position.xy, 0.0, 1.0);
    TexCoords = position.zw;
}
