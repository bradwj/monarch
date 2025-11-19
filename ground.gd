extends StaticBody2D

func _ready() -> void:
	pass

func _physics_process(delta: float) -> void:
	constant_linear_velocity.x = -GameState.scroll_speed
	$Sprite2D.position.x -= GameState.scroll_speed * delta
	
	if $Sprite2D.position.x <= -$Sprite2D.texture.get_size().x / 2:
		$Sprite2D.position.x += $Sprite2D.texture.get_size().x / 2
