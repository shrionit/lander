#version 400

in vec2 oTexCoord;
//in vec3 oWorldPos;
//in vec3 oLightPos;
uniform sampler2D map;

void main(){
//    float lightFactor = 1 / distance(oLightPos, oWorldPos);
    vec4 color = texture(map, oTexCoord);
    gl_FragColor = color;
}