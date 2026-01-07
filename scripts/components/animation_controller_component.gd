extends Node
class_name AnimationControllerComponent
## Manages animation states based on entity state

signal animation_changed(animation_name: String)

@export var animated_sprite: AnimatedSprite2D
@export var auto_flip_sprite: bool = true

var current_animation: String = ""
var is_playing: bool = false


func _ready() -> void:
	if not animated_sprite:
		animated_sprite = get_parent().get_node_or_null("AnimatedSprite2D")
	
	if not animated_sprite:
		push_error("AnimationControllerComponent: No AnimatedSprite2D found!")


func play(animation_name: String, force: bool = false) -> void:
	"""Play an animation"""
	if not animated_sprite:
		return
	
	# Don't interrupt if same animation and not forcing
	if current_animation == animation_name and not force:
		return
	
	current_animation = animation_name
	animated_sprite.play(animation_name)
	is_playing = true
	animation_changed.emit(animation_name)


func play_if_not(animation_name: String, exclude_animations: Array[String]) -> void:
	"""Play animation unless current animation is in exclude list"""
	if current_animation in exclude_animations:
		return
	play(animation_name)


func stop() -> void:
	"""Stop current animation"""
	if animated_sprite:
		animated_sprite.stop()
		is_playing = false


func is_animation_playing(animation_name: String) -> bool:
	"""Check if specific animation is playing"""
	return current_animation == animation_name and is_playing


func set_sprite_direction(direction: Vector2) -> void:
	"""Flip sprite based on direction"""
	if not animated_sprite or not auto_flip_sprite:
		return
	
	if direction.x < 0:
		animated_sprite.flip_h = true
	elif direction.x > 0:
		animated_sprite.flip_h = false


func set_sprite_flip_h(flipped: bool) -> void:
	"""Manually set horizontal flip"""
	if animated_sprite:
		animated_sprite.flip_h = flipped


func set_sprite_flip_v(flipped: bool) -> void:
	"""Manually set vertical flip"""
	if animated_sprite:
		animated_sprite.flip_v = flipped


func get_current_animation() -> String:
	"""Get currently playing animation name"""
	return current_animation


func has_animation(animation_name: String) -> bool:
	"""Check if animation exists"""
	if not animated_sprite or not animated_sprite.sprite_frames:
		return false
	return animated_sprite.sprite_frames.has_animation(animation_name)
