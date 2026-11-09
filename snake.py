import tkinter
import random

ROWS = 20
COLS = 20
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Janela
window = tkinter.Tk()
window.title("Jogo da cobrinha")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth= 0, highlightthickness=0)
canvas.pack()
window.update()


# Centralizar
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


#Init
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = []
gameover = False
vel_x = 0
vel_y = 0
score = 0

def change_direction(e):
    button = e.keysym

    global vel_x, vel_y, gameover

    if gameover:
        return

    if button == "Up" and vel_y != 1:
        vel_x = 0
        vel_y = -1

    elif button == "Down" and vel_y != -1:
        vel_x = 0
        vel_y = 1

    elif button == "Left" and vel_x != 1:
        vel_x = -1
        vel_y = 0

    elif button == "Right" and vel_x != -1:
        vel_x = 1
        vel_y = 0

def move():
    global snake, gameover, food, snake_body, score

    if gameover:
        return

    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        gameover = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            gameover = True
            return

    # colisão
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    

    for i in range(len(snake_body) -1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y 

    snake.x += vel_x * TILE_SIZE
    snake.y += vel_y * TILE_SIZE
 

def draw():
    global snake, food, snake_body, gameover, score
    move()

    canvas.delete("all")

    # comida
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")

    # cobra
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green")

    if (gameover):
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text=f"GAME OVER: {score}", fill= "white")
    else:
        canvas.create_text(30, 20, font="Arial 12", text=f"Score: {score}", fill= "white")
    
    window.after(100, draw)

window.bind("<KeyRelease>", change_direction)

draw()
window.mainloop()
