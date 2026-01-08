extends CharacterBody2D
## Antigrav Orb Enemy - Gravity-defying enemy that teases the gravity flip mechanic

@export var float_speed: float = 80.0
@export var detection_range: float = 150.0
@export var max_health: int = 2
@export var flip_chance: float = 0.3 # Chance to flip gravity when patrolling

var health: int = max_health
var player: Node2D = null
var state: String = "idle" # idle, patrol, gravity_flip, damaged
var patrol_pattern: int = 0 # 0=horizontal, 1=vertical, 2=circular
var pattern_timer: float = 0.0
var pattern_duration: float = 5.0
var flip_cooldown: float = 0.0

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var detection_area: Area2D = $DetectionArea


func _ready():
	add_to_group("enemies")
	animated_sprite.play("Idle")
	
	# Randomize initial patrol pattern
	patrol_pattern = randi() % 3


func _physics_process(delta):
	flip_cooldown = max(0, flip_cooldown - delta)
	pattern_timer += delta
	
	# Change patrol pattern periodically
	if pattern_timer >= pattern_duration:
		patrol_pattern = (patrol_pattern + 1) % 3
		pattern_timer = 0.0
		
		# Chance to flip gravity
		if randf() < flip_chance and flip_cooldown <= 0:
			_perform_gravity_flip()
	
	match state:
		"idle":
			animated_sprite.play("Idle")
		"patrol":
			_patrol(delta)
		"gravity_flip":
			# Animation handles this state
			pass
		"damaged":
			# Knockback handled in take_damage
			pass
	
	# Antigrav orb ignores gravity!
	# It moves freely in any direction
	
	move_and_slide()
	
	# Whimsical floating animation when idle
	if state == "idle":
		var time = Time.get_ticks_msec() * 0.001
		# Gentle vertical bobbing
		position.y += sin(time * 2.0) * 0.3
		# Subtle horizontal sway
		position.x += cos(time * 1.5) * 0.2
		# Gentle rotation that changes direction
		rotation = sin(time * 0.8) * 0.15


func _patrol(delta):
	"""Patrol in various patterns to show off antigravity"""
	match patrol_pattern:
		0: # Horizontal wave
			velocity.x = sin(Time.get_ticks_msec() * 0.001) * float_speed
			velocity.y = cos(Time.get_ticks_msec() * 0.002) * float_speed * 0.5
		1: # Vertical wave
			velocity.x = cos(Time.get_ticks_msec() * 0.002) * float_speed * 0.5
			velocity.y = sin(Time.get_ticks_msec() * 0.001) * float_speed
		2: # Circular
			var angle = Time.get_ticks_msec() * 0.001
			velocity.x = cos(angle) * float_speed
			velocity.y = sin(angle) * float_speed
	
	if animated_sprite.animation != "patrol":
		animated_sprite.play("patrol")


func _perform_gravity_flip():
	"""Perform a gravity flip with dramatic motion"""
	state = "gravity_flip"
	animated_sprite.play("gravity_flip")
	flip_cooldown = 3.0
	
	# Store original values
	var original_scale = animated_sprite.scale
	var original_rotation = rotation
	
	# Phase 1: Charge up (0.3 seconds)
	var tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(animated_sprite, "scale", original_scale * 1.2, 0.3)
	tween.tween_property(self, "position:y", position.y - 10, 0.3).set_ease(Tween.EASE_OUT)
	await tween.finished
	
	# Phase 2: Spin flip (0.4 seconds) - dramatic 360° spin with position change
	tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(self, "rotation", original_rotation + PI * 2, 0.4).set_ease(Tween.EASE_IN_OUT)
	tween.tween_property(self, "position:y", position.y + 20, 0.4).set_ease(Tween.EASE_IN_OUT)
	# Pulse the scale during spin
	tween.tween_property(animated_sprite, "scale", original_scale * 0.8, 0.2).set_ease(Tween.EASE_IN)
	await get_tree().create_timer(0.2).timeout
	tween.tween_property(animated_sprite, "scale", original_scale * 1.1, 0.2).set_ease(Tween.EASE_OUT)
	await tween.finished
	
	# Flip the sprite vertically
	animated_sprite.flip_v = !animated_sprite.flip_v
	
	# Phase 3: Settle (0.3 seconds) - gentle wobble
	tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(animated_sprite, "scale", original_scale, 0.3).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "rotation", original_rotation, 0.3).set_ease(Tween.EASE_OUT)
	await tween.finished
	
	state = "patrol"


func take_damage(amount: int):
	"""Take damage and handle death"""
	health -= amount
	state = "damaged"
	animated_sprite.play("damaged")
	
	# Knockback (loses control briefly)
	var knockback_dir = Vector2(randf_range(-1, 1), randf_range(-1, 1)).normalized()
	velocity = knockback_dir * 300.0
	
	if health <= 0:
		die()
	else:
		await animated_sprite.animation_finished
		state = "patrol"


func die():
	"""Handle enemy death"""
	# TODO: Drop antigravity resources (higher chance)
	queue_free()


func _on_detection_area_body_entered(body):
	"""Player detected - start patrolling to show off"""
	if body.is_in_group("player"):
		player = body
		state = "patrol"


func _on_detection_area_body_exited(body):
	"""Player left - return to idle"""
	if body == player:
		player = null
		state = "idle"
