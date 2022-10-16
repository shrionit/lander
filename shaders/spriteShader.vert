#version 400
layout(location=0) in vec3 position;
layout(location=1) in vec2 currentTexCoord;
layout(location=2) in vec2 nextTexCoord;

out vec2 oCurrentTexCoord;
out vec2 oNextTexCoord;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 transformationMatrix;

void main() {
    oCurrentTexCoord = currentTexCoord;
    oNextTexCoord = nextTexCoord;
    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(position, 1.0);
}
