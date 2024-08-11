extends Node

@export var initial_scroll_speed: float = 200.0
@export var scroll_speed = initial_scroll_speed
var time_elapsed: float = 0.0
@export var speed_increase_rate: float = 10.0

func _process(delta: float) -> void:
	time_elapsed += delta
	scroll_speed += speed_increase_rate * delta
