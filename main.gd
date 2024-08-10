extends Node

@export var initial_scroll_speed = 200
var score = 0
var ground_scroll = 0

var scroll_speed = initial_scroll_speed
var scroll_speed_delta = 1 # amount to increase scroll speed
var scroll_incr_freq = 100 # scroll speed increases every 100 points earned


# Called when the node enters the scene tree for the first time.
func _ready():
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var velocity = scroll_speed * delta
	var ground_sprite = get_node("Ground/Sprite2D")
	ground_sprite.position.x -= velocity
	if abs(ground_sprite.position.x) > $Background.size.x:
		ground_sprite.position.x = 0
	
	
