extends RigidBody2D

var is_being_pollinated = false
var is_pollinated = false
@export var point_value: int = 5

# Called when the node enters the scene tree for the first time.
func _ready():
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

# delete flower after exits the screen
func _on_visible_on_screen_notifier_2d_screen_exited():
	queue_free()

func _on_pollinate_area_2d_body_entered(body):
	#print("pollinate area entered")
	is_being_pollinated = true
	if not is_pollinated:
		$AnimatedSprite2D.play("pollinate")

func _on_pollinate_area_2d_body_exited(body):
	#print("pollinate area exited")
	is_being_pollinated = false
	if not is_pollinated:
		$AnimatedSprite2D.pause()

func _on_animated_sprite_2d_animation_finished():
	is_pollinated = true
	GameState.increase_score(point_value)
