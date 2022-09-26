#version 400

layout(location=0) in vec3 position;
layout(location=1) in vec2 texCoord;
layout(location=2) in mat4 transformationMatrix;

out vec2 oTexCoord;
out vec3 oColor;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main(){
    vec3 finalPos = vec3(position);
    mat4 mvMatrix = viewMatrix * transformationMatrix;
    mvMatrix[0].xyz = vec3(transformationMatrix[0].x,0,0);
    mvMatrix[1].xyz = vec3(0,transformationMatrix[1].y,0);
    mvMatrix[2].xyz = vec3(0,0,transformationMatrix[2].z);
    vec4 worldPos = projectionMatrix * mvMatrix * vec4(finalPos, 1.0);
    oTexCoord = texCoord;
    gl_Position = worldPos;
}