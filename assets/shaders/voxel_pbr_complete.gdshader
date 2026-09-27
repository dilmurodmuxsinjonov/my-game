// assets/shaders/voxel_pbr_complete.gdshader
// Voxel Lord: Feudal Realm - Production 6-Channel PBR Triplanar Shader
// Milestone 4 / R4: Photorealistic PBR Surfaces & Dynamic Atmosphere
//
// Features:
// 1. Full 6-channel PBR Triplanar Mapping:
//    - Albedo, Normal, Roughness, Metallic, Ambient Occlusion, Height/Displacement
// 2. Parallax Occlusion Mapping (POM) raymarched relief for deep crevices
// 3. Subsurface Scattering (SSS) organic transmittance profiles:
//    - Human Skin (capillary red), Plant Leaves/Foliage (emerald chlorophyll),
//      Candle Wax/Tallow (warm amber), Raw Meat (dense myoglobin red), and Custom
// 4. Dynamic Rain Surface Wetness:
//    - Porous albedo darkening, microfacet smoothing (roughness drop), specular sheen,
//      and procedural animated puddle ripples on horizontal surfaces
// 5. Procedural Snow Accumulation:
//    - Directional accumulation on horizontal voxel faces gated by normal slope (world_normal.y > 0.6)
//    - Thermal thaw response (ambient_temp > 0.0°C and proximity heat sources)

shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

// =========================================================================
// 1. 6-Channel PBR Texture Uniforms
// =========================================================================
uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D texture_normal : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D texture_roughness : hint_roughness_gray, filter_linear_mipmap, repeat_enable;
uniform sampler2D texture_metallic : hint_default_black, filter_linear_mipmap, repeat_enable;
uniform sampler2D texture_ao : hint_default_white, filter_linear_mipmap, repeat_enable;
uniform sampler2D texture_height : hint_default_black, filter_linear_mipmap, repeat_enable;

// =========================================================================
// 2. Triplanar Projection & Parallax Occlusion Mapping (POM) Uniforms
// =========================================================================
uniform float uv_scale : hint_range(0.01, 2.0) = 0.5;
uniform float triplanar_sharpness : hint_range(1.0, 16.0) = 6.0;

uniform float height_scale : hint_range(0.0, 0.2) = 0.05;
uniform int pom_min_layers : hint_range(4, 16) = 8;
uniform int pom_max_layers : hint_range(8, 64) = 32;
uniform bool pom_invert_depth = false;

// =========================================================================
// 3. Subsurface Scattering (SSS) Organic Transmittance Profiles
// =========================================================================
// Profile Selection:
// 0 = Custom (uses individual uniforms)
// 1 = Human / Citizen Skin (capillary blood absorption)
// 2 = Plant Leaves / Foliage (chlorophyll transmission)
// 3 = Candle Wax / Tallow (paraffin internal diffusion)
// 4 = Raw Butchery Meat (dense myoglobin scattering)
uniform int sss_profile : hint_range(0, 4) = 0;
uniform float sss_strength : hint_range(0.0, 1.0) = 0.0;
uniform vec4 sss_transmittance_color : source_color = vec4(0.85, 0.25, 0.12, 1.0);
uniform float sss_transmittance_depth : hint_range(0.01, 2.0) = 0.15;
uniform float sss_backlight_intensity : hint_range(0.0, 2.0) = 0.0;

// =========================================================================
// 4. Dynamic Weather: Rain Wetness & Procedural Ripples
// =========================================================================
uniform float rain_wetness : hint_range(0.0, 1.0) = 0.0;
uniform float puddle_ripple_speed : hint_range(0.1, 10.0) = 2.5;
uniform float puddle_ripple_scale : hint_range(0.5, 20.0) = 3.0;

