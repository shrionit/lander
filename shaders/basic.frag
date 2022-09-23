#version 400

in vec2 oTexCoord;

uniform sampler2D basicTexture;

void main(){
    vec4 color = texture(basicTexture, oTexCoord);
    gl_FragColor = color;
}