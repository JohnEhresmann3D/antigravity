extends Node2D
class_name LevelManager

## Manages level state, tutorial prompts, collectibles, and progression
##
## This script handles:
## - Tutorial prompt triggering based on player position
## - Gravity core collection tracking
## - Checkpoint activation
## - Level completion detection
## - Camera configuration

signal level_completed
signal collectible_collected(total: int, max_total: int)
signal checkpoint_reached(checkpoint_id: int)

@export var camera_limits := Rect2(0, 0, 2000, 1200)
@export var camera_zoom := 1.5

var gravity_cores_collected := 0
var total_gravity_cores := 20
var current_checkpoint := 0

@onready var player: CharacterBody2D = $Player
@onready var camera: Camera2D = $Player/Camera2D if has_node("Player/Camera2D") else null


func _ready() -> void:
	_setup_camera()
	_connect_collectibles()
	_connect_checkpoints()
	_setup_tutorial_prompts()


func _setup_camera() -> void:
	if camera:
		camera.enabled = true
		camera.zoom = Vector2(camera_zoom, camera_zoom)
		camera.position_smoothing_enabled = true
		camera.position_smoothing_speed = 5.0
		camera.limit_left = int(camera_limits.position.x)
		camera.limit_top = int(camera_limits.position.y)
		camera.limit_right = int(camera_limits.position.x + camera_limits.size.x)
		camera.limit_bottom = int(camera_limits.position.y + camera_limits.size.y)


func _connect_collectibles() -> void:
	if not has_node("Collectibles"):
		return
	
	var collectibles_node = $Collectibles
	for child in collectibles_node.get_children():
		if child.has_signal("collected"):
			child.collected.connect(_on_collectible_collected)


func _connect_checkpoints() -> void:
	if not has_node("Checkpoints"):
		return
	
	var checkpoints_node = $Checkpoints
	for child in checkpoints_node.get_children():
		if child.has_signal("activated"):
			child.activated.connect(_on_checkpoint_activated)


func _setup_tutorial_prompts() -> void:
	# Tutorial prompts will be triggered by Area2D zones
	# Each room has a trigger zone that shows the appropriate prompt
	pass


func _on_collectible_collected() -> void:
	gravity_cores_collected += 1
	collectible_collected.emit(gravity_cores_collected, total_gravity_cores)
	
	# Update HUD if it exists
	var hud = get_node_or_null("/root/GameHUD")
	if hud and hud.has_method("update_collectibles"):
		hud.update_collectibles(gravity_cores_collected, total_gravity_cores)


func _on_checkpoint_activated(checkpoint_id: int) -> void:
	if checkpoint_id > current_checkpoint:
		current_checkpoint = checkpoint_id
		checkpoint_reached.emit(checkpoint_id)


func complete_level() -> void:
	level_completed.emit()
	# Transition to next level or show completion screen
	print("Level 1 Complete! Gravity Cores: %d/%d" % [gravity_cores_collected, total_gravity_cores])
