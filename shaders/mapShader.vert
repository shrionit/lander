#version 400

layout(location=0) in vec3 position;
layout(location=1) in vec2 iTexOffset;
layout(location=2) in mat4 transformationMatrix;

out vec2 oTexCoord;
out vec3 oWorldPos;
out vec3 oLightPos;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec2 tileSize;
//uniform vec3 lightPos = vec3(0, 0, 0);
void main(){
    vec2 texcoord = vec2(
        iTexOffset.x + position.x * tileSize.x,
        iTexOffset.y + position.y * tileSize.y
    );
    oTexCoord = texcoord;
    vec3 finalPos = vec3(position);
    mat4 pvmMatrix = projectionMatrix * viewMatrix * transformationMatrix;

    vec4 worldPos = pvmMatrix * vec4(finalPos, 1.0);

    //    oLightPos = (projectionMatrix * viewMatrix * vec4(lightPos, 1.0)).xyz;
    //    oWorldPos = worldPos.xyz;

    gl_Position = worldPos;
}