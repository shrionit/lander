#version 400

layout(location=0) in vec3 position;
layout(location=1) in vec3 color;
layout(location=2) in vec2 texCoord;
layout(location=3) in vec4 instanceModelMatrixColA;
layout(location=4) in vec4 instanceModelMatrixColB;
layout(location=5) in vec4 instanceModelMatrixColC;
layout(location=6) in vec4 instanceModelMatrixColD;

out vec3 oColor;
out vec2 oTexCoord;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main(){
    vec3 localPosition = position;
    vec4 worldPos = projectionMatrix * viewMatrix * modelMatrix * vec4(localPosition, 1.0);
    oColor = color;
    oTexCoord = texCoord;
    gl_Position = worldPos;
}