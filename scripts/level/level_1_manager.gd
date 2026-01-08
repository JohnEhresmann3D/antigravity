extends Node2D
class_name Level1Manager
## Manages Level 1 "Awakening" - Tutorial level

signal cores_collected_changed(current: int, total: int)
signal checkpoint_reached(checkpoint: Checkpoint)

@export var total_gravity_cores: int = 20
@export var tutorial_prompts: Dictionary = {
	"room_1": "Use A/D or Arrow Keys to move",
	"room_2": "Press SPACE, W, or UP to jump",
	"room_3": "Hold jump longer to jump higher",
	"room_4": "Jump just after walking off edges",
	"room_5": "Combine movement and jumping",
	"room_6": "Wait for the platform",
	"room_7": "Reach the top",
	"room_8": "Approach the Gravity Core"
}

var cores_collected: int = 0
var current_checkpoint: Checkpoint = null
var start_time: float = 0.0
var death_count: int = 0
var player: Node = null


func _ready() -> void:
	# Add to level group
	add_to_group("level")
	
	# Start timer
	start_time = Time.get_ticks_msec() / 1000.0
	
	# Find player
	await get_tree().process_frame
	player = get_tree().get_first_node_in_group("player")
	
	# Connect to all gravity cores
	_connect_gravity_cores()
	
	# Connect to player death if available
	if player and player.has_node("HealthComponent"):
		var health = player.get_node("HealthComponent")
		health.died.connect(_on_player_died)
	
	# Update HUD
	_update_hud()


func _connect_gravity_cores() -> void:
	"""Connect to all gravity core collectibles"""
	var cores = get_tree().get_nodes_in_group("gravity_cores")
	for core in cores:
		if core.has_signal("collected"):
			core.collected.connect(_on_gravity_core_collected)


func _on_gravity_core_collected(collector: Node) -> void:
	"""Handle gravity core collection"""
	cores_collected += 1
	cores_collected_changed.emit(cores_collected, total_gravity_cores)
	
	# Update HUD
	var hud = get_tree().get_first_node_in_group("hud")
	if hud and hud.has_method("add_core"):
		hud.add_core()
	
	# Check for 100% collection
	if cores_collected >= total_gravity_cores:
		print("All gravity cores collected!")


func set_checkpoint(checkpoint: Checkpoint) -> void:
	"""Set the current checkpoint"""
	current_checkpoint = checkpoint
	checkpoint_reached.emit(checkpoint)
	print("Checkpoint reached: ", checkpoint.get_checkpoint_id())


func respawn_player() -> void:
	"""Respawn player at last checkpoint"""
	if not player:
		return
	
	var spawn_position = Vector2.ZERO
	
	if current_checkpoint:
		spawn_position = current_checkpoint.get_spawn_position()
	else:
		# Default spawn (start of level)
		spawn_position = Vector2(100, 100) # Adjust based on your level
	
	player.global_position = spawn_position
	
	# Reset player health if available
	if player.has_node("HealthComponent"):
		var health = player.get_node("HealthComponent")
		health.revive()


func _on_player_died() -> void:
	"""Handle player death"""
	death_count += 1
	
	# Wait a moment before respawning
	await get_tree().create_timer(1.0).timeout
	respawn_player()


func get_cores_collected() -> int:
	"""Get number of cores collected"""
	return cores_collected


func get_total_cores() -> int:
	"""Get total cores in level"""
	return total_gravity_cores


func get_completion_time() -> float:
	"""Get time elapsed since level start"""
	return (Time.get_ticks_msec() / 1000.0) - start_time


func get_death_count() -> int:
	"""Get number of player deaths"""
	return death_count


func _update_hud() -> void:
	"""Update HUD with current stats"""
	var hud = get_tree().get_first_node_in_group("hud")
	if hud:
		if hud.has_method("update_cores_display"):
			hud.update_cores_display(cores_collected)
		
		# Connect to player health
		if player and player.has_node("HealthComponent") and hud.has_method("set_player_health_component"):
			hud.set_player_health_component(player.get_node("HealthComponent"))


func show_tutorial_prompt(room_id: String) -> void:
	"""Show tutorial prompt for a room"""
	if tutorial_prompts.has(room_id):
		var tutorial = get_tree().get_first_node_in_group("tutorial_prompt")
		if tutorial and tutorial.has_method("show_prompt"):
			tutorial.show_prompt(tutorial_prompts[room_id])


func get_completion_percentage() -> float:
	"""Get completion percentage (0.0 to 1.0)"""
	if total_gravity_cores == 0:
		return 0.0
	return float(cores_collected) / float(total_gravity_cores)
