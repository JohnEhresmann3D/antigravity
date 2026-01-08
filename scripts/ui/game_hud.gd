extends CanvasLayer
class_name GameHUD
## Main game HUD displaying health and collectibles

signal health_display_updated(current: int, maximum: int)
signal cores_display_updated(count: int)

@export var heart_texture: Texture2D
@export var heart_spacing: float = 5.0
@export var max_hearts: int = 5

@onready var health_container: HBoxContainer = $MarginContainer/VBoxContainer/HealthContainer
@onready var cores_label: Label = $MarginContainer/VBoxContainer/CoresContainer/CoresLabel

var current_hearts: int = 0
var gravity_cores_collected: int = 0


func _ready() -> void:
	# Initialize displays
	update_health_display(max_hearts, max_hearts)
	update_cores_display(0)


func update_health_display(current: int, maximum: int) -> void:
	"""Update health heart display"""
	# Clear existing hearts
	for child in health_container.get_children():
		child.queue_free()
	
	# Calculate hearts to show
	var hearts_to_show = ceili(float(maximum) / 20.0) # 1 heart per 20 HP
	var filled_hearts = ceili(float(current) / 20.0)
	
	# Create heart icons
	for i in range(hearts_to_show):
		var heart = TextureRect.new()
		
		if heart_texture:
			heart.texture = heart_texture
		else:
			# Fallback: create colored rect
			heart.custom_minimum_size = Vector2(16, 16)
		
		# Set color based on filled/empty
		if i < filled_hearts:
			heart.modulate = Color.WHITE # Filled
		else:
			heart.modulate = Color(0.3, 0.3, 0.3) # Empty/gray
		
		heart.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		health_container.add_child(heart)
	
	current_hearts = filled_hearts
	health_display_updated.emit(current, maximum)


func update_cores_display(count: int) -> void:
	"""Update gravity cores counter"""
	gravity_cores_collected = count
	cores_label.text = "Cores: %d" % count
	cores_display_updated.emit(count)


func add_core() -> void:
	"""Increment core counter"""
	update_cores_display(gravity_cores_collected + 1)


func set_player_health_component(health_component: HealthComponent) -> void:
	"""Connect to player's health component"""
	if health_component:
		health_component.health_changed.connect(update_health_display)
		# Initialize with current health
		update_health_display(health_component.current_health, health_component.max_health)


func reset() -> void:
	"""Reset HUD to initial state"""
	update_health_display(max_hearts * 20, max_hearts * 20)
	update_cores_display(0)
