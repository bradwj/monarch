extends Node

var screen_size
@export var flower_scene: PackedScene


func _ready():
	screen_size = get_viewport().size

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func spawn_flower():
	var flower: Node = flower_scene.instantiate()

	var position_offset = Vector2(
		randi_range(100, 200), 0
	)
	var flower_spawn_position = $FlowerSpawnPoint.position + position_offset
	flower.position = flower_spawn_position
	
	add_child(flower)
