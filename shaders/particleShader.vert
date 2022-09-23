#version 400

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoord;
layout(location=2) in vec3 offset;

out vec2 oTexCoord;
out vec3 oColor;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 transformationMatrix;

void main(){
    vec3 finalPos = vec3(position + offset);
    vec4 worldPos = projectionMatrix * viewMatrix * transformationMatrix * vec4(finalPos, 1.0);
    oTexCoord = texCoord;
    gl_Position = worldPos;
    oColor = vec3(offset);
}