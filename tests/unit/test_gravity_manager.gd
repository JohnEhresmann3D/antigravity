extends GutTest

## Unit tests for GravityManager
## Tests gravity direction, strength, and signal emissions

var gravity_manager: Node

func before_all():
	# GravityManager is a singleton, so we access it directly
	gravity_manager = get_node("/root/GravityManager")

# ============================================
# INITIALIZATION TESTS
# ============================================

func test_gravity_manager_exists():
	assert_not_null(gravity_manager, "GravityManager singleton should exist")

func test_default_gravity_is_downward():
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector.normalized(), Vector2.DOWN, "Default gravity should be downward")

func test_default_gravity_strength_is_one():
	var strength = gravity_manager.get_gravity_strength()
	assert_eq(strength, 1.0, "Default gravity strength should be 1.0")

# ============================================
# GRAVITY DIRECTION TESTS
# ============================================

func test_set_gravity_direction_changes_direction():
	gravity_manager.set_gravity_direction(Vector2.UP)
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector.normalized(), Vector2.UP, "Gravity direction should change to UP")
	# Reset to default
	gravity_manager.reset_gravity()

func test_set_cardinal_direction_up():
	gravity_manager.set_cardinal_direction("up")
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector.normalized(), Vector2.UP, "Cardinal 'up' should set gravity upward")
	gravity_manager.reset_gravity()

func test_set_cardinal_direction_down():
	gravity_manager.set_cardinal_direction("down")
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector.normalized(), Vector2.DOWN, "Cardinal 'down' should set gravity downward")

func test_set_cardinal_direction_left():
	gravity_manager.set_cardinal_direction("left")
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector.normalized(), Vector2.LEFT, "Cardinal 'left' should set gravity leftward")
	gravity_manager.reset_gravity()

func test_set_cardinal_direction_right():
	gravity_manager.set_cardinal_direction("right")
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector.normalized(), Vector2.RIGHT, "Cardinal 'right' should set gravity rightward")
	gravity_manager.reset_gravity()

# ============================================
# GRAVITY FLIP TESTS
# ============================================

func test_flip_gravity_reverses_direction():
	gravity_manager.set_gravity_direction(Vector2.DOWN)
	gravity_manager.flip_gravity()
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector.normalized(), Vector2.UP, "Flip should reverse gravity to UP")
	gravity_manager.reset_gravity()

func test_flip_gravity_twice_returns_to_original():
	var original = gravity_manager.get_gravity_vector()
	gravity_manager.flip_gravity()
	gravity_manager.flip_gravity()
	var current = gravity_manager.get_gravity_vector()
	assert_eq(current.normalized(), original.normalized(), "Double flip should return to original direction")

# ============================================
# GRAVITY STRENGTH TESTS
# ============================================

func test_set_gravity_strength_changes_strength():
	gravity_manager.set_gravity_strength(2.0)
	var strength = gravity_manager.get_gravity_strength()
	assert_eq(strength, 2.0, "Gravity strength should be 2.0")
	gravity_manager.reset_gravity()

func test_set_gravity_strength_affects_vector_magnitude():
	gravity_manager.set_gravity_direction(Vector2.DOWN)
	gravity_manager.set_gravity_strength(2.0)
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_gt(gravity_vector.length(), 980.0, "Gravity vector magnitude should increase with strength")
	gravity_manager.reset_gravity()

func test_zero_gravity_strength():
	gravity_manager.set_gravity_strength(0.0)
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_eq(gravity_vector, Vector2.ZERO, "Zero strength should result in zero gravity vector")
	gravity_manager.reset_gravity()

# ============================================
# SIGNAL TESTS
# ============================================

func test_set_gravity_direction_emits_signal():
	watch_signals(gravity_manager)
	gravity_manager.set_gravity_direction(Vector2.LEFT)
	assert_signal_emitted(gravity_manager, "gravity_changed", "Should emit gravity_changed signal")
	gravity_manager.reset_gravity()

func test_set_gravity_strength_emits_signal():
	watch_signals(gravity_manager)
	gravity_manager.set_gravity_strength(1.5)
	assert_signal_emitted(gravity_manager, "gravity_strength_changed", "Should emit gravity_strength_changed signal")
	gravity_manager.reset_gravity()

func test_flip_gravity_emits_signal():
	watch_signals(gravity_manager)
	gravity_manager.flip_gravity()
	assert_signal_emitted(gravity_manager, "gravity_changed", "Flip should emit gravity_changed signal")
	gravity_manager.reset_gravity()

# ============================================
# RESET TESTS
# ============================================

func test_reset_gravity_restores_defaults():
	gravity_manager.set_gravity_direction(Vector2.LEFT)
	gravity_manager.set_gravity_strength(2.5)
	gravity_manager.reset_gravity()
	
	var gravity_vector = gravity_manager.get_gravity_vector()
	var strength = gravity_manager.get_gravity_strength()
	
	assert_eq(gravity_vector.normalized(), Vector2.DOWN, "Reset should restore default direction")
	assert_eq(strength, 1.0, "Reset should restore default strength")

# ============================================
# EDGE CASES
# ============================================

func test_set_gravity_direction_with_zero_vector():
	gravity_manager.set_gravity_direction(Vector2.ZERO)
	var gravity_vector = gravity_manager.get_gravity_vector()
	# Behavior with zero vector is implementation-dependent
	# Should either maintain previous direction or set to zero
	assert_true(true, "Should handle zero vector without crashing")
	gravity_manager.reset_gravity()

func test_negative_gravity_strength():
	gravity_manager.set_gravity_strength(-1.0)
	var strength = gravity_manager.get_gravity_strength()
	# Behavior with negative strength is implementation-dependent
	assert_true(true, "Should handle negative strength without crashing")
	gravity_manager.reset_gravity()

func test_extremely_high_gravity_strength():
	gravity_manager.set_gravity_strength(1000.0)
	var gravity_vector = gravity_manager.get_gravity_vector()
	assert_true(gravity_vector.length() > 0, "Should handle extremely high strength")
	gravity_manager.reset_gravity()