// =========================================================================
// 5. Dynamic Weather: Procedural Snow Accumulation & Thermal Thaw
// =========================================================================
uniform float snow_accumulation : hint_range(0.0, 1.0) = 0.0;
uniform float snow_depth : hint_range(0.0, 1.0) = 0.0; // Alias for snow_accumulation
uniform vec3 snow_color : source_color = vec3(0.93, 0.96, 0.99);
uniform float snow_slope_threshold : hint_range(0.0, 1.0) = 0.60;
uniform float ambient_temp : float = -5.0; // Celsius; > 0°C triggers thaw
uniform float thermal_thaw : hint_range(0.0, 1.0) = 0.0; // Proximity to hearth / furnace

// =========================================================================
// Varyings
// =========================================================================
varying vec3 v_world_pos;
varying vec3 v_world_normal;

void vertex() {
	v_world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	v_world_normal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

// Parallax Occlusion Mapping raymarched depth offset
vec2 pom_offset(sampler2D h_tex, vec2 uv, vec3 view_dir_tangent) {
	if (height_scale <= 0.0001) {
		return uv;
	}
	float vz = max(abs(view_dir_tangent.z), 0.001);
	float num_layers = mix(float(pom_max_layers), float(pom_min_layers), vz);
	float layer_depth = 1.0 / num_layers;
	float current_layer_depth = 0.0;
	vec2 p = (view_dir_tangent.xy / vz) * height_scale;
	vec2 delta_uv = p / num_layers;

	vec2 current_uv = uv;
	float raw_h = texture(h_tex, current_uv).r;
	float current_depth_value = pom_invert_depth ? raw_h : (1.0 - raw_h);

	for (int i = 0; i < pom_max_layers; i++) {
		if (current_layer_depth >= current_depth_value) {
			break;
		}
		current_uv -= delta_uv;
		raw_h = texture(h_tex, current_uv).r;
		current_depth_value = pom_invert_depth ? raw_h : (1.0 - raw_h);
		current_layer_depth += layer_depth;
	}

	// Parallax Occlusion interpolation between steps
	vec2 prev_uv = current_uv + delta_uv;
	float after_depth = current_depth_value - current_layer_depth;
	float prev_h = texture(h_tex, prev_uv).r;
	float before_depth = (pom_invert_depth ? prev_h : (1.0 - prev_h)) - current_layer_depth + layer_depth;
	float denom = after_depth - before_depth;
	float weight = (abs(denom) > 0.0001) ? clamp(after_depth / denom, 0.0, 1.0) : 0.0;
	return mix(prev_uv, current_uv, weight);
}

void fragment() {
	// ---------------------------------------------------------------------
	// 1. Calculate Triplanar Blending Weights
	// ---------------------------------------------------------------------
	vec3 blend_weights = pow(abs(v_world_normal), vec3(triplanar_sharpness));
	blend_weights /= max(blend_weights.x + blend_weights.y + blend_weights.z, 0.00001);

	// ---------------------------------------------------------------------
	// 2. Base World-Space UVs & Parallax Occlusion Mapping
	// ---------------------------------------------------------------------
	vec2 uv_x = v_world_pos.zy * uv_scale;
	vec2 uv_y = v_world_pos.xz * uv_scale;
	vec2 uv_z = v_world_pos.xy * uv_scale;

	vec3 cam_pos = INV_VIEW_MATRIX[3].xyz;
	vec3 view_dir_world = normalize(cam_pos - v_world_pos);

	// Projected view vectors in tangent space for planes X, Y, Z
	vec3 view_tangent_x = vec3(view_dir_world.z * sign(v_world_normal.x), view_dir_world.y, abs(view_dir_world.x));
	vec3 view_tangent_y = vec3(view_dir_world.x, view_dir_world.z * sign(v_world_normal.y), abs(view_dir_world.y));
	vec3 view_tangent_z = vec3(view_dir_world.x, view_dir_world.y, abs(view_dir_world.z));

	if (height_scale > 0.0001) {
		uv_x = pom_offset(texture_height, uv_x, view_tangent_x);
		uv_y = pom_offset(texture_height, uv_y, view_tangent_y);
		uv_z = pom_offset(texture_height, uv_z, view_tangent_z);
	}

	// ---------------------------------------------------------------------
	// 3. Sample 6 PBR Channels
	// ---------------------------------------------------------------------
	// Albedo
	vec3 col_x = texture(texture_albedo, uv_x).rgb;
	vec3 col_y = texture(texture_albedo, uv_y).rgb;
	vec3 col_z = texture(texture_albedo, uv_z).rgb;
	vec3 base_color = col_x * blend_weights.x + col_y * blend_weights.y + col_z * blend_weights.z;

	// Normal
	vec3 norm_x = texture(texture_normal, uv_x).rgb * 2.0 - 1.0;
	vec3 norm_y = texture(texture_normal, uv_y).rgb * 2.0 - 1.0;
	vec3 norm_z = texture(texture_normal, uv_z).rgb * 2.0 - 1.0;
	vec3 blended_normal = normalize(norm_x * blend_weights.x + norm_y * blend_weights.y + norm_z * blend_weights.z);

	// Roughness
	float rough_x = texture(texture_roughness, uv_x).r;
	float rough_y = texture(texture_roughness, uv_y).r;
	float rough_z = texture(texture_roughness, uv_z).r;
	float base_roughness = rough_x * blend_weights.x + rough_y * blend_weights.y + rough_z * blend_weights.z;

	// Metallic
	float metal_x = texture(texture_metallic, uv_x).r;
	float metal_y = texture(texture_metallic, uv_y).r;
	float metal_z = texture(texture_metallic, uv_z).r;
	float base_metallic = metal_x * blend_weights.x + metal_y * blend_weights.y + metal_z * blend_weights.z;

	// Ambient Occlusion
	float ao_x = texture(texture_ao, uv_x).r;
	float ao_y = texture(texture_ao, uv_y).r;
	float ao_z = texture(texture_ao, uv_z).r;
	float base_ao = ao_x * blend_weights.x + ao_y * blend_weights.y + ao_z * blend_weights.z;

	// ---------------------------------------------------------------------
	// 4. Dynamic Rain Wetness & Procedural Puddle Ripples
	// ---------------------------------------------------------------------
	if (rain_wetness > 0.01) {
		float horizontal_puddle_mask = clamp((v_world_normal.y - 0.40) / 0.60, 0.0, 1.0);
		float effective_wetness = rain_wetness * mix(0.70, 1.0, horizontal_puddle_mask);

		// Porous surface darkening via internal light absorption
		base_color = mix(base_color, base_color * 0.70, effective_wetness);
		// Water film smoothens microfacets (drastic roughness reduction)
		base_roughness = mix(base_roughness, 0.04, effective_wetness * 0.90);

		// Procedural animated rain puddle ripples on horizontal surfaces (normal.y > 0.60)
		float puddle_ripple_mask = clamp((v_world_normal.y - 0.60) / 0.40, 0.0, 1.0) * rain_wetness;
		if (puddle_ripple_mask > 0.01) {
			vec2 ripple_uv = v_world_pos.xz * puddle_ripple_scale;
			float ripple_time = TIME * puddle_ripple_speed;
			vec2 ripple_offset = vec2(0.0);

			for (int i = 0; i < 3; i++) {
				float fi = float(i);
				vec2 grid_uv = ripple_uv + vec2(fi * 1.618, fi * 2.718);
				vec2 cell = floor(grid_uv);
				vec2 frac_uv = fract(grid_uv) - 0.5;
				float dist = length(frac_uv);
				float cell_hash = fract(sin(dot(cell, vec2(12.9898, 78.233))) * 43758.5453);
				float phase = fract(ripple_time * 0.75 + cell_hash);
				float ring_radius = phase * 0.65;
				float ring_dist = abs(dist - ring_radius);
				float ring_amp = (1.0 - phase) * exp(-ring_dist * ring_dist * 180.0);
				vec2 ring_dir = (dist > 0.001) ? (frac_uv / dist) : vec2(0.0);
				ripple_offset += ring_dir * ring_amp * sin(ring_dist * 45.0 - phase * 18.0);
			}

			vec3 ripple_perturbation = vec3(ripple_offset.x, 0.0, ripple_offset.y) * 0.40 * puddle_ripple_mask;
			blended_normal = normalize(blended_normal + ripple_perturbation);
		}
	}

	// ---------------------------------------------------------------------
	// 5. Procedural Snow Accumulation with Slope Gate & Thermal Thaw
	// ---------------------------------------------------------------------
	float total_snow_input = max(snow_accumulation, snow_depth);
	if (total_snow_input > 0.001) {
		// Normal slope gate: horizontal voxel faces (world_normal.y > 0.60)
		float slope_factor = clamp((v_world_normal.y - snow_slope_threshold) / (1.0 - snow_slope_threshold), 0.0, 1.0);

		// Thermal thaw: melting above 0°C or near active heat sources
		float temp_thaw = (ambient_temp > 0.0) ? clamp(ambient_temp / 10.0, 0.0, 1.0) : 0.0;
		float effective_thaw = clamp(thermal_thaw + temp_thaw, 0.0, 1.0);
		float net_snow = total_snow_input * (1.0 - effective_thaw);
		float snow_coverage = clamp(net_snow * slope_factor * 1.5, 0.0, 1.0);

		if (snow_coverage > 0.001) {
			base_color = mix(base_color, snow_color, snow_coverage);
			base_roughness = mix(base_roughness, 0.88, snow_coverage);
			base_metallic = mix(base_metallic, 0.0, snow_coverage);
			base_ao = mix(base_ao, 1.0, snow_coverage * 0.50);
			blended_normal = normalize(mix(blended_normal, vec3(0.0, 1.0, 0.0), snow_coverage * 0.70));
		}
	}

	// ---------------------------------------------------------------------
	// 6. Subsurface Scattering (SSS) Organic Transmittance Profiles
	// ---------------------------------------------------------------------
	float final_sss_strength = sss_strength;
	vec4 final_sss_color = sss_transmittance_color;
	float final_sss_depth = sss_transmittance_depth;
	float final_backlight = sss_backlight_intensity;

	if (sss_profile == 1) {
		// Human / Citizen Skin: subcutaneous capillary blood absorption
		final_sss_strength = 0.45;
		final_sss_color = vec4(0.85, 0.25, 0.12, 1.0);
		final_sss_depth = 0.15;
		final_backlight = 0.20;
	} else if (sss_profile == 2) {
		// Plant Leaves / Foliage: vibrant chlorophyll transmission
		final_sss_strength = 0.70;
		final_sss_color = vec4(0.35, 0.75, 0.08, 1.0);
		final_sss_depth = 0.05;
		final_backlight = 1.25;
	} else if (sss_profile == 3) {
		// Candle Wax / Tallow: soft paraffin internal amber diffusion
		final_sss_strength = 0.80;
		final_sss_color = vec4(0.95, 0.82, 0.55, 1.0);
		final_sss_depth = 0.25;
		final_backlight = 0.50;
	} else if (sss_profile == 4) {
		// Raw Butchery Meat: dense myoglobin deep red scattering
		final_sss_strength = 0.30;
		final_sss_color = vec4(0.80, 0.15, 0.10, 1.0);
		final_sss_depth = 0.08;
		final_backlight = 0.10;
	}

	if (final_sss_strength > 0.01) {
		SSS_STRENGTH = final_sss_strength;
		SSS_TRANSMITTANCE_COLOR = final_sss_color;
		SSS_TRANSMITTANCE_DEPTH = final_sss_depth;
		if (final_backlight > 0.01) {
			BACKLIGHT = final_sss_color.rgb * final_backlight;
		}
	}

	// ---------------------------------------------------------------------
	// 7. Output to PBR Buffers
	// ---------------------------------------------------------------------
	ALBEDO = base_color;
	NORMAL_MAP = blended_normal * 0.5 + 0.5;
	NORMAL_MAP_DEPTH = 1.0;
	ROUGHNESS = base_roughness;
	METALLIC = base_metallic;
	AO = base_ao;
	SPECULAR = mix(0.50, 0.90, rain_wetness);
}
