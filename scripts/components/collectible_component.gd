extends Area2D
class_name CollectibleComponent
## Handles collectible pickup behavior and scoring

signal collected(collector: Node)
signal collection_failed(collector: Node, reason: String)

@export_group("Collectible")
@export var collectible_type: String = "coin"
@export var point_value: int = 10
@export var auto_collect: bool = true

@export_group("Collection")
@export var collector_groups: Array[String] = ["player"]
@export var destroy_on_collect: bool = true
@export var collection_delay: float = 0.0

var is_collected: bool = false
var collection_timer: float = 0.0


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _process(delta: float) -> void:
	if collection_timer > 0:
		collection_timer -= delta
		if collection_timer <= 0:
			_complete_collection()


func _on_body_entered(body: Node) -> void:
	"""Handle collision with potential collector"""
	if is_collected or not auto_collect:
		return
	
	# Check if collector is in allowed groups
	for group in collector_groups:
		if body.is_in_group(group):
			collect(body)
			break


func collect(collector: Node) -> void:
	"""Manually trigger collection"""
	if is_collected:
		collection_failed.emit(collector, "already_collected")
		return
	
	is_collected = true
	
	if collection_delay > 0:
		collection_timer = collection_delay
		# Could play collection animation here
	else:
		_complete_collection(collector)


func _complete_collection(collector: Node = null) -> void:
	"""Complete the collection process"""
	collected.emit(collector)
	
	# Add score if GameManager exists
	if has_node("/root/GameManager"):
		get_node("/root/GameManager").add_score(point_value)
	
	# Destroy parent entity if configured
	if destroy_on_collect:
		get_parent().queue_free()


func get_type() -> String:
	"""Get collectible type"""
	return collectible_type


func get_value() -> int:
	"""Get point value"""
	return point_value
