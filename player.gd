extends CharacterBody2D

signal game_over

@export var speed = Vector2(300, 500)
@export var gravity = 100
var screen_size

var is_on_ground = false
var screen_border_tolerance = Vector2(100, 100)

# Called when the node enters the scene tree for the first time.
func _ready():
	screen_size = get_viewport_rect().size

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	velocity = Vector2.ZERO
	if Input.is_action_pressed("move_right"):
		velocity.x += 1
	if Input.is_action_pressed("move_left"):
		velocity.x -= 1
	if Input.is_action_pressed("move_down") and not is_on_ground:
		velocity.y += 1
	if Input.is_action_pressed("move_up"):
		velocity.y -= 1
	
	if velocity.length() > 0:
		velocity = velocity.normalized() * speed
	
	velocity.y += gravity
	
	# process collisions
	var collision: KinematicCollision2D = move_and_collide(velocity * delta)
	if collision:
		var collider = collision.get_collider()
		if collider.name == "Ground":
			is_on_ground = true
			# Move the character backwards at the global scroll speed
			velocity.x -= GameState.scroll_speed
	else:
		is_on_ground = false
	
	# Apply the final movement
	move_and_slide()

	# detect when leaves left side of screen
	if position.x < -screen_border_tolerance.x and not GameState.is_game_over:
		set_physics_process(false) # disable player movement
		game_over.emit()
	
	position = position.clamp(
		Vector2.ZERO - screen_border_tolerance, 
		screen_size + screen_border_tolerance
	)
	
	
