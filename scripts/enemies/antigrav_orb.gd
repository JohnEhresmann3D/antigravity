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
	animated_sprite.play("idle")
	
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
			animated_sprite.play("idle")
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
	
	# Subtle rotation for visual effect
	rotation += delta * 0.5


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
	"""Perform a gravity flip to show off the mechanic"""
	state = "gravity_flip"
	animated_sprite.play("gravity_flip")
	flip_cooldown = 3.0
	
	await animated_sprite.animation_finished
	
	# Flip the sprite
	animated_sprite.flip_v = !animated_sprite.flip_v
	
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
