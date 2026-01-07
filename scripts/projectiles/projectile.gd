extends Area2D
## Projectile - Base projectile script for enemy attacks

@export var speed: float = 200.0
@export var damage: int = 1
@export var lifetime: float = 5.0
@export var affected_by_gravity: bool = false

var direction: Vector2 = Vector2.RIGHT
var life_timer: float = 0.0

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D


func _ready():
	add_to_group("projectiles")
	
	# Play animation based on scene name
	if "energy_ball" in name.to_lower():
		animated_sprite.play("energy_ball")
	elif "laser" in name.to_lower():
		animated_sprite.play("laser_bolt")
	elif "plasma" in name.to_lower():
		animated_sprite.play("plasma_shot")


func _physics_process(delta):
	life_timer += delta
	
	# Destroy after lifetime expires
	if life_timer >= lifetime:
		_destroy()
		return
	
	# Move in direction
	position += direction * speed * delta
	
	# Apply gravity if needed (for plasma shots)
	if affected_by_gravity:
		direction += GravityManager.get_gravity_vector().normalized() * delta * 2.0
		direction = direction.normalized()
	
	# Rotate sprite to face movement direction
	rotation = direction.angle()


func set_direction(new_direction: Vector2):
	"""Set the projectile's movement direction"""
	direction = new_direction.normalized()


func _on_body_entered(body):
	"""Handle collision with player or environment"""
	if body.is_in_group("player"):
		# Damage player
		if body.has_method("take_damage"):
			body.take_damage(damage)
	
	# Destroy projectile on any collision
	_destroy()


func _on_screen_exited():
	"""Destroy projectile when it leaves the screen"""
	queue_free()


func _destroy():
	"""Play impact animation and destroy"""
	# TODO: Play impact effect
	# For now, just destroy immediately
	queue_free()
