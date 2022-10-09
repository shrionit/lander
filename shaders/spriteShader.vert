#version 400
layout(location=0) in vec3 position;
layout(location=1) in vec2 iTexCoord;

out vec2 oTexCoord;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 transformationMatrix;

void main() {
    oTexCoord = iTexCoord;
    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(position, 1.0);
}
