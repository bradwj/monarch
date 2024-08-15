extends Node

var screen_size
@export var flower_scene: PackedScene
var default_flower_spawn_position: Vector2

func _ready():
	screen_size = get_viewport().size
	calc_default_flower_spawn_position()
	
func _on_player_game_over():
	print("Game over!")
	GameState.game_over()


func new_game():
	print("Starting new game")
	GameState.reset()


func calc_default_flower_spawn_position():
	var flower: Node = flower_scene.instantiate()
	var flower_spawn_position_x = screen_size.x
	var ground_size = $Ground.get_node("CollisionShape2D").get_shape().size
	var flower_size = flower.get_node("CollisionShape2D").get_shape().size
	var flower_spawn_position_y = \
		$Ground.position.y - ground_size.y - (abs(flower_size.y - ground_size.y) / 2)
	
	default_flower_spawn_position = Vector2(flower_spawn_position_x, flower_spawn_position_y)
	flower.queue_free()
	

func _on_spawn_flower_timer_timeout():
	var flower: Node = flower_scene.instantiate()

	var position_offset = Vector2(
		randi_range(100, 200),
		0
	)
	var flower_spawn_position = default_flower_spawn_position + position_offset
	flower.position = flower_spawn_position
	
	add_child(flower)

