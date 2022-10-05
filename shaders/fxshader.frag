#version 400

in vec2 oTexCoord;
uniform sampler2D frame;

const float offset = 1.0 / 500.0;
vec2 offsets[9] = vec2[](
    vec2(-offset,  offset), // top-left
    vec2( 0.0f,    offset), // top-center
    vec2( offset,  offset), // top-right
    vec2(-offset,  0.0f),   // center-left
    vec2( 0.0f,    0.0f),   // center-center
    vec2( offset,  0.0f),   // center-right
    vec2(-offset, -offset), // bottom-left
    vec2( 0.0f,   -offset), // bottom-center
    vec2( offset, -offset)  // bottom-right
);
 uniform float kernel[9] = float[](
    0, 0, 0,
    0, 1, 0,
    0, 0, 0
 );

vec4 applyKernel(float[9] kern, sampler2D tex, vec2 texCoord){
    vec4 sampleTex[9];
    for(int i = 0; i < 9; i++) {
        sampleTex[i] = texture(tex, texCoord.st + offsets[i]);
    }
    vec4 col = vec4(0.0);
    for(int i = 0; i < 9; i++) {
        col.rgb += vec3(sampleTex[i]) * kern[i];
        col.a = sampleTex[i].a;
    }
    return col;
}

void main() {
    vec4 color = texture(frame, oTexCoord);
    vec4 fxColor = applyKernel(kernel, frame, oTexCoord);
    vec4 finalColor = fxColor;
    gl_FragColor = finalColor;
}
