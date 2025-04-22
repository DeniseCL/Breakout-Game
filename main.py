import turtle

# Screen setup
win = turtle.Screen()
win.title("Breakout Game")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Globals
score = 0
high_score = 0


# Play Again Button
play_button = turtle.Turtle()
play_button.shape("square")
play_button.color("white")
play_button.shapesize(stretch_wid=1.5, stretch_len=6)
play_button.penup()
play_button.goto(0, -50)
play_button.hideturtle()

# Play Again Button Text
button_text = turtle.Turtle()
button_text.hideturtle()
button_text.color("white")
button_text.penup()
button_text.goto(0, -55)

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.speed(1)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, -230)
ball.dx = 2
ball.dy = 2

# Score Display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 260)


def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}    High Score: {high_score}",
                        align="left", font=("Courier", 16, "normal"))


# Initial score display
update_score()

# End message
end_message = turtle.Turtle()
end_message.hideturtle()
end_message.penup()
end_message.color("white")
end_message.goto(0, 0)

# Bricks
bricks = []

colors = ["red", "orange", "green", "yellow"]

for row in range(4):
    for col in range(-7, 8):
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.color(colors[row])
        brick.shapesize(stretch_wid=1, stretch_len=3)
        brick.penup()
        brick.goto(col * 60, 250 - row * 30)
        bricks.append(brick)


# Paddle movement
def paddle_left():
    x = paddle.xcor()
    if x > -350:
        paddle.setx(x - 40)


def paddle_right():
    x = paddle.xcor()
    if x < 350:
        paddle.setx(x + 40)


def show_play_button():
    play_button.showturtle()
    button_text.write("Play Again", align="center", font=("Courier", 12, "normal"))
    win.onscreenclick(check_click)


def check_click(x, y):
    if -60 < x < 60 and -65 < y < -35:
        play_button.clear()
        button_text.clear()
        play_button.hideturtle()
        win.onscreenclick(None)
        restart_game()


def restart_game():
    global score, high_score
    if score > high_score:
        high_score = score
    score = 0
    update_score()
    end_message.clear()
    play_button.clear()
    play_button.hideturtle()
    button_text.clear()

    # Reset paddle and ball
    paddle.goto(0, -250)
    ball.goto(0, -230)
    ball.dx = 2
    ball.dy = 2

    # Reset bricks
    for brick in bricks:
        brick.showturtle()

    game_loop()


# Main game loop
def game_loop():
    global score
    game_running = True

    while game_running:
        win.update()
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Wall collisions
        if ball.xcor() > 390 or ball.xcor() < -390:
            ball.dx *= -1
        if ball.ycor() > 290:
            ball.dy *= -1

        # ON Game Over
        if ball.ycor() < -290:
            end_message.write("Game Over", align="center", font=("Courier", 24, "bold"))
            show_play_button()
            return

        # Paddle collision
        if -240 < ball.ycor() < -220 and (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
            ball.dy *= -1

        # Brick collision
        for brick in bricks:
            if brick.isvisible() and abs(ball.xcor() - brick.xcor()) < 50 and abs(ball.ycor() - brick.ycor()) < 20:
                brick.hideturtle()
                ball.dy *= -1
                score += 10
                update_score()
                break  # Check win right after

        # Win condition
        if all(not b.isvisible() for b in bricks):
            end_message.write("You Win!", align="center", font=("Courier", 24, "bold"))
            show_play_button()
            return


# Key bindings
win.listen()
win.onkeypress(paddle_left, "Left")
win.onkeypress(paddle_right, "Right")

# Start the game
game_loop()
win.mainloop()
