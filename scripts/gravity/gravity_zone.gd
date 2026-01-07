extends Area2D
class_name GravityZone
## GravityZone - Defines areas with custom gravity
## Can be normal gravity, zero-G, or custom direction

@export_enum("Normal", "Zero-G", "Custom") var zone_type: String = "Normal"
@export var custom_gravity_direction: Vector2 = Vector2.DOWN
@export var gravity_strength_multiplier: float = 1.0

var original_gravity_direction: Vector2
var original_gravity_strength: float
var players_in_zone: Array[Node] = []


func _ready() -> void:
	# Connect signals
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	
	# Store original gravity settings
	if GravityManager:
		original_gravity_direction = GravityManager.gravity_direction
		original_gravity_strength = GravityManager.gravity_strength


func _on_body_entered(body: Node2D) -> void:
	if body is Player:
		players_in_zone.append(body)
		_apply_zone_gravity()
		print("Player entered ", zone_type, " gravity zone")


func _on_body_exited(body: Node2D) -> void:
	if body is Player:
		players_in_zone.erase(body)
		
		# Restore original gravity if no players in zone
		if players_in_zone.is_empty():
			_restore_original_gravity()
			print("Player exited gravity zone")


func _apply_zone_gravity() -> void:
	if not GravityManager:
		return
	
	match zone_type:
		"Normal":
			# Use default gravity
			GravityManager.set_gravity_direction(Vector2.DOWN)
			GravityManager.set_gravity_strength(1.0)
		
		"Zero-G":
			# No gravity
			GravityManager.set_gravity_strength(0.0)
		
		"Custom":
			# Custom gravity direction and strength
			GravityManager.set_gravity_direction(custom_gravity_direction)
			GravityManager.set_gravity_strength(gravity_strength_multiplier)


func _restore_original_gravity() -> void:
	if not GravityManager:
		return
	
	GravityManager.set_gravity_direction(original_gravity_direction)
	GravityManager.set_gravity_strength(original_gravity_strength)
