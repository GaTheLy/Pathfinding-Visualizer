import pygame, sys
from tkinter import messagebox

pygame.init()
window_w = 600
window_h = 600

SCREEN = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Main Menu")
fps = 60
timer = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)

state = 0
con = 0

col = 30
row = 25

box_w = 20
box_h = 20

grid = []
path = []
queue = []
stack = []

# Load gambar
BG = pygame.image.load("assets/bg-1.jpg")


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.neigh = []
        self.start = False
        self.wall = False
        self.end = False
        self.queued = False
        self.visited = False
        self.prior = None
        self.box = None

    def draw(self, win, color):
        self.box = pygame.draw.rect(win, color, (self.x * box_w, self.y * box_h, box_w-2, box_h-2))

    def set_neighbours(self):
        if self.x > 0:
            self.neigh.append(grid[self.x - 1][self.y])
        if self.x < col - 1:
            self.neigh.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neigh.append(grid[self.x][self.y - 1])
        if self.y < row - 1:
            self.neigh.append(grid[self.x][self.y + 1])


def draw_menu():
    SCREEN.fill('black')
    com = 0

    djik_btn = pygame.draw.rect(SCREEN, 'gray', [225, 150, 150, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [225, 150, 150, 50], 5, 5)
    djik_text = font.render('Djikstra', True, 'black')
    SCREEN.blit(djik_text, (240, 160))

    dfs_btn = pygame.draw.rect(SCREEN, 'gray', [225, 250, 150, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [225, 250, 150, 50], 5, 5)
    dfs_text = font.render('DFS', True, 'black')
    SCREEN.blit(dfs_text, (265, 260))

    a_btn = pygame.draw.rect(SCREEN, 'gray', [225, 350, 150, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [225, 350, 150, 50], 5, 5)
    a_text = font.render('A*', True, 'black')
    SCREEN.blit(a_text, (285, 360))

    if djik_btn.collidepoint(pygame.mouse.get_pos()):
        djik_text = font.render('Djikstra', True, 'beige')
        SCREEN.blit(djik_text, (240, 160))
        if pygame.mouse.get_pressed()[0]:
            com = 1
    if dfs_btn.collidepoint(pygame.mouse.get_pos()):
        dfs_text = font.render('DFS', True, 'beige')
        SCREEN.blit(dfs_text, (265, 260))
        if  pygame.mouse.get_pressed()[0]:
            com = 2
    if a_btn.collidepoint(pygame.mouse.get_pos()):
        a_text = font.render('A*', True, 'beige')
        SCREEN.blit(a_text, (285, 360))
        if  pygame.mouse.get_pressed()[0]:
            com = 3
    return com


def draw_djik(condition):
    SCREEN.fill('black')
    com = 1
    con = condition

    check_color()

    menu_btn = pygame.draw.rect(SCREEN, 'gray', [225, 525, 150, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [225, 525, 150, 50], 5, 5)
    font_1 = pygame.font.Font('freesansbold.ttf', 24)
    a_text = font_1.render('Main Menu', True, 'black')
    SCREEN.blit(a_text, (235, 535))

    s_btn = pygame.draw.rect(SCREEN, 'dark green', [165, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [165, 525, 50, 50], 5, 5)
    s_text = font_1.render('S', True, 'white')
    SCREEN.blit(s_text, (182, 538))

    e_btn = pygame.draw.rect(SCREEN, 'maroon', [105, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [105, 525, 50, 50], 5, 5)
    s_text = font_1.render('E', True, 'white')
    SCREEN.blit(s_text, (122, 538))

    w_btn = pygame.draw.rect(SCREEN, 'black', [45, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [45, 525, 50, 50], 5, 5)
    s_text = font_1.render('W', True, 'white')
    SCREEN.blit(s_text, (59, 538))

    if menu_btn.collidepoint(pygame.mouse.get_pos()):
        menu_text = font_1.render('Main Menu', True, 'beige')
        SCREEN.blit(menu_text, (235, 535))
        if pygame.mouse.get_pressed()[0]:
            com = 0

    if s_btn.collidepoint(pygame.mouse.get_pos()):
        s_text = font_1.render('S', True, 'beige')
        SCREEN.blit(s_text, (182, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 1
            # messagebox.showinfo("cek aja", f"{con}")

    if e_btn.collidepoint(pygame.mouse.get_pos()):
        e_text = font_1.render('E', True, 'beige')
        SCREEN.blit(e_text, (122, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 2
            # messagebox.showinfo("cek aja", f"{con}")

    if w_btn.collidepoint(pygame.mouse.get_pos()):
        menu_text = font_1.render('W', True, 'beige')
        SCREEN.blit(menu_text, (58, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 3
            # messagebox.showinfo("cek aja", f"{con}")

    return com, con


def draw_dfs(condition):
    SCREEN.fill('white')

    com = 2
    con = condition

    check_color()

    menu_btn = pygame.draw.rect(SCREEN, 'gray', [225, 525, 150, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [225, 525, 150, 50], 5, 5)
    font_1 = pygame.font.Font('freesansbold.ttf', 24)
    a_text = font_1.render('Main Menu', True, 'black')
    SCREEN.blit(a_text, (235, 535))

    s_btn = pygame.draw.rect(SCREEN, 'dark green', [165, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [165, 525, 50, 50], 5, 5)
    s_text = font_1.render('S', True, 'white')
    SCREEN.blit(s_text, (182, 538))

    e_btn = pygame.draw.rect(SCREEN, 'maroon', [105, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [105, 525, 50, 50], 5, 5)
    s_text = font_1.render('E', True, 'white')
    SCREEN.blit(s_text, (122, 538))

    w_btn = pygame.draw.rect(SCREEN, 'black', [45, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [45, 525, 50, 50], 5, 5)
    s_text = font_1.render('W', True, 'white')
    SCREEN.blit(s_text, (59, 538))

    if menu_btn.collidepoint(pygame.mouse.get_pos()):
        menu_text = font_1.render('Main Menu', True, 'beige')
        SCREEN.blit(menu_text, (235, 535))
        if pygame.mouse.get_pressed()[0]:
            com = 0

    if s_btn.collidepoint(pygame.mouse.get_pos()):
        s_text = font_1.render('S', True, 'beige')
        SCREEN.blit(s_text, (182, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 1
            # messagebox.showinfo("cek aja", f"{con}")

    if e_btn.collidepoint(pygame.mouse.get_pos()):
        e_text = font_1.render('E', True, 'beige')
        SCREEN.blit(e_text, (122, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 2
            # messagebox.showinfo("cek aja", f"{con}")

    if w_btn.collidepoint(pygame.mouse.get_pos()):
        menu_text = font_1.render('W', True, 'beige')
        SCREEN.blit(menu_text, (58, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 3
            # messagebox.showinfo("cek aja", f"{con}")

    return com, con


def draw_a(condition):
    SCREEN.fill('pink')

    com = 3
    con = condition

    check_color()

    menu_btn = pygame.draw.rect(SCREEN, 'gray', [225, 525, 150, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [225, 525, 150, 50], 5, 5)
    font_1 = pygame.font.Font('freesansbold.ttf', 24)
    a_text = font_1.render('Main Menu', True, 'black')
    SCREEN.blit(a_text, (235, 535))

    s_btn = pygame.draw.rect(SCREEN, 'dark green', [165, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [165, 525, 50, 50], 5, 5)
    s_text = font_1.render('S', True, 'white')
    SCREEN.blit(s_text, (182, 538))

    e_btn = pygame.draw.rect(SCREEN, 'maroon', [105, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [105, 525, 50, 50], 5, 5)
    s_text = font_1.render('E', True, 'white')
    SCREEN.blit(s_text, (122, 538))

    w_btn = pygame.draw.rect(SCREEN, 'black', [45, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [45, 525, 50, 50], 5, 5)
    s_text = font_1.render('W', True, 'white')
    SCREEN.blit(s_text, (59, 538))

    if menu_btn.collidepoint(pygame.mouse.get_pos()):
        menu_text = font_1.render('Main Menu', True, 'beige')
        SCREEN.blit(menu_text, (235, 535))
        if pygame.mouse.get_pressed()[0]:
            com = 0

    if s_btn.collidepoint(pygame.mouse.get_pos()):
        s_text = font_1.render('S', True, 'beige')
        SCREEN.blit(s_text, (182, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 1
            # messagebox.showinfo("cek aja", f"{con}")

    if e_btn.collidepoint(pygame.mouse.get_pos()):
        e_text = font_1.render('E', True, 'beige')
        SCREEN.blit(e_text, (122, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 2
            # messagebox.showinfo("cek aja", f"{con}")

    if w_btn.collidepoint(pygame.mouse.get_pos()):
        menu_text = font_1.render('W', True, 'beige')
        SCREEN.blit(menu_text, (58, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 3
            # messagebox.showinfo("cek aja", f"{con}")

    return com, con


def check_color():
    for i in range(col):
        for j in range(row):
            # print(f'{i} {j}')
            box = grid[i][j]
            box.draw(SCREEN, (100, 100, 100))

            if box.queued:
                box.draw(SCREEN, (200, 0, 0))
            if box.visited:
                box.draw(SCREEN, (0, 200, 0))
            if box in path:
                box.draw(SCREEN, (0, 0, 200))

            if box.start:
                box.draw(SCREEN, (0, 200, 200))
            if box.wall:
                box.draw(SCREEN, (52, 52, 52))
            if box.end:
                box.draw(SCREEN, (200, 200, 0))


# Mengisi Grid
for i in range(col):
    arr = []
    for j in range(row):
        arr.append(Box(i, j))
    grid.append(arr)

# Mengisi Neighbour
for i in range(col):
    for j in range(row):
        grid[i][j].set_neighbours()


def check_collide(con):
    for l in grid:
        for box in l:
            if box.box.collidepoint(pygame.mouse.get_pos()):
                box.draw(SCREEN, (169, 169, 169))
                if pygame.mouse.get_pressed()[0]:
                    if con == 1:
                        box.start = not box.start
                    elif con == 2:
                        box.end = not box.end
                    elif con == 3:
                        box.wall = not box.wall
                    # messagebox.showinfo("cek aja", f"{con} box {box.x}, {box.y}")


run = True
while run:

    timer.tick(fps)

    if state == 0:
        state = draw_menu()
    if state == 1:
        state, con = draw_djik(con)
        check_collide(con)
    if state == 2:
        state, con = draw_dfs(con)
    if state == 3:
        state, con = draw_a(con)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

