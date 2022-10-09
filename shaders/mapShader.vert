#version 400

layout(location=0) in vec3 position;
layout(location=1) in vec2 iTexOffset;
layout(location=2) in mat4 transformationMatrix;

out vec2 oTexCoord;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec2 tileSize;

void main(){
    vec2 texcoord = vec2(
        iTexOffset.x + position.x * tileSize.x,
        iTexOffset.y + position.y * tileSize.y
    );
    oTexCoord = texcoord;
    vec3 finalPos = vec3(position);
    mat4 mvMatrix = viewMatrix * transformationMatrix;
    vec4 worldPos = projectionMatrix * mvMatrix * vec4(finalPos, 1.0);
    gl_Position = worldPos;
}