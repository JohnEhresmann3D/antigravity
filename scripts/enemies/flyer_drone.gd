extends CharacterBody2D
## Flyer Drone Enemy - Flying patrol enemy that chases the player

@export var patrol_speed: float = 100.0
@export var chase_speed: float = 150.0
@export var detection_range: float = 200.0
@export var max_health: int = 2

var health: int = max_health
var player: Node2D = null
var state: String = "idle" # idle, alert, chase, damaged
var patrol_direction: Vector2 = Vector2.RIGHT
var patrol_timer: float = 0.0
var patrol_change_time: float = 3.0

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var detection_area: Area2D = $DetectionArea


func _ready():
	add_to_group("enemies")
	animated_sprite.play("idle")
	
	# Randomize patrol direction
	if randf() > 0.5:
		patrol_direction = Vector2.LEFT


func _physics_process(delta):
	match state:
		"idle":
			_patrol(delta)
		"chase":
			_chase_player(delta)
		"damaged":
			# Knockback handled in take_damage
			pass
	
	# Apply gravity (affected by GravityManager)
	if not is_on_floor():
		velocity += GravityManager.get_gravity_vector() * delta
	
	move_and_slide()
	
	# Update sprite direction
	if velocity.x != 0:
		animated_sprite.flip_h = velocity.x < 0


func _patrol(delta):
	"""Simple back-and-forth patrol"""
	patrol_timer += delta
	
	if patrol_timer >= patrol_change_time:
		patrol_direction = - patrol_direction
		patrol_timer = 0.0
	
	velocity.x = patrol_direction.x * patrol_speed
	
	if animated_sprite.animation != "flying":
		animated_sprite.play("flying")


func _chase_player(delta):
	"""Chase the player"""
	if not player:
		state = "idle"
		return
	
	var direction = (player.global_position - global_position).normalized()
	velocity.x = direction.x * chase_speed
	velocity.y = direction.y * chase_speed * 0.5 # Less vertical movement
	
	if animated_sprite.animation != "flying":
		animated_sprite.play("flying")


func take_damage(amount: int):
	"""Take damage and handle death"""
	health -= amount
	state = "damaged"
	animated_sprite.play("damaged")
	
	# Knockback
	var knockback_dir = - velocity.normalized() if velocity.length() > 0 else Vector2.LEFT
	velocity = knockback_dir * 200.0
	
	if health <= 0:
		die()
	else:
		await animated_sprite.animation_finished
		state = "idle" if not player else "chase"


func die():
	"""Handle enemy death"""
	# TODO: Drop resources, play death effect
	queue_free()


func _on_detection_area_body_entered(body):
	"""Player detected"""
	if body.is_in_group("player"):
		player = body
		state = "alert"
		animated_sprite.play("alert")
		await animated_sprite.animation_finished
		state = "chase"


func _on_detection_area_body_exited(body):
	"""Player left detection range"""
	if body == player:
		player = null
		state = "idle"
