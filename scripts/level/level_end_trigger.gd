extends Area2D
class_name LevelEndTrigger
## Triggers level completion when player reaches gravity core chamber

signal level_completed(stats: Dictionary)

@export var next_level_path: String = ""
@export var unlock_ability: String = "gravity_flip"
@export var completion_delay: float = 2.0

var is_triggered: bool = false


func _ready() -> void:
	# Connect signals
	body_entered.connect(_on_body_entered)
	
	# Add to group
	add_to_group("level_triggers")


func _on_body_entered(body: Node) -> void:
	"""Handle player entering end trigger"""
	if is_triggered:
		return
	
	if body.is_in_group("player"):
		trigger_completion(body)


func trigger_completion(player: Node) -> void:
	"""Trigger level completion sequence"""
	if is_triggered:
		return
	
	is_triggered = true
	
	# Gather completion stats
	var stats = _gather_stats()
	
	# Show completion message
	_show_completion_message(stats)
	
	# Emit signal
	level_completed.emit(stats)
	
	# Wait before transitioning
	await get_tree().create_timer(completion_delay).timeout
	
	# Transition to next level or menu
	_transition_to_next()


func _gather_stats() -> Dictionary:
	"""Gather level completion statistics"""
	var stats = {
		"cores_collected": 0,
		"total_cores": 0,
		"completion_time": 0.0,
		"deaths": 0,
		"ability_unlocked": unlock_ability
	}
	
	# Get level manager stats if available
	var level = get_tree().get_first_node_in_group("level")
	if level:
		if level.has_method("get_cores_collected"):
			stats.cores_collected = level.get_cores_collected()
		if level.has_method("get_total_cores"):
			stats.total_cores = level.get_total_cores()
		if level.has_method("get_completion_time"):
			stats.completion_time = level.get_completion_time()
		if level.has_method("get_death_count"):
			stats.deaths = level.get_death_count()
	
	return stats


func _show_completion_message(stats: Dictionary) -> void:
	"""Display level completion message"""
	# Create completion UI
	var message = "GRAVITY CORE SYNCHRONIZED\n"
	message += "New Ability Unlocked: %s\n\n" % unlock_ability.to_upper().replace("_", " ")
	message += "Gravity Cores: %d/%d\n" % [stats.cores_collected, stats.total_cores]
	
	if stats.completion_time > 0:
		var minutes = int(stats.completion_time / 60)
		var seconds = int(stats.completion_time) % 60
		message += "Time: %02d:%02d\n" % [minutes, seconds]
	
	# Show via tutorial prompt if available
	var tutorial = get_tree().get_first_node_in_group("tutorial_prompt")
	if tutorial and tutorial.has_method("show_prompt"):
		tutorial.show_prompt(message, false)
	else:
		print(message)


func _transition_to_next() -> void:
	"""Transition to next level or menu"""
	if next_level_path.is_empty():
		# Return to main menu or level select
		print("Level complete! No next level specified.")
		# Could load main menu here
	else:
		# Load next level
		get_tree().change_scene_to_file(next_level_path)


func set_next_level(path: String) -> void:
	"""Set the next level path"""
	next_level_path = path
