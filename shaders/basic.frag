#version 400

in vec3 oColor;
in vec2 oTexCoord;

uniform float iTime;
uniform float xOffset;
uniform sampler2D dayTex;
uniform sampler2D nightTex;

void main(){
    vec3 color = vec3(0);
    vec2 texCoord = vec2(
        oTexCoord.x+xOffset,
        oTexCoord.y
    );
    vec3 dayColor = vec3(texture(dayTex, texCoord));
    vec3 nightColor = vec3(texture(nightTex, texCoord));
    color = dayColor*pow(sin(iTime * 0.1), 2) + nightColor*pow(cos(iTime*0.1), 2);
    gl_FragColor = vec4(color, 1.0);
}