#version 400

in vec2 position;
in vec2 texCoord;

out mat4 mvp;
out vec2 oPos;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 transformationMatrix;

out vec2 oTexCoord;

void main() {
    mvp = projectionMatrix * viewMatrix * transformationMatrix;
    oPos = position.xy;
    gl_Position = vec4(position, 0.0, 1.0);
    oTexCoord = texCoord;
}
