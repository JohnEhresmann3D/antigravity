extends Area2D
class_name GravityCore
## Gravity core collectible for Level 1

signal collected(collector: Node)

@export var point_value: int = 1
@export var collection_animation_duration: float = 0.3
@export var bob_amplitude: float = 5.0
@export var bob_speed: float = 2.0

var is_collected: bool = false
var initial_position: Vector2
var time_elapsed: float = 0.0


func _ready() -> void:
	# Store initial position for bobbing animation
	initial_position = global_position
	
	# Connect collision signal
	body_entered.connect(_on_body_entered)
	
	# Add to collectibles group
	add_to_group("collectibles")
	add_to_group("gravity_cores")


func _process(delta: float) -> void:
	if is_collected:
		return
	
	# Bobbing animation
	time_elapsed += delta
	var bob_offset = sin(time_elapsed * bob_speed) * bob_amplitude
	global_position.y = initial_position.y + bob_offset


func _on_body_entered(body: Node) -> void:
	"""Handle collision with player"""
	if is_collected:
		return
	
	# Check if it's the player
	if body.is_in_group("player"):
		collect(body)


func collect(collector: Node) -> void:
	"""Trigger collection"""
	if is_collected:
		return
	
	is_collected = true
	
	# Emit signal
	collected.emit(collector)
	
	# Update global counter if GameManager exists
	if has_node("/root/GameManager"):
		get_node("/root/GameManager").add_gravity_cores(point_value)
	
	# Play collection animation
	_play_collection_animation()


func _play_collection_animation() -> void:
	"""Animate collection (shrink and fade)"""
	# Create tween for smooth animation
	var tween = create_tween()
	tween.set_parallel(true)
	
	# Shrink
	tween.tween_property(self, "scale", Vector2.ZERO, collection_animation_duration)
	
	# Fade out
	tween.tween_property(self, "modulate:a", 0.0, collection_animation_duration)
	
	# Move up slightly
	tween.tween_property(self, "global_position:y", global_position.y - 20, collection_animation_duration)
	
	# Destroy after animation
	tween.finished.connect(queue_free)


func get_value() -> int:
	"""Get point value"""
	return point_value
