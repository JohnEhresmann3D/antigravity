extends StaticBody2D
## Turret Enemy - Stationary enemy that fires projectiles at the player

@export var fire_rate: float = 2.0
@export var projectile_speed: float = 200.0
@export var detection_range: float = 300.0
@export var max_health: int = 3
@export var projectile_scene: PackedScene # Assign in editor

var health: int = max_health
var player: Node2D = null
var can_fire: bool = true
var state: String = "idle" # idle, aiming, firing, damaged

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var barrel_marker: Marker2D = $BarrelMarker
@onready var fire_timer: Timer = $FireTimer


func _ready():
	add_to_group("enemies")
	animated_sprite.play("idle")
	fire_timer.wait_time = fire_rate


func _process(delta):
	if player and state != "damaged":
		_aim_at_player()


func _aim_at_player():
	"""Rotate turret to face player"""
	var angle = global_position.angle_to_point(player.global_position)
	rotation = angle
	
	if state == "idle":
		state = "aiming"
		animated_sprite.play("aiming")


func fire_projectile():
	"""Fire a projectile at the player"""
	if not can_fire or not player or not projectile_scene:
		return
	
	state = "firing"
	animated_sprite.play("firing")
	
	# Spawn projectile
	var projectile = projectile_scene.instantiate()
	get_parent().add_child(projectile)
	projectile.global_position = barrel_marker.global_position
	
	# Set projectile direction
	var direction = (player.global_position - barrel_marker.global_position).normalized()
	if projectile.has_method("set_direction"):
		projectile.set_direction(direction)
	
	can_fire = false
	fire_timer.start()
	
	await animated_sprite.animation_finished
	state = "idle"
	animated_sprite.play("idle")


func take_damage(amount: int):
	"""Take damage and handle death"""
	health -= amount
	state = "damaged"
	animated_sprite.play("damaged")
	
	if health <= 0:
		die()
	else:
		await animated_sprite.animation_finished
		state = "idle"


func die():
	"""Handle enemy death"""
	# TODO: Drop resources, play death effect
	queue_free()


func _on_detection_area_body_entered(body):
	"""Player detected"""
	if body.is_in_group("player"):
		player = body


func _on_detection_area_body_exited(body):
	"""Player left detection range"""
	if body == player:
		player = null
		state = "idle"
		animated_sprite.play("idle")


func _on_fire_timer_timeout():
	"""Fire timer expired, can fire again"""
	can_fire = true
	if player and state != "damaged":
		fire_projectile()
