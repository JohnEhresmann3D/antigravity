extends Node
## GravityManager - Singleton for managing global gravity system
## Handles gravity direction, strength, and zones

signal gravity_changed(new_direction: Vector2)
signal gravity_strength_changed(new_strength: float)

## Current gravity direction (normalized vector)
var gravity_direction: Vector2 = Vector2.DOWN

## Gravity strength multiplier
var gravity_strength: float = 1.0

## Base gravity value (pixels per second squared)
const BASE_GRAVITY: float = 980.0

## Debug mode - allows runtime gravity adjustment
var debug_mode: bool = false


func _ready() -> void:
	print("GravityManager initialized")
	print("Base gravity: ", BASE_GRAVITY)
	print("Initial direction: ", gravity_direction)


## Get the current gravity vector (direction * strength * base)
func get_gravity_vector() -> Vector2:
	return gravity_direction * gravity_strength * BASE_GRAVITY


## Set gravity direction (will be normalized)
func set_gravity_direction(direction: Vector2) -> void:
	if direction.length() > 0:
		gravity_direction = direction.normalized()
		gravity_changed.emit(gravity_direction)
		print("Gravity direction changed to: ", gravity_direction)


## Flip gravity 180 degrees
func flip_gravity() -> void:
	gravity_direction = - gravity_direction
	gravity_changed.emit(gravity_direction)
	print("Gravity flipped to: ", gravity_direction)


## Set gravity strength multiplier
func set_gravity_strength(strength: float) -> void:
	gravity_strength = clamp(strength, 0.0, 5.0)
	gravity_strength_changed.emit(gravity_strength)
	print("Gravity strength changed to: ", gravity_strength)


## Get current gravity strength
func get_gravity_strength() -> float:
	return gravity_strength


## Rotate gravity direction by angle (in radians)
func rotate_gravity(angle: float) -> void:
	gravity_direction = gravity_direction.rotated(angle)
	gravity_changed.emit(gravity_direction)


## Set gravity to one of the cardinal directions
func set_cardinal_direction(direction: String) -> void:
	match direction.to_lower():
		"down":
			set_gravity_direction(Vector2.DOWN)
		"up":
			set_gravity_direction(Vector2.UP)
		"left":
			set_gravity_direction(Vector2.LEFT)
		"right":
			set_gravity_direction(Vector2.RIGHT)
		_:
			push_warning("Invalid cardinal direction: " + direction)


## Reset gravity to default (down)
func reset_gravity() -> void:
	set_gravity_direction(Vector2.DOWN)
	set_gravity_strength(1.0)
	print("Gravity reset to default")


## Debug function to adjust gravity at runtime
func _input(event: InputEvent) -> void:
	if not debug_mode:
		return
	
	# Debug controls (only active when debug_mode = true)
	if event.is_action_pressed("ui_up"):
		set_cardinal_direction("up")
	elif event.is_action_pressed("ui_down"):
		set_cardinal_direction("down")
	elif event.is_action_pressed("ui_left"):
		set_cardinal_direction("left")
	elif event.is_action_pressed("ui_right"):
		set_cardinal_direction("right")
