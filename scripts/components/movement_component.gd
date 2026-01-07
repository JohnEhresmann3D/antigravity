extends Node
class_name MovementComponent
## Handles movement physics with acceleration, friction, and speed limits

signal velocity_changed(new_velocity: Vector2)

@export_group("Speed")
@export var speed: float = 200.0
@export var max_speed: float = 500.0

@export_group("Physics")
@export var acceleration: float = 1000.0
@export var friction: float = 800.0
@export var air_friction: float = 200.0

var velocity: Vector2 = Vector2.ZERO
var target_velocity: Vector2 = Vector2.ZERO
var is_grounded: bool = false


func update(delta: float) -> void:
	"""Update velocity based on target and physics"""
	# Apply acceleration toward target
	velocity = velocity.move_toward(target_velocity, acceleration * delta)
	
	# Clamp to max speed
	if velocity.length() > max_speed:
		velocity = velocity.normalized() * max_speed
	
	velocity_changed.emit(velocity)


func set_target(target: Vector2) -> void:
	"""Set the target velocity to move toward"""
	target_velocity = target


func set_target_direction(direction: Vector2, use_speed: bool = true) -> void:
	"""Set target velocity from a direction vector"""
	if use_speed:
		target_velocity = direction.normalized() * speed
	else:
		target_velocity = direction


func apply_friction(delta: float, use_air_friction: bool = false) -> void:
	"""Apply friction to slow down velocity"""
	var friction_amount = air_friction if use_air_friction else friction
	velocity = velocity.move_toward(Vector2.ZERO, friction_amount * delta)
	velocity_changed.emit(velocity)


func apply_impulse(impulse: Vector2) -> void:
	"""Apply an instant force (knockback, jump, etc.)"""
	velocity += impulse
	
	# Clamp to max speed
	if velocity.length() > max_speed:
		velocity = velocity.normalized() * max_speed
	
	velocity_changed.emit(velocity)


func stop() -> void:
	"""Immediately stop all movement"""
	velocity = Vector2.ZERO
	target_velocity = Vector2.ZERO
	velocity_changed.emit(velocity)


func get_speed() -> float:
	"""Get current speed (magnitude of velocity)"""
	return velocity.length()


func get_direction() -> Vector2:
	"""Get current movement direction (normalized)"""
	if velocity.length() > 0:
		return velocity.normalized()
	return Vector2.ZERO


func is_moving() -> bool:
	"""Check if entity is moving"""
	return velocity.length() > 1.0
