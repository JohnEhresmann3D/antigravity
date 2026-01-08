extends Area2D
class_name DamageComponent
## Deals damage to entities that enter this area

signal hit_target(target: Node, damage_dealt: int)
signal hit_blocked(target: Node)

@export_group("Damage")
@export var damage: int = 1
@export var damage_groups: Array[String] = ["player"]

@export_group("Knockback")
@export var apply_knockback: bool = true
@export var knockback_force: float = 200.0

@export_group("Behavior")
@export var one_shot: bool = false
@export var destroy_on_hit: bool = false

var has_hit: bool = false


func _ready() -> void:
	body_entered.connect(_on_body_entered)
	area_entered.connect(_on_area_entered)


func _on_body_entered(body: Node) -> void:
	"""Handle collision with a body"""
	if one_shot and has_hit:
		return
	
	# Check if target is in damage groups
	for group in damage_groups:
		if body.is_in_group(group):
			_deal_damage_to_node(body)
			break


func _on_area_entered(area: Node) -> void:
	"""Handle collision with another area (for hitboxes)"""
	if one_shot and has_hit:
		return
	
	# Check if the area's parent is in damage groups
	var parent = area.get_parent()
	if parent:
		for group in damage_groups:
			if parent.is_in_group(group):
				_deal_damage_to_node(parent)
				break


func _deal_damage_to_node(target: Node) -> void:
	"""Deal damage to a target node"""
	# Try to find HealthComponent by name first, then by type
	var health: HealthComponent = target.get_node_or_null("HealthComponent")
	
	if not health:
		# Try to find by iterating children
		for child in target.get_children():
			if child is HealthComponent:
				health = child
				break
	
	if health:
		# Check if target is invincible
		if health.is_invincible():
			hit_blocked.emit(target)
			return
		
		# Deal damage
		health.take_damage(damage, get_parent())
		has_hit = true
		hit_target.emit(target, damage)
		
		# Apply knockback if enabled
		if apply_knockback and target is CharacterBody2D:
			var direction = (target.global_position - global_position).normalized()
			
			# Check if target has MovementComponent
			var movement: MovementComponent = target.get_node_or_null("MovementComponent")
			if movement:
				movement.apply_impulse(direction * knockback_force)
			else:
				# Fallback: apply directly to velocity
				target.velocity += direction * knockback_force
		
		# Destroy parent if configured
		if destroy_on_hit:
			get_parent().queue_free()
	else:
		# No health component found, still emit signal
		hit_target.emit(target, 0)


func reset() -> void:
	"""Reset one-shot state"""
	has_hit = false


func set_damage(new_damage: int) -> void:
	"""Change damage value"""
	damage = new_damage
