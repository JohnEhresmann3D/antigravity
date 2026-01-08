extends Node
class_name HealthComponent
## Manages entity health, damage, healing, and death

signal health_changed(current: int, maximum: int)
signal died
signal damaged(amount: int, attacker: Node)
signal healed(amount: int)

@export_group("Health")
@export var max_health: int = 100
@export var start_at_max: bool = true

@export_group("Invincibility")
@export var invincible: bool = false
@export var invincibility_duration: float = 0.5

var current_health: int
var invincibility_timer: float = 0.0
var is_alive: bool = true


func _ready() -> void:
	current_health = max_health if start_at_max else 0
	health_changed.emit(current_health, max_health)


func _process(delta: float) -> void:
	if invincibility_timer > 0:
		invincibility_timer -= delta


func take_damage(amount: int, attacker: Node = null) -> void:
	"""Deal damage to this entity"""
	if not is_alive or invincible or invincibility_timer > 0:
		return
	
	# Reject negative damage
	if amount <= 0:
		return
	
	var actual_damage = min(amount, current_health)
	current_health -= actual_damage
	
	damaged.emit(actual_damage, attacker)
	health_changed.emit(current_health, max_health)
	
	if current_health <= 0:
		is_alive = false
		died.emit()


func heal(amount: int) -> void:
	"""Heal this entity"""
	if not is_alive:
		return
	
	# Reject negative healing
	if amount <= 0:
		return
	
	var actual_heal = min(amount, max_health - current_health)
	
	# Only emit signals if actually healed
	if actual_heal > 0:
		current_health += actual_heal
		healed.emit(actual_heal)
		health_changed.emit(current_health, max_health)


func set_invincible(duration: float) -> void:
	"""Make entity invincible for a duration"""
	invincibility_timer = max(invincibility_timer, duration)


func is_invincible() -> bool:
	"""Check if currently invincible"""
	return invincible or invincibility_timer > 0


func get_health_percent() -> float:
	"""Get health as percentage (0.0 to 1.0)"""
	if max_health == 0:
		return 0.0
	return float(current_health) / float(max_health)


func set_health(value: int) -> void:
	"""Directly set health value"""
	current_health = clamp(value, 0, max_health)
	health_changed.emit(current_health, max_health)
	
	if current_health <= 0 and is_alive:
		is_alive = false
		died.emit()


func revive(health_amount: int = -1) -> void:
	"""Revive a dead entity"""
	is_alive = true
	if health_amount < 0:
		current_health = max_health
	else:
		current_health = clamp(health_amount, 1, max_health)
	health_changed.emit(current_health, max_health)


func set_max_health(new_max: int) -> void:
	"""Set maximum health and scale current health proportionally"""
	if new_max <= 0:
		return
	
	var health_percent = get_health_percent()
	max_health = new_max
	current_health = int(health_percent * max_health)
	health_changed.emit(current_health, max_health)
