extends CharacterBody2D
class_name Player
## Player Controller for Cosmo
## Handles movement, jumping, gravity, and animations

# Movement parameters
@export_group("Movement")
@export var move_speed: float = 200.0
@export var run_speed: float = 300.0
@export var acceleration: float = 1000.0
@export var friction: float = 800.0

# Jump parameters
@export_group("Jump")
@export var jump_velocity: float = -400.0
@export var jump_cut_multiplier: float = 0.5
@export var coyote_time: float = 0.1
@export var jump_buffer_time: float = 0.1

# Gravity parameters
@export_group("Gravity")
@export var fall_gravity_multiplier: float = 1.5
@export var max_fall_speed: float = 500.0

# Abilities
@export_group("Abilities")
@export var has_gravity_flip: bool = false
@export var gravity_flip_cooldown: float = 0.5

# References
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

# State variables
var is_running: bool = false
var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0
var gravity_flip_timer: float = 0.0
var is_flipped: bool = false

# Input
var move_input: float = 0.0
var jump_pressed: bool = false
var jump_just_pressed: bool = false
var run_pressed: bool = false


func _ready() -> void:
	# Connect to gravity manager signals
	if GravityManager:
		GravityManager.gravity_changed.connect(_on_gravity_changed)
	
	# Set up initial animation
	animated_sprite.play("idle")


func _physics_process(delta: float) -> void:
	# Get input
	_handle_input()
	
	# Update timers
	_update_timers(delta)
	
	# Apply gravity
	_apply_gravity(delta)
	
	# Handle movement
	_handle_movement(delta)
	
	# Handle jumping
	_handle_jump()
	
	# Handle abilities
	_handle_abilities()
	
	# Move the character
	move_and_slide()
	
	# Update animations
	_update_animation()
	
	# Update sprite direction
	_update_sprite_direction()


func _handle_input() -> void:
	# Get movement input
	move_input = Input.get_axis("move_left", "move_right")
	
	# Get jump input
	jump_just_pressed = Input.is_action_just_pressed("jump")
	jump_pressed = Input.is_action_pressed("jump")
	
	# Get run input
	run_pressed = Input.is_action_pressed("run")
	
	# Buffer jump input
	if jump_just_pressed:
		jump_buffer_timer = jump_buffer_time


func _update_timers(delta: float) -> void:
	# Coyote time (grace period after leaving ground)
	if is_on_floor():
		coyote_timer = coyote_time
	else:
		coyote_timer -= delta
	
	# Jump buffer timer
	if jump_buffer_timer > 0:
		jump_buffer_timer -= delta
	
	# Gravity flip cooldown
	if gravity_flip_timer > 0:
		gravity_flip_timer -= delta


func _apply_gravity(delta: float) -> void:
	if not is_on_floor():
		if not GravityManager:
			# Fallback to default gravity if GravityManager not available
			velocity.y += 980.0 * delta
			return
		
		var gravity = GravityManager.get_gravity_vector()
		
		# Apply extra gravity when falling
		if velocity.dot(gravity.normalized()) > 0:
			gravity *= fall_gravity_multiplier
		
		velocity += gravity * delta
		
		# Cap fall speed
		var speed_in_gravity_dir = velocity.dot(gravity.normalized())
		if speed_in_gravity_dir > max_fall_speed:
			velocity = velocity.limit_length(max_fall_speed)


func _handle_movement(delta: float) -> void:
	# Determine target speed
	var target_speed = run_speed if run_pressed else move_speed
	is_running = run_pressed and abs(move_input) > 0.1
	
	# Apply movement
	if move_input != 0:
		# Accelerate
		velocity.x = move_toward(velocity.x, move_input * target_speed, acceleration * delta)
	else:
		# Apply friction
		velocity.x = move_toward(velocity.x, 0, friction * delta)


func _handle_jump() -> void:
	# Check if we can jump (on ground or coyote time)
	var can_jump = coyote_timer > 0
	
	# Check if jump was buffered
	var wants_to_jump = jump_buffer_timer > 0
	
	# Perform jump
	if wants_to_jump and can_jump:
		_perform_jump()
		jump_buffer_timer = 0
		coyote_timer = 0
	
	# Variable jump height (cut jump short if button released)
	if not jump_pressed and velocity.y < 0:
		velocity.y *= jump_cut_multiplier


func _perform_jump() -> void:
	# Jump opposite to gravity direction
	if not GravityManager:
		# Fallback: jump upward if GravityManager not available
		velocity.y = jump_velocity
	else:
		var gravity_dir = GravityManager.gravity_direction
		velocity = - gravity_dir * abs(jump_velocity)
	
	print("Jump! Velocity: ", velocity)


func _handle_abilities() -> void:
	# Gravity flip ability
	if has_gravity_flip and Input.is_action_just_pressed("gravity_flip"):
		if gravity_flip_timer <= 0:
			_activate_gravity_flip()


func _activate_gravity_flip() -> void:
	# Flip gravity
	GravityManager.flip_gravity()
	is_flipped = not is_flipped
	
	# Start cooldown
	gravity_flip_timer = gravity_flip_cooldown
	
	# Play animation
	animated_sprite.play("gravity_flip")
	
	print("Gravity flip activated!")


func _update_animation() -> void:
	# Don't interrupt gravity flip animation
	if animated_sprite.animation == "gravity_flip" and animated_sprite.is_playing():
		return
	
	# Determine animation based on state
	if not is_on_floor():
		# Airborne
		if velocity.y < 0:
			animated_sprite.play("jump")
		else:
			animated_sprite.play("fall")
	else:
		# Grounded
		if abs(velocity.x) > 10:
			if is_running:
				animated_sprite.play("run")
			else:
				animated_sprite.play("walk")
		else:
			animated_sprite.play("idle")


func _update_sprite_direction() -> void:
	# Flip sprite based on movement direction
	if move_input < 0:
		animated_sprite.flip_h = true
	elif move_input > 0:
		animated_sprite.flip_h = false
	
	# Rotate sprite based on gravity direction
	if is_flipped:
		animated_sprite.rotation_degrees = 180
	else:
		animated_sprite.rotation_degrees = 0


func _on_gravity_changed(new_direction: Vector2) -> void:
	print("Player: Gravity changed to ", new_direction)
	# Could add visual effects here


## Take damage from enemies or hazards
func take_damage(amount: int) -> void:
	print("Player took ", amount, " damage!")
	animated_sprite.play("damage")
	# TODO: Implement health system
	# TODO: Add invincibility frames
	# TODO: Add knockback


## Called when landing on ground
func _on_landed() -> void:
	animated_sprite.play("land")
	# TODO: Add landing particles
	# TODO: Add landing sound


## Unlock gravity flip ability
func unlock_gravity_flip() -> void:
	has_gravity_flip = true
	print("Gravity flip unlocked!")
	# TODO: Show UI notification
	# TODO: Play unlock effect
