extends Node

@export var initial_scroll_speed: float = 200.0
#@export var scroll_speed = initial_scroll_speed
@export var scroll_speed = 0.0
var time_elapsed: float = 0.0
@export var speed_increase_rate: float = 10.0

@export var is_game_over = false

func _ready():
	scroll_speed = initial_scroll_speed

func _process(delta: float):
	time_elapsed += delta
	scroll_speed += speed_increase_rate * delta
	

func _on_player_game_over():
	set_process(false)
	is_game_over = true
	scroll_speed = 0
	print("Game over!")
	print("scroll_speed=",scroll_speed)
	
