extends Node
class_name TurretAI
## AI component for stationary turret behavior with aiming and firing

signal target_acquired(target: Node)
signal target_lost
signal ready_to_fire(target: Node)
signal fired(projectile: Node)

@export_group("Targeting")
@export var detection_range: float = 300.0
@export var target_groups: Array[String] = ["player"]
@export var use_line_of_sight: bool = true
@export var aim_tolerance: float = 5.0 # degrees

@export_group("Firing")
@export var fire_rate: float = 2.0
@export var projectile_scene: PackedScene
@export var projectile_speed: float = 200.0

@export_group("Rotation")
@export var can_rotate: bool = true
@export var rotation_speed: float = 180.0 # degrees per second
@export var barrel_offset: Vector2 = Vector2(16, 0)

var current_target: Node = null
var can_fire: bool = true
var fire_timer: float = 0.0
var entity: Node2D
var detection_area: Area2D
var barrel_marker: Marker2D


func _ready() -> void:
	entity = get_parent()
	
	# Find detection area
	detection_area = entity.get_node_or_null("DetectionArea")
	if detection_area:
		detection_area.body_entered.connect(_on_body_entered)
		detection_area.body_exited.connect(_on_body_exited)
	
	# Find barrel marker
	barrel_marker = entity.get_node_or_null("BarrelMarker")


func _process(delta: float) -> void:
	# Update fire timer
	if fire_timer > 0:
		fire_timer -= delta
		if fire_timer <= 0:
			can_fire = true
	
	# Update targeting
	if current_target:
		_check_target_validity()
		if can_rotate:
			_aim_at_target(delta)


func _on_body_entered(body: Node) -> void:
	"""Handle body entering detection range"""
	if current_target:
		return
	
	for group in target_groups:
		if body.is_in_group(group):
			acquire_target(body)
			break


func _on_body_exited(body: Node) -> void:
	"""Handle body exiting detection range"""
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


func _aim_at_target(delta: float) -> void:
	"""Rotate to aim at target"""
	if not current_target or not current_target is Node2D:
		return
	
	var target_angle = entity.global_position.angle_to_point(current_target.global_position)
	var current_angle = entity.rotation
	
	# Rotate toward target
	var angle_diff = wrapf(target_angle - current_angle, -PI, PI)
	var rotation_step = deg_to_rad(rotation_speed) * delta
	
	if abs(angle_diff) < rotation_step:
		entity.rotation = target_angle
	else:
		entity.rotation += sign(angle_diff) * rotation_step
	
	# Check if aimed and ready to fire
	if abs(rad_to_deg(angle_diff)) < aim_tolerance and can_fire:
		ready_to_fire.emit(current_target)
		fire()


func fire() -> void:
	"""Fire a projectile at current target"""
	if not can_fire or not projectile_scene:
		return
	
	can_fire = false
	fire_timer = fire_rate
	
	# Spawn projectile
	var projectile = projectile_scene.instantiate()
	entity.get_parent().add_child(projectile)
	
	# Position projectile at barrel
	if barrel_marker:
		projectile.global_position = barrel_marker.global_position
	else:
		projectile.global_position = entity.global_position + barrel_offset.rotated(entity.rotation)
	
	# Set projectile direction
	var direction = Vector2.RIGHT.rotated(entity.rotation)
	if projectile.has_method("set_direction"):
		projectile.set_direction(direction)
	
	fired.emit(projectile)


func _check_target_validity() -> void:
	"""Check if current target is still valid"""
	if not is_instance_valid(current_target):
		lose_target()
		return
	
	if use_line_of_sight and not _has_line_of_sight(current_target):
		lose_target()


func _has_line_of_sight(target: Node) -> bool:
	"""Check line of sight to target"""
	if not target is Node2D:
		return false
	
	var space_state = entity.get_world_2d().direct_space_state
	var query = PhysicsRayQueryParameters2D.create(
		entity.global_position,
		target.global_position
	)
	query.exclude = [entity]
	
	var result = space_state.intersect_ray(query)
	return result.is_empty() or result.collider == target


func has_target() -> bool:
	"""Check if has a target"""
	return current_target != null


func get_target() -> Node:
	"""Get current target"""
	return current_target
