#version 400

in vec2 oTexCoord;

uniform sampler2D particleTexture;

void main(){
    vec4 color = texture(particleTexture, oTexCoord);
    gl_FragColor = color;
}