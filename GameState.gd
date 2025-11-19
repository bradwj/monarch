extends Node

var initial_scroll_speed: float = 150.0
var scroll_speed: float = initial_scroll_speed
var time_elapsed: float = 0.0
var speed_increase_rate: float = 10.0
var is_game_over: bool = false
var score: int = 0

#func _ready():
	#pass

func _process(delta: float):
	time_elapsed += delta
	scroll_speed += speed_increase_rate * delta


func game_over():
	print("GameState: game_over()")
	set_process(false)
	is_game_over = true
	scroll_speed = 0


func reset():
	print("GameState: reset()")
	set_process(true)
	scroll_speed = initial_scroll_speed
	is_game_over = false
	score = 0
	

func increase_score(point_value: int):
	score += point_value
	print(score)
