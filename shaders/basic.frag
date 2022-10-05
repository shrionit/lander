#version 400

in vec2 oTexCoord;

uniform sampler2D basicTexture;
uniform float offsetX = 0;

void main(){
    vec2 texCoord = vec2(oTexCoord);
    texCoord.x += offsetX;
    vec4 color = texture(basicTexture, texCoord);
    gl_FragColor = color;
}