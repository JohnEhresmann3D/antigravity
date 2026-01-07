extends Node
class_name ChaseAI
## AI component for chasing and pursuing targets

signal target_acquired(target: Node)
signal target_lost
signal target_in_range(target: Node, distance: float)

@export_group("Chase")
@export var chase_speed: float = 150.0
@export var stop_distance: float = 50.0
@export var lose_target_distance: float = 500.0

@export_group("Detection")
@export var detection_range: float = 200.0
@export var target_groups: Array[String] = ["player"]
@export var use_line_of_sight: bool = false

var current_target: Node = null
var entity: Node2D
var detection_area: Area2D


func _ready() -> void:
	entity = get_parent()
	
	# Try to find detection area
	detection_area = entity.get_node_or_null("DetectionArea")
	if detection_area:
		detection_area.body_entered.connect(_on_body_entered)
		detection_area.body_exited.connect(_on_body_exited)


func _process(delta: float) -> void:
	if current_target:
		_check_target_validity()


func get_target_velocity() -> Vector2:
	"""Get velocity to chase current target"""
	if not current_target:
		return Vector2.ZERO
	
	var distance = entity.global_position.distance_to(current_target.global_position)
	
	# Stop if within stop distance
	if distance < stop_distance:
		target_in_range.emit(current_target, distance)
		return Vector2.ZERO
	
	# Chase target
	var direction = (current_target.global_position - entity.global_position).normalized()
	return direction * chase_speed


func _on_body_entered(body: Node) -> void:
	"""Handle body entering detection area"""
	if current_target:
		return # Already have a target
	
	# Check if body is in target groups
	for group in target_groups:
		if body.is_in_group(group):
			acquire_target(body)
			break


func _on_body_exited(body: Node) -> void:
	"""Handle body exiting detection area"""
	if body == current_target:
		lose_target()


func acquire_target(target: Node) -> void:
	"""Acquire a new target"""
	if use_line_of_sight and not _has_line_of_sight(target):
		return
	
	current_target = target
	target_acquired.emit(target)


func lose_target() -> void:
	"""Lose current target"""
	if current_target:
		current_target = null
		target_lost.emit()


func _check_target_validity() -> void:
	"""Check if current target is still valid"""
	if not is_instance_valid(current_target):
		lose_target()
		return
	
	# Check distance
	var distance = entity.global_position.distance_to(current_target.global_position)
	if distance > lose_target_distance:
		lose_target()
		return
	
	# Check line of sight if enabled
	if use_line_of_sight and not _has_line_of_sight(current_target):
		lose_target()


func _has_line_of_sight(target: Node) -> bool:
	"""Check if there's a clear line of sight to target"""
	if not target is Node2D:
		return false
	
	var space_state = entity.get_world_2d().direct_space_state
	var query = PhysicsRayQueryParameters2D.create(
		entity.global_position,
		target.global_position
	)
	query.exclude = [entity]
	
	var result = space_state.intersect_ray(query)
	
	# If ray hits the target or nothing, we have line of sight
	return result.is_empty() or result.collider == target


func has_target() -> bool:
	"""Check if currently has a target"""
	return current_target != null


func get_target() -> Node:
	"""Get current target"""
	return current_target


func get_distance_to_target() -> float:
	"""Get distance to current target"""
	if not current_target:
		return -1.0
	return entity.global_position.distance_to(current_target.global_position)
