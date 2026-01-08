extends CanvasLayer
class_name TutorialPrompt
## Displays tutorial prompts to the player

signal prompt_shown(text: String)
signal prompt_dismissed

@export var fade_duration: float = 0.3
@export var auto_dismiss_delay: float = 5.0

@onready var panel: Panel = $Panel
@onready var label: Label = $Panel/MarginContainer/Label

var is_showing: bool = false
var auto_dismiss_timer: float = 0.0


func _ready() -> void:
	# Start hidden
	modulate = Color(1, 1, 1, 0)
	visible = false


func _process(delta: float) -> void:
	# Handle auto-dismiss timer
	if is_showing and auto_dismiss_delay > 0 and auto_dismiss_timer > 0:
		auto_dismiss_timer -= delta
		if auto_dismiss_timer <= 0:
			dismiss()


func show_prompt(text: String, auto_dismiss: bool = true) -> void:
	"""Display a tutorial prompt"""
	if is_showing:
		dismiss()
		await get_tree().create_timer(fade_duration).timeout
	
	# Set text
	label.text = text
	
	# Show and fade in
	visible = true
	is_showing = true
	
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 1.0, fade_duration)
	
	# Set auto-dismiss timer
	if auto_dismiss:
		auto_dismiss_timer = auto_dismiss_delay
	
	prompt_shown.emit(text)


func dismiss() -> void:
	"""Hide the tutorial prompt"""
	if not is_showing:
		return
	
	is_showing = false
	auto_dismiss_timer = 0.0
	
	# Fade out
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, fade_duration)
	tween.finished.connect(func(): visible = false)
	
	prompt_dismissed.emit()


func is_prompt_visible() -> bool:
	"""Check if prompt is currently showing"""
	return is_showing
