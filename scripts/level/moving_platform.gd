extends AnimatableBody2D
class_name MovingPlatform
## Moving platform that carries the player

@export_group("Movement")
@export var move_direction: Vector2 = Vector2.RIGHT
@export var move_distance: float = 150.0
@export var move_speed: float = 50.0
@export var pause_at_ends: float = 0.5

@export_group("Options")
@export var start_moving: bool = true
@export var loop: bool = true

var start_position: Vector2
var end_position: Vector2
var current_target: Vector2
var is_moving: bool = true
var pause_timer: float = 0.0
var moving_to_end: bool = true


func _ready() -> void:
	# Calculate start and end positions
	start_position = global_position
	end_position = start_position + (move_direction.normalized() * move_distance)
	current_target = end_position if start_moving else start_position
	is_moving = start_moving
	
	# Ensure it's set up as a moving platform
	sync_to_physics = true


func _physics_process(delta: float) -> void:
	if not is_moving:
		# Handle pause timer
		if pause_timer > 0:
			pause_timer -= delta
			if pause_timer <= 0:
				is_moving = true
		return
	
	# Move towards current target
	var direction = (current_target - global_position).normalized()
	var distance_to_target = global_position.distance_to(current_target)
	
	# Calculate movement
	var move_amount = move_speed * delta
	
	if move_amount >= distance_to_target:
		# Reached target
		global_position = current_target
		_on_target_reached()
	else:
		# Move towards target
		global_position += direction * move_amount


func _on_target_reached() -> void:
	"""Called when platform reaches a target position"""
	# Pause at end
	if pause_at_ends > 0:
		is_moving = false
		pause_timer = pause_at_ends
	
	# Switch direction
	if moving_to_end:
		current_target = start_position
		moving_to_end = false
	else:
		current_target = end_position
		moving_to_end = true
		
		# Check if we should stop (no loop)
		if not loop and not moving_to_end:
			is_moving = false


func stop() -> void:
	"""Stop the platform"""
	is_moving = false
	pause_timer = 0.0


func start() -> void:
	"""Start the platform moving"""
	is_moving = true


func set_speed(speed: float) -> void:
	"""Change platform speed"""
	move_speed = speed
