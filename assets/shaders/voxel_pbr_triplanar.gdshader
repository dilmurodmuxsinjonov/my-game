// assets/shaders/voxel_pbr_triplanar.gdshader
// Voxel Lord: Feudal Realm - Milestone 31: Realistic PBR Triplanar Voxel Shader
// Provides seamless world-space triplanar projection, tangent normal mapping,
// dynamic rain puddle wetness, and seasonal winter snow accumulation.

shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D texture_normal : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D texture_roughness : hint_roughness_gray, filter_linear_mipmap, repeat_enable;

uniform float uv_scale : hint_range(0.01, 2.0) = 0.5;
uniform float triplanar_sharpness : hint_range(1.0, 16.0) = 4.0;
uniform float rain_wetness : hint_range(0.0, 1.0) = 0.0;
uniform float snow_accumulation : hint_range(0.0, 1.0) = 0.0;
uniform vec3 snow_color : source_color = vec3(0.92, 0.95, 0.98);

varying vec3 v_world_pos;
varying vec3 v_world_normal;

void vertex() {
	v_world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	v_world_normal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

void fragment() {
	// 1. Calculate triplanar blend weights
	vec3 blend_weights = pow(abs(v_world_normal), vec3(triplanar_sharpness));
	blend_weights /= (blend_weights.x + blend_weights.y + blend_weights.z);

	// 2. Sample UVs projected on XYZ planes
	vec2 uv_x = v_world_pos.zy * uv_scale;
	vec2 uv_y = v_world_pos.xz * uv_scale;
	vec2 uv_z = v_world_pos.xy * uv_scale;

	// 3. Triplanar Albedo Blending
	vec3 col_x = texture(texture_albedo, uv_x).rgb;
	vec3 col_y = texture(texture_albedo, uv_y).rgb;
	vec3 col_z = texture(texture_albedo, uv_z).rgb;
	vec3 base_color = col_x * blend_weights.x + col_y * blend_weights.y + col_z * blend_weights.z;

	// 4. Triplanar Normal Blending
	vec3 norm_x = texture(texture_normal, uv_x).rgb * 2.0 - 1.0;
	vec3 norm_y = texture(texture_normal, uv_y).rgb * 2.0 - 1.0;
	vec3 norm_z = texture(texture_normal, uv_z).rgb * 2.0 - 1.0;
	vec3 blended_normal = normalize(norm_x * blend_weights.x + norm_y * blend_weights.y + norm_z * blend_weights.z);

	// 5. Triplanar Roughness Blending
	float rough_x = texture(texture_roughness, uv_x).r;
	float rough_y = texture(texture_roughness, uv_y).r;
	float rough_z = texture(texture_roughness, uv_z).r;
	float base_roughness = rough_x * blend_weights.x + rough_y * blend_weights.y + rough_z * blend_weights.z;

	// 6. Dynamic Rain Wetness (darkens albedo, increases specular shine, lowers roughness)
	if (rain_wetness > 0.01) {
		base_color = mix(base_color, base_color * 0.72, rain_wetness);
		base_roughness = mix(base_roughness, 0.08, rain_wetness * 0.85);
	}

	// 7. Winter Snow Accumulation on upward-facing normal surfaces
	float upward_factor = clamp(v_world_normal.y * 1.5, 0.0, 1.0);
	float snow_factor = clamp(snow_accumulation * upward_factor * 1.4, 0.0, 1.0);
	if (snow_factor > 0.01) {
		base_color = mix(base_color, snow_color, snow_factor);
		base_roughness = mix(base_roughness, 0.85, snow_factor);
	}

	ALBEDO = base_color;
	NORMAL_MAP = blended_normal * 0.5 + 0.5;
	NORMAL_MAP_DEPTH = 1.0;
	ROUGHNESS = base_roughness;
	SPECULAR = mix(0.5, 0.85, rain_wetness);
}
