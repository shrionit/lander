#version 400

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoord;

out vec2 oTexCoord;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 transformationMatrix;

void main(){
    vec4 worldPos = projectionMatrix * viewMatrix * transformationMatrix * vec4(position, 1.0);
    oTexCoord = texCoord;
    gl_Position = worldPos;
}