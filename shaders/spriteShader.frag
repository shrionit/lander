#version 400
in vec2 oCurrentTexCoord;
in vec2 oNextTexCoord;

uniform sampler2D image;
uniform float blendFactor;

void main() {
    vec4 colorA = texture(image, oCurrentTexCoord);
    vec4 colorB = texture(image, oNextTexCoord);
    vec4 color = mix(colorA, colorB, blendFactor);
    gl_FragColor = colorA;
}