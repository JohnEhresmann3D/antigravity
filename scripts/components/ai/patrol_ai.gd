extends Node
class_name PatrolAI
## AI component for patrol behavior with waypoints

signal reached_waypoint(waypoint_index: int)
signal patrol_direction_changed(new_direction: Vector2)

@export_group("Patrol")
@export var patrol_points: Array[Vector2] = []
@export var patrol_speed: float = 100.0
@export var loop_patrol: bool = true
@export var reverse_on_end: bool = false

@export_group("Wait")
@export var wait_at_waypoints: bool = true
@export var wait_time: float = 2.0

@export_group("Detection")
@export var waypoint_reach_distance: float = 10.0

var current_point_index: int = 0
var wait_timer: float = 0.0
var is_waiting: bool = false
var patrol_direction: int = 1 # 1 = forward, -1 = backward
var entity: Node2D


func _ready() -> void:
	entity = get_parent()


func _process(delta: float) -> void:
	if is_waiting and wait_timer > 0:
		wait_timer -= delta
		if wait_timer <= 0:
			is_waiting = false


func get_target_velocity() -> Vector2:
	"""Get the velocity to move toward current patrol point"""
	if patrol_points.is_empty() or is_waiting:
		return Vector2.ZERO
	
	var target = patrol_points[current_point_index]
	var distance = entity.global_position.distance_to(target)
	
	# Check if reached waypoint
	if distance < waypoint_reach_distance:
		_on_waypoint_reached()
		return Vector2.ZERO
	
	# Move toward waypoint
	var direction = (target - entity.global_position).normalized()
	patrol_direction_changed.emit(direction)
	return direction * patrol_speed


func _on_waypoint_reached() -> void:
	"""Handle reaching a waypoint"""
	reached_waypoint.emit(current_point_index)
	
	# Start waiting if configured
	if wait_at_waypoints:
		is_waiting = true
		wait_timer = wait_time
	
	# Move to next waypoint
	_advance_waypoint()


func _advance_waypoint() -> void:
	"""Move to next waypoint in sequence"""
	if patrol_points.is_empty():
		return
	
	current_point_index += patrol_direction
	
	# Handle end of patrol path
	if current_point_index >= patrol_points.size():
		if loop_patrol:
			current_point_index = 0
		elif reverse_on_end:
			patrol_direction = -1
			current_point_index = patrol_points.size() - 2
		else:
			current_point_index = patrol_points.size() - 1
	
	elif current_point_index < 0:
		if reverse_on_end:
			patrol_direction = 1
			current_point_index = 1
		else:
			current_point_index = 0


func add_patrol_point(point: Vector2) -> void:
	"""Add a waypoint to the patrol path"""
	patrol_points.append(point)


func clear_patrol_points() -> void:
	"""Clear all patrol points"""
	patrol_points.clear()
	current_point_index = 0


func set_patrol_speed(speed: float) -> void:
	"""Change patrol speed"""
	patrol_speed = speed


func get_current_target() -> Vector2:
	"""Get current waypoint position"""
	if patrol_points.is_empty():
		return Vector2.ZERO
	return patrol_points[current_point_index]
