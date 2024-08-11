extends StaticBody2D

var ground_width: float

func _ready() -> void:
	# Get the width of the ground sprite (assuming it's a child of the StaticBody2D)
	ground_width = $Sprite2D.texture.get_width()
	print(ground_width)

func _process(delta: float) -> void:
	# Use the global scroll speed
	position.x -= GameState.scroll_speed * delta

	# Check if the ground has moved out of the screen to the left
	if position.x <= 0:
		# Reset the position to create a loop effect
		position.x = ground_width / 2
