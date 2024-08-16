extends Node

var screen_size

func _ready():
	screen_size = get_viewport().size
	
func _on_player_game_over():
	print("Game over!")
	GameState.game_over()


func new_game():
	print("Starting new game")
	GameState.reset()

