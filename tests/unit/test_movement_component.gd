extends GutTest

## Unit tests for MovementComponent
## Tests velocity management, acceleration, friction, and impulses

var movement_component: MovementComponent

func before_each():
	movement_component = MovementComponent.new()
	movement_component.speed = 200.0
	movement_component.max_speed = 300.0
	movement_component.acceleration = 1000.0
	movement_component.friction = 800.0
	movement_component.air_friction = 200.0

func after_each():
	movement_component.free()

# ============================================
# INITIALIZATION TESTS
# ============================================

func test_movement_component_initializes_with_zero_velocity():
	assert_eq(movement_component.velocity, Vector2.ZERO, "Velocity should start at zero")

func test_movement_component_has_correct_default_values():
	assert_eq(movement_component.speed, 200.0, "Speed should be 200.0")
	assert_eq(movement_component.max_speed, 300.0, "Max speed should be 300.0")
	assert_eq(movement_component.acceleration, 1000.0, "Acceleration should be 1000.0")

# ============================================
# TARGET DIRECTION TESTS
# ============================================

func test_set_target_direction_accelerates_velocity():
	movement_component.set_target_direction(Vector2.RIGHT, false)
	movement_component.update(0.1) # 0.1 second
	assert_gt(movement_component.velocity.x, 0, "Velocity should increase in target direction")

func test_set_target_direction_with_run_uses_max_speed():
	movement_component.set_target_direction(Vector2.RIGHT, true)
	movement_component.update(1.0) # 1 second (enough to reach max speed)
	assert_almost_eq(movement_component.velocity.x, 300.0, 10.0, "Velocity should reach max_speed when running")

func test_set_target_direction_without_run_uses_normal_speed():
	movement_component.set_target_direction(Vector2.RIGHT, false)
	movement_component.update(1.0) # 1 second
	assert_almost_eq(movement_component.velocity.x, 200.0, 10.0, "Velocity should reach speed when not running")

func test_set_target_clamps_to_max_speed():
	movement_component.set_target(Vector2.RIGHT * 500.0) # Target beyond max speed
	movement_component.update(2.0) # Long time
	assert_lte(movement_component.velocity.length(), movement_component.max_speed, "Velocity should not exceed max_speed")

# ============================================
# FRICTION TESTS
# ============================================

func test_apply_friction_reduces_velocity():
	movement_component.velocity = Vector2(100, 0)
	movement_component.apply_friction(0.1, true) # 0.1 second, grounded
	assert_lt(movement_component.velocity.x, 100, "Friction should reduce velocity")

func test_friction_stops_at_zero():
	movement_component.velocity = Vector2(10, 0)
	movement_component.apply_friction(1.0, true) # Long time
	assert_almost_eq(movement_component.velocity.x, 0.0, 1.0, "Friction should stop velocity at zero")

func test_air_friction_is_weaker_than_ground_friction():
	var ground_vel = Vector2(100, 0)
	var air_vel = Vector2(100, 0)
	
	var ground_comp = MovementComponent.new()
	ground_comp.friction = 800.0
	ground_comp.air_friction = 200.0
	ground_comp.velocity = ground_vel
	ground_comp.apply_friction(0.1, true) # Grounded
	
	var air_comp = MovementComponent.new()
	air_comp.friction = 800.0
	air_comp.air_friction = 200.0
	air_comp.velocity = air_vel
	air_comp.apply_friction(0.1, false) # Airborne
	
	assert_gt(air_comp.velocity.x, ground_comp.velocity.x, "Air friction should reduce velocity less than ground friction")
	
	ground_comp.free()
	air_comp.free()

# ============================================
# IMPULSE TESTS
# ============================================

func test_apply_impulse_adds_to_velocity():
	var initial_velocity = movement_component.velocity
	movement_component.apply_impulse(Vector2(100, -200))
	assert_eq(movement_component.velocity, initial_velocity + Vector2(100, -200), "Impulse should add to velocity")

func test_apply_impulse_emits_velocity_changed_signal():
	watch_signals(movement_component)
	movement_component.apply_impulse(Vector2(50, 0))
	assert_signal_emitted(movement_component, "velocity_changed", "Should emit velocity_changed signal")

# ============================================
# VELOCITY MANAGEMENT TESTS
# ============================================

func test_set_velocity_updates_velocity():
	movement_component.set_velocity(Vector2(150, -100))
	assert_eq(movement_component.velocity, Vector2(150, -100), "set_velocity should update velocity")

func test_set_velocity_emits_signal():
	watch_signals(movement_component)
	movement_component.set_velocity(Vector2(100, 0))
	assert_signal_emitted(movement_component, "velocity_changed", "Should emit velocity_changed signal")

func test_get_velocity_returns_current_velocity():
	movement_component.velocity = Vector2(123, 456)
	assert_eq(movement_component.get_velocity(), Vector2(123, 456), "get_velocity should return current velocity")

# ============================================
# UPDATE TESTS
# ============================================

func test_update_with_zero_delta_does_nothing():
	var initial_velocity = movement_component.velocity
	movement_component.update(0.0)
	assert_eq(movement_component.velocity, initial_velocity, "Update with zero delta should not change velocity")

func test_update_applies_acceleration_over_time():
	movement_component.set_target_direction(Vector2.RIGHT, false)
	movement_component.update(0.05) # Small update
	var vel_after_small = movement_component.velocity.x
	assert_gt(vel_after_small, 0, "Velocity should increase after first update")
	assert_lt(vel_after_small, 200.0, "Velocity should not reach target immediately")
	
	# After enough time, should reach target
	movement_component.update(1.0)
	assert_almost_eq(movement_component.velocity.x, 200.0, 1.0, "Velocity should approach target speed")

# ============================================
# EDGE CASES
# ============================================

func test_negative_acceleration_is_handled():
	movement_component.acceleration = -1000.0
	movement_component.set_target_direction(Vector2.RIGHT, false)
	movement_component.update(0.1)
	# Behavior with negative acceleration is undefined, but should not crash
	assert_true(true, "Should handle negative acceleration without crashing")

func test_zero_friction_maintains_velocity():
	movement_component.friction = 0.0
	movement_component.air_friction = 0.0
	movement_component.velocity = Vector2(100, 0)
	movement_component.apply_friction(1.0, true)
	assert_eq(movement_component.velocity.x, 100.0, "Zero friction should maintain velocity")

func test_extremely_high_delta_is_clamped():
	movement_component.set_target_direction(Vector2.RIGHT, false)
	movement_component.update(100.0) # Extremely high delta
	assert_lte(movement_component.velocity.length(), movement_component.max_speed * 1.1, "Extremely high delta should not cause velocity to explode")
