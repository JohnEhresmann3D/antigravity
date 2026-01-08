extends Area2D
class_name Checkpoint
## Checkpoint system for saving player progress

signal activated(checkpoint: Checkpoint)

@export var checkpoint_id: String = ""
@export var one_time_activation: bool = true
@export var visual_feedback: bool = true

var is_activated: bool = false
var player_spawn_position: Vector2


func _ready() -> void:
	# Store spawn position
	player_spawn_position = global_position
	
	# Connect signals
	body_entered.connect(_on_body_entered)
	
	# Add to checkpoints group
	add_to_group("checkpoints")
	
	# Generate ID if not set
	if checkpoint_id.is_empty():
		checkpoint_id = "checkpoint_" + str(get_instance_id())


func _on_body_entered(body: Node) -> void:
	"""Handle player entering checkpoint"""
	if body.is_in_group("player"):
		activate(body)


func activate(player: Node) -> void:
	"""Activate this checkpoint"""
	# Skip if already activated and one-time only
	if is_activated and one_time_activation:
		return
	
	is_activated = true
	
	# Emit signal
	activated.emit(self)
	
	# Update level manager if it exists
	var level = get_tree().get_first_node_in_group("level")
	if level and level.has_method("set_checkpoint"):
		level.set_checkpoint(self)
	
	# Visual feedback
	if visual_feedback:
		_play_activation_effect()


func _play_activation_effect() -> void:
	"""Visual effect when checkpoint is activated"""
	# Create a simple pulse effect
	var tween = create_tween()
	tween.set_loops(2)
	tween.tween_property(self, "modulate:a", 0.5, 0.2)
	tween.tween_property(self, "modulate:a", 1.0, 0.2)


func get_spawn_position() -> Vector2:
	"""Get the position where player should spawn"""
	return player_spawn_position


func get_checkpoint_id() -> String:
	"""Get checkpoint identifier"""
	return checkpoint_id


func reset() -> void:
	"""Reset checkpoint to inactive state"""
	is_activated = false
	modulate.a = 1.0
