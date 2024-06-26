import pygame
import random

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

leng = 16
wid = 16
grid = [[0 for i in range(wid)] for i in range(leng)]                         ##9 for mines, 10 is safe, 0 is clear, 10 temp for safety start
seen = [[0 for i in range(wid)] for i in range(leng)]                         ##0 for False 1, 1 for True, 2 for flagged
colors = [(3, 60, 210), (0, 110, 0), (200, 30, 35), (31, 66, 101),
          (160, 0, 0), (0, 100, 255), (0, 0, 0), (110, 0, 140)]
gray = (150, 150, 150)
black = (0, 0, 0)
dgray = (100, 100, 100)
flag = (255, 34, 34)
size = 32
mines = 40
game_state = "first turn"
win = False

text_font = pygame.font.SysFont("Bitmap", 25, bold = True)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def set_adj(x, y, op):
    for n in range(3):
        for m in range(3):
            if x+n-1>=0 and x+n-1<=15 and y+m-1>=0 and y+m-1<=15 and grid[x+n-1][y+m-1]!=9:
                grid[x+n-1][y+m-1] = op(grid[x+n-1][y+m-1])

def create_mines():
    for i in range(mines):
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        while grid[x][y] > 8:
            x = random.randint(0, 15)
            y = random.randint(0, 15)
        grid[x][y] = 9
        set_adj(x, y, lambda a:a+1)         

def display():
    for r in range(leng):
        for c in range(wid):
            if seen[c][r] == 1:
                if grid[c][r] == 0:
                    pygame.draw.rect(screen, gray, (c*37+6, r*37+6, size, size))
                elif grid[c][r] == 9:
                    pygame.draw.rect(screen, black, (c*37+6, r*37+6, size, size))
                elif grid[c][r] >= 1:
                    pygame.draw.rect(screen, gray, (c*37+6, r*37+6, size, size))
                    draw_text(str(grid[c][r]), text_font, colors[grid[c][r]-1], c*37+17, r*37+15)
            else:
                pygame.draw.rect(screen, dgray, (c*37+6, r*37+6, size, size))
                if seen[c][r] == 2:
                    pygame.draw.polygon(screen, flag, ((c*37+20, r*37+12),(c*37+20, r*37+22),(c*37+30, r*37+17)))
                    pygame.draw.line(screen, flag, (c*37+20, r*37+32), (c*37+20, r*37+12))

def reveal(x, y):
    if win == True:
        animate()
    elif grid[x][y] == 0:
        seen[x][y] = 1
        for n in range(3):
            for m in range(3):
                if x+n-1>=0 and x+n-1<=15 and y+m-1>=0 and y+m-1<=15 and seen[x+n-1][y+m-1] == 0:
                    reveal(x+n-1, y+m-1)
    elif grid[x][y] < 9:
        seen[x][y] = 1
    else:
        seen[x][y] = 1
        display()
        animate()    

def animate():
    global game_state
    for r in range(leng):
        for c in range(wid):
            pygame.display.flip()
            pygame.time.delay(1)
            display()
            seen[c][r] = 1
    pygame.time.delay(leng*wid+0)
    game_state = "game over"

def special(x, y):
    surr_mines = 0
    for n in range(3):
            for m in range(3):
                if x+n-1>=0 and x+n-1<=15 and y+m-1>=0 and y+m-1<=15 and seen[x+n-1][y+m-1] == 2:
                    surr_mines += 1
    if surr_mines == grid[x][y]:
        for n in range(3):
            for m in range(3):
                if x+n-1>=0 and x+n-1<=15 and y+m-1>=0 and y+m-1<=15 and seen[x+n-1][y+m-1] == 0:
                    reveal(x+n-1, y+m-1)
                    
def check_win():
    safe_cells = leng*wid-mines
    for x in range(wid):
            for y in range(leng):
                if seen[x][y] == 1 and grid[x][y] != 9 and game_state != "game over":
                    safe_cells -= 1
    return safe_cells

while running:
    mousex, mousey = pygame.mouse.get_pos()
    posx = int((mousex-3)/37)%32
    posy = int((mousey-3)/37)%32
    screen.fill((200,200,200))
    clock.tick(60)
    display()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "game over":
        if win == True:
            draw_text("WIN", pygame.font.SysFont("Bitmap", 200, bold = True), "white", 158, 200)
        else:
            draw_text("LOSE", pygame.font.SysFont("Bitmap", 200, bold = True), "white", 105, 200)
        draw_text("CLICK TO RESET", pygame.font.SysFont("Bitmap", 80, bold = True), "white", 65, 350)

    if posx >= 0 and posx <= 15 and posy >= 0 and posy <= 15:
        if pygame.mouse.get_pressed()[0]:
            if game_state == "first turn":
                set_adj(posx, posy, lambda a: 10)
                first = False
                seen = [[0 for i in range(wid)] for i in range(leng)]
                create_mines()
                set_adj(posx, posy, lambda a: a-10)
                reveal(posx, posy)
                game_state = "play"
            elif seen[posx][posy] != 2 and game_state == "play":
                    reveal(posx, posy)
                    if pygame.mouse.get_pressed()[2] and grid[posx][posy] > 0:
                        special(posx, posy)
                    if win == False:
                        win = not check_win()
            elif game_state == "game over":
                game_state = "first turn"
                grid = [[0 for i in range(wid)] for i in range(leng)]
                seen = [[0 for i in range(wid)] for i in range(leng)]
                win = False
                clock.tick(7)
        elif pygame.mouse.get_pressed()[2] and seen[posx][posy] == 0 and game_state == "play":
            seen[posx][posy] = 2
            clock.tick(7)
        elif pygame.mouse.get_pressed()[2] and seen[posx][posy] == 2 and game_state == "play":
            seen[posx][posy] = 0
            clock.tick(7)

    pygame.display.flip()

pygame.quit()
