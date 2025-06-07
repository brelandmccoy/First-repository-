import turtle
import time

# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=1000, height=600)
sc.tracer(0) # Turns off screen updates

# Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0) # Animation speed, not movement speed
left_pad.shape("square")
left_pad.color("black")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup() # Lifts the pen so it doesn't draw lines
left_pad.goto(-400, 0) # Starting position for left paddle

# Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0) # Animation speed
right_pad.shape("square")
right_pad.color("black")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400, 0) # Starting position for right paddle

# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(0) # Animation speed, set to 0 for fastest
hit_ball.shape("circle")
hit_ball.color("blue")
hit_ball.penup()
hit_ball.goto(0, 0) # Starting position for the ball
hit_ball.dx = 5 # Ball's horizontal movement speed
hit_ball.dy = -5 # Ball's vertical movement speed

# Initialize the score
left_player = 0
right_player = 0

# Displays the score
sketch = turtle.Turtle()
sketch.speed(0) # Animation speed
sketch.color("blue")
sketch.penup()
sketch.hideturtle() # Hides the turtle icon
sketch.goto(0, 260) # Position for the score display
sketch.write("Left_player: 0     Right_player: 0",
             align="center", font=("Courier", 24, "normal"))

# Functions to move paddles
def paddleaup():
    y = left_pad.ycor()
    # Limit paddle movement to stay within screen boundaries
    if y < 250:
        y += 20
        left_pad.sety(y)

def paddleadown():
    y = left_pad.ycor()
    # Limit paddle movement to stay within screen boundaries
    if y > -240:
        y -= 20
        left_pad.sety(y)

def paddlebup():
    y = right_pad.ycor()
    # Limit paddle movement to stay within screen boundaries
    if y < 250:
        y += 20
        right_pad.sety(y)

def paddlebdown():
    y = right_pad.ycor()
    # Limit paddle movement to stay within screen boundaries
    if y > -240:
        y -= 20
        right_pad.sety(y)

# Keyboard bindings
sc.listen() # Listen for keyboard input
sc.onkeypress(paddleaup, "w") # 'w' key for left paddle up
sc.onkeypress(paddleadown, "s") # 's' key for left paddle down
sc.onkeypress(paddlebup, "Up") # Up arrow key for right paddle up
sc.onkeypress(paddlebdown, "Down") # Down arrow key for right paddle down

# Main game loop
while True:
    sc.update() # Manually update the screen
    time.sleep(0.01) # Add a small delay for smoother animation

    # Move the ball
    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    # Checking borders for top and bottom walls
    # Top wall collision
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1 # Reverse vertical direction

    # Bottom wall collision (CORRECTED: changed > to <)
    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1 # Reverse vertical direction

    # Checking for scoring (left and right walls)
    # Right side score
    if hit_ball.xcor() > 500:
        hit_ball.goto(0, 0) # Reset ball to center
        # hit_ball.dy *= -1 # REMOVED: No need to reverse dy here, ball resets
        left_player += 1 # Increment left player's score
        sketch.clear() # Clear previous score
        sketch.write("Left_player: {}     Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    # Left side score
    if hit_ball.xcor() < -500:
        hit_ball.goto(0, 0) # Reset ball to center
        # hit_ball.dy *= -1 # REMOVED: No need to reverse dy here, ball resets
        right_player += 1 # Increment right player's score
        sketch.clear() # Clear previous score
        sketch.write("Left_player: {}     Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))

    # Paddle ball collision
    # Right paddle collision
    # Check if ball is within horizontal range of right paddle
    # And if ball is within vertical range of right paddle
    if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) and \
            (hit_ball.ycor() < right_pad.ycor() + 60 and hit_ball.ycor() > right_pad.ycor() - 60):
        hit_ball.setx(360) # Move ball just outside the paddle to prevent sticking
        hit_ball.dx *= -1 # Reverse horizontal direction

    # Left paddle collision
    # Check if ball is within horizontal range of left paddle
    # And if ball is within vertical range of left paddle
    if (hit_ball.xcor() < -360 and hit_ball.xcor() > -370) and \
            (hit_ball.ycor() < left_pad.ycor() + 50 and hit_ball.ycor() > left_pad.ycor() - 50):
        hit_ball.setx(-360) # Move ball just outside the paddle to prevent sticking
        hit_ball.dx *= -1 # Reverse horizontal direction
