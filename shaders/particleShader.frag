#version 400

in vec2 oTexCoord;
in vec3 oColor;

uniform sampler2D particleTexture;

void main(){
    vec4 color = texture(particleTexture, oTexCoord);
//    color += vec4(oColor, 1.0);
    gl_FragColor = color;
}