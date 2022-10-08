#version 400

in vec2 oTexCoord;

uniform sampler2D map;

void main(){
    vec4 color = texture(map, oTexCoord);
    gl_FragColor = color;
}