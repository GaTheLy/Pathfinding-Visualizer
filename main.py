import pygame
import tkinter

# Set window width and height
pygame.init()
window_w = 600
window_h = 600

SCREEN = pygame.display.set_mode((window_w, window_h))

fps = 90
timer = pygame.time.Clock()

font = pygame.font.Font(None, 46)

# State (berada di page mana) & con untuk kondisi node saat dipencet
state = 0
con = 0

# Column dan row dari grid
col = 30
row = 25

# Width and height dari box
box_w = 20
box_h = 20

# Grid = List 2D berisi objek Box
grid = []
# Path = Jalan dari start node ke end node
path = []

searching = False
nemu = False
cur = None
queue = []
stack = []

neigh_btn = []
n_btn_x = []
n_btn_y = []
neighbours = [True] * 9
# print(neighbours)

active = False
weight = ''


class Box:
    def __init__(self, i, j):
        # Posisi di grid (grid[x][y])
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
        self.weight = 1
        self.distance = float('inf')
        self.text = ''

    def draw(self, win, color):
        self.box = pygame.draw.rect(win, color, (self.x * box_w, self.y * box_h, box_w-2, box_h-2))
        if 1 < self.weight < 10:
            temp_txt = pygame.font.Font(None, 16).render(self.text, True, 'black')
            SCREEN.blit(temp_txt, (self.x * box_w + 5, self.y * box_h + 4))
        elif self.weight >= 10:
            temp_txt = pygame.font.Font(None, 16).render(self.text, True, 'black')
            SCREEN.blit(temp_txt, (self.x * box_w + 3, self.y * box_h + 4))

    def reset_neighbours(self):
        self.neigh = []

    def set_neighbours(self):
        # Kiri atas
        if (self.x > 0 and self.y > 0) and neighbours[0]:
            self.neigh.append(grid[self.x - 1][self.y - 1])
        # Atas
        if self.y > 0 and neighbours[3]:
            self.neigh.append(grid[self.x][self.y - 1])
        # Kanan atas
        if (self.x < col - 1 and self.y > 0) and neighbours[6]:
            self.neigh.append(grid[self.x + 1][self.y - 1])
        # Kiri
        if self.x > 0 and neighbours[1]:
            self.neigh.append(grid[self.x - 1][self.y])
        # Kanan
        if self.x < col - 1 and neighbours[7]:
            self.neigh.append(grid[self.x + 1][self.y])
        # Kanan bawah
        if (self.x < col - 1 and self.y < row - 1) and neighbours[8]:
            self.neigh.append(grid[self.x + 1][self.y + 1])
        # Bawah
        if self.y < row - 1 and neighbours[5]:
            self.neigh.append(grid[self.x][self.y + 1])
        # Kiri bawah
        if (self.x > 0 and self.y < row - 1) and neighbours[2]:
            self.neigh.append(grid[self.x - 1][self.y+1])


def draw_menu():
    pygame.display.set_caption("Main Menu")
    SCREEN.fill('black')
    # com ini temp variable buat state
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
    a_text = font.render('Quit', True, 'black')
    SCREEN.blit(a_text, (265, 360))

    if djik_btn.collidepoint(pygame.mouse.get_pos()):
        # Hover
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        djik_text = font.render('Djikstra', True, 'beige')
        SCREEN.blit(djik_text, (240, 160))
        if pygame.mouse.get_pressed()[0]:
            # Click
            com = 1
    elif dfs_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        dfs_text = font.render('DFS', True, 'beige')
        SCREEN.blit(dfs_text, (265, 260))
        if  pygame.mouse.get_pressed()[0]:
            com = 2
    elif a_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        pygame.draw.rect(SCREEN, 'red', [225, 350, 150, 50], 5, 5)
        a_text = font.render('Quit', True, 'red')
        SCREEN.blit(a_text, (265, 360))
        if  pygame.mouse.get_pressed()[0]:
            com = 3
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    return com


def draw_djik(condition, search, queue, cur, nemu, path, active, weight, neighbours):
    pygame.display.set_caption("Dijkstra")
    # if queue:
    #     for box in queue:
    #         print(box.x, box.y)

    ready = None

    SCREEN.fill('#343434')
    com = 1
    con = condition

    check_color()

    font_1 = pygame.font.Font(None, 14)
    dis_n_btn = font_1.render('Set Neighbours', True, 'white')
    SCREEN.blit(dis_n_btn, (512, 505))

    inp_col = pygame.Color('gray')
    if active:
        inp_col = pygame.Color('white')

    input_w_btn = pygame.draw.rect(SCREEN, "indigo", [420, 525, 50, 20], 0, 5)
    pygame.draw.rect(SCREEN, "dark grey", [420, 525, 50, 20], 3, 5)

    input_w_space = pygame.draw.rect(SCREEN, inp_col, [420, 550, 50, 20], 1, 5)
    weight_text = font_1.render(weight, True, 'white')
    SCREEN.blit(weight_text, (input_w_space.x + 19, input_w_space.y + 5))

    dis_n_btn = font_1.render('Weight', True, 'white')
    SCREEN.blit(dis_n_btn, (428, 530))

    # Dalem
    menu_btn = pygame.draw.rect(SCREEN, 'gray', [225, 525, 150, 50], 0, 5)
    # Border
    pygame.draw.rect(SCREEN, 'dark gray', [225, 525, 150, 50], 5, 5)
    font_1 = pygame.font.Font(None, 36)
    # Text
    a_text = font_1.render('Main Menu', True, 'black')
    # Posisi Text
    SCREEN.blit(a_text, (235, 535))

    s_btn = pygame.draw.rect(SCREEN, "#FFD643", [165, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [165, 525, 50, 50], 5, 5)
    s_text = font_1.render('S', True, 'black')
    SCREEN.blit(s_text, (182, 538))

    e_btn = pygame.draw.rect(SCREEN, "#FF8800", [105, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [105, 525, 50, 50], 5, 5)
    s_text = font_1.render('E', True, 'black')
    SCREEN.blit(s_text, (122, 538))

    w_col = pygame.Color('black')
    if con == 4:
        w_col = pygame.Color('red')
    w_btn = pygame.draw.rect(SCREEN, w_col, [45, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [45, 525, 50, 50], 5, 5)
    s_text = font_1.render('W', True, 'white')
    SCREEN.blit(s_text, (59, 538))

    # print(len(neigh_btn), len(neighbours), print(neighbours))

    if menu_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        menu_text = font_1.render('Main Menu', True, 'beige')
        SCREEN.blit(menu_text, (235, 535))
        if pygame.mouse.get_pressed()[0]:
            # State berubah
            com = 0

    elif s_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        s_text = font_1.render('S', True, 'beige')
        SCREEN.blit(s_text, (182, 538))
        if pygame.mouse.get_pressed()[0]:
            # Condition berubah
            con = 1
            # messagebox.showinfo("cek aja", f"{con}")

    elif e_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        e_text = font_1.render('E', True, 'beige')
        SCREEN.blit(e_text, (122, 538))
        if pygame.mouse.get_pressed()[0]:
            con = 2
            # messagebox.showinfo("cek aja", f"{con}")

    elif w_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        menu_text = font_1.render('W', True, 'beige')
        SCREEN.blit(menu_text, (58, 538))
        if pygame.mouse.get_pressed()[0]:
            if con == 3:
                con = 4
            else:
                con = 3
            # messagebox.showinfo("cek aja", f"{con}")

    elif input_w_btn.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if pygame.mouse.get_pressed()[0]:
            con = 5

    elif input_w_space.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if input_w_space.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            active = True
    else:
        if pygame.mouse.get_pressed()[0]:
            active = False

    # print(active)
    # print(weight)
    # print(con)

    if nemu and not cur.start:
        path.append(cur)
        cur = cur.prior

    if not search:
        ready, queue, stack, end_node = check_ready()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key in range(48, 59) and len(weight) < 2:
                    weight += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    weight = weight[:-1]
            print(event.type)
            print(event.key)
            if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and ready:
                path = reset_path_etc()
                # print("test hemm")
                assign_neighbours()
                search = True
                nemu = False
            if event.key == pygame.K_w:
                print("Test W")
                if con == 3:
                    con = 4
                else:
                    con = 3
            if event.key == pygame.K_s:
                con = 1
            if event.key == pygame.K_e:
                con = 2
            if event.key == pygame.K_b:
                con = 5
            if event.key == pygame.K_TAB:
                active = not active
            if event.key == pygame.K_KP1:
                neighbours[2] = not neighbours[2]
            if event.key == pygame.K_KP2:
                neighbours[5] = not neighbours[5]
            if event.key == pygame.K_KP3:
                neighbours[8] = not neighbours[8]
            if event.key == pygame.K_KP4:
                neighbours[1] = not neighbours[1]
            if event.key == pygame.K_KP5:
                pass
            if event.key == pygame.K_KP6:
                neighbours[7] = not neighbours[7]
            if event.key == pygame.K_KP7:
                neighbours[0] = not neighbours[0]
            if event.key == pygame.K_KP8:
                neighbours[3] = not neighbours[3]
            if event.key == pygame.K_KP9:
                neighbours[6] = not neighbours[6]
            if event.key == pygame.K_c:
                path, nemu, searching, neighbours = reset_grid()
        if event.type == pygame.QUIT:
            run[0] = False

    if queue and search:
        cur = queue.pop(0)

        if cur == None:
            search = False
            return com, con, search, queue, cur, nemu, path, active, weight, neighbours

        # Test Neighbours
        # if cur.start or not cur.start:
        #     print("Neigbours of " + str(cur.x) + " " + str(cur.y) + " weight -> " + str(cur.weight) + " dist -> " + str(cur.distance))
        #     if cur.prior:
        #         print("Prior " + str(cur.prior.x) + " " + str(cur.prior.y) + " dist -> " +str(cur.prior.distance))
        #     for n in cur.neigh:
        #         print(n.x, n.y)

        cur.visited = True
        if cur.end:
            search = False
            nemu = True
            print("Jarak: " + str(cur.distance))

            # while not cur.prior.start:
            #     path.append(cur.prior)
            #     cur = cur.prior

        else:
            # for n in cur.neigh:
            #     if not n.queued and not n.wall:
            #         n.queued = True
            #         n.prior = cur
            #         queue.append(n)

            # Update estimates
            for n in cur.neigh:
                if not n.visited and not n.wall:
                    if (cur.distance + n.weight) < n.distance:
                        n.distance = (cur.distance + n.weight)
                        n.prior = cur
                        n.queued = True
                    # n.queued = True
                    # n.prior = cur
                    # queue.append(n)

            # Pilih mau pergi kemana
            paling_min = float('inf')
            to_go = None

            for l in grid:
                for box in l:
                    if box.distance < paling_min and not box.visited:
                        paling_min = box.distance
                        to_go = box

            # to_go.prior = cur
            queue.append(to_go)

    else:
        if search:
            pygame.draw.rect(SCREEN, 'black', [200, 200, 200, 200], 0, 5)
            search = False

    return com, con, search, queue, cur, nemu, path, active, weight, neighbours


def draw_dfs(condition, search, stack, cur, nemu, path, neighbours):
    pygame.display.set_caption("Depth First Search")
    ready = None

    SCREEN.fill('#343434')

    com = 2
    con = condition

    check_color()

    font_1 = pygame.font.Font(None, 14)
    dis_n_btn = font_1.render('Set Neighbours', True, 'white')
    SCREEN.blit(dis_n_btn, (512, 505))

    menu_btn = pygame.draw.rect(SCREEN, 'gray', [225, 525, 150, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [225, 525, 150, 50], 5, 5)
    font_1 = pygame.font.Font(None, 36)
    a_text = font_1.render('Main Menu', True, 'black')
    SCREEN.blit(a_text, (235, 535))

    s_btn = pygame.draw.rect(SCREEN, "#FFD643", [165, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [165, 525, 50, 50], 5, 5)
    s_text = font_1.render('S', True, 'black')
    SCREEN.blit(s_text, (182, 538))

    e_btn = pygame.draw.rect(SCREEN, "#FF8800", [105, 525, 50, 50], 0, 5)
    pygame.draw.rect(SCREEN, 'dark gray', [105, 525, 50, 50], 5, 5)
    s_text = font_1.render('E', True, 'black')
    SCREEN.blit(s_text, (122, 538))

    w_col = pygame.Color('black')
    if con == 4:
        w_col = pygame.Color('red')
    w_btn = pygame.draw.rect(SCREEN, w_col, [45, 525, 50, 50], 0, 5)
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

    if nemu and not cur.start:
        path.append(cur)
        cur = cur.prior

    if not search:
        ready, queue, stack, end_node = check_ready()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(event.type)
            print(event.key)
            if event.key == pygame.K_RETURN and ready:
                # print("test hemm")
                path = reset_path_etc()
                assign_neighbours()
                search = True
                nemu = False
            if event.key == pygame.K_w:
                print("Test W")
                if con == 3:
                    con = 4
                else:
                    con = 3
            if event.key == pygame.K_s:
                con = 1
            if event.key == pygame.K_e:
                con = 2
            if event.key == pygame.K_KP1:
                neighbours[2] = not neighbours[2]
            if event.key == pygame.K_KP2:
                neighbours[5] = not neighbours[5]
            if event.key == pygame.K_KP3:
                neighbours[8] = not neighbours[8]
            if event.key == pygame.K_KP4:
                neighbours[1] = not neighbours[1]
            if event.key == pygame.K_KP5:
                pass
            if event.key == pygame.K_KP6:
                neighbours[7] = not neighbours[7]
            if event.key == pygame.K_KP7:
                neighbours[0] = not neighbours[0]
            if event.key == pygame.K_KP8:
                neighbours[3] = not neighbours[3]
            if event.key == pygame.K_KP9:
                neighbours[6] = not neighbours[6]
            if event.key == pygame.K_c:
                path, nemu, searching, neighbours = reset_grid()
        if event.type == pygame.QUIT:
            run[0] = False
        # print(queue[0].x, queue[0].y)
    if stack and search:
        cur = stack.pop()
        cur.visited = True
        if cur.end:
            search = False
            nemu = True
            # while not cur.prior.start:
            #     path.append(cur.prior)
            #     cur = cur.prior

        else:
            for n in cur.neigh:
                if not n.queued and not n.wall:
                    n.queued = True
                    n.prior = cur
                    stack.append(n)
    else:
        if search:
            pygame.draw.rect(SCREEN, 'black', [200, 200, 200, 200], 0, 5)
            search = False

    return com, con, search, stack, cur, nemu, path, neighbours


def check_color():
    for i in range(col):
        for j in range(row):
            # print(f'{i} {j}')
            box = grid[i][j]
            box.draw(SCREEN, (100, 100, 100))

            if box.weight != 1:
                box.draw(SCREEN, "#9867C5")

            if box.queued:
                box.draw(SCREEN, "#BEFFA6")
            if box.visited:
                box.draw(SCREEN, "#539375")
            if box in path:
                box.draw(SCREEN, "#FFE99B")

            if box.start:
                box.draw(SCREEN, "#FFD643")
            if box.wall:
                box.draw(SCREEN, (52, 52, 52))
            if box.end:
                box.draw(SCREEN, "#FF8800")

    for i in range(len(neigh_btn)):
        if i == 4:
            neigh_btn[i].draw(SCREEN, "#82EEFD")
        else:
            neigh_btn[i].draw(SCREEN, "#48AAAD")

        if not neighbours[i]:
            neigh_btn[i].draw(SCREEN, "#FF5C5C")


# Mengisi Grid
def make_grid():
    for i in range(col):
        arr = []
        for j in range(row):
            arr.append(Box(i, j))
        grid.append(arr)

    for i in range(26, 29):
        for j in range(26, 29):
            neigh_btn.append(Box(i, j))


def reset_grid():
    for i in grid:
        for box in i:
            box.start = False
            box.wall = False
            box.end = False
            box.queued = False
            box.visited = False
            box.prior = None
            box.weight = 1
            box.distance = float('inf')

    return [], False, False, [True] * 9


def reset_path_etc():
    for i in grid:
        for box in i:
            box.queued = False
            box.visited = False
            box.prior = None
            if not box.start:
                box.distance = float('inf')

    return []


def delete_start():
    for i in grid:
        for box in i:
            box.start = False
            box.distance = float('inf')


def delete_end():
    for i in grid:
        for box in i:
            box.end = False


def assign_neighbours():
    for i in range(col):
        for j in range(row):
            grid[i][j].reset_neighbours()
            grid[i][j].set_neighbours()


def check_ready():
    # Count buat start node
    cond1 = 0
    # Count buat end node
    cond2 = 0
    q = None
    s = None
    end_n = None

    for l in grid:
        for box in l:
            if box.start:
                cond1 += 1
                # Isi queue dengan Start Node
                # box.queued = True
                q = [box]
                s = [box]
            if box.end:
                cond2 += 1

    if cond1 == cond2 == 1:
        return True, q, s, end_n

    return False, q, s, end_n


def check_collide(con, nemu, path, searching):
    for l in grid:
        for box in l:
            if box.box.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                box.draw(SCREEN, (169, 169, 169))
                if pygame.mouse.get_pressed()[0]:
                    if con == 1 and not box.wall and not box.end:
                        delete_start()
                        box.start = True
                        box.distance = 0
                        path = reset_path_etc()
                        nemu = False
                        searching = False
                    elif con == 2 and not box.wall and not box.start:
                        delete_end()
                        box.end = True
                        path = reset_path_etc()
                        nemu = False
                        searching = False
                    elif con == 3:
                        path = reset_path_etc()
                        nemu = False
                        searching = False
                        if not box.start and not box.end:
                            # box.wall = not box.wall
                            box.weight = 1
                            box.wall = True
                    # messagebox.showinfo("cek aja", f"{con} box {box.x}, {box.y}")
                    elif con == 4:
                        path = reset_path_etc()
                        nemu = False
                        searching = False
                        if not box.start and not box.end:
                            # box.wall = not box.wall
                            box.wall = False
                    elif con == 5:
                        if weight != '' and int(weight) != 0:
                            path = reset_path_etc()
                            nemu = False
                            searching = False
                            if not box.start and not box.wall and not box.end:
                                box.weight = int(weight)
                                box.text = str(box.weight)
                                print(box.x, box.y, box.weight)

    for i in range(len(neigh_btn)):
        if neigh_btn[i].box.collidepoint(pygame.mouse.get_pos()) and i != 4:
            neigh_btn[i].draw(SCREEN, (169, 169, 169))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if pygame.mouse.get_pressed()[0]:
                neighbours[i] = not neighbours[i]
        elif neigh_btn[i].box.collidepoint(pygame.mouse.get_pos()) and i == 4:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)

    return nemu, path, searching


make_grid()

print(len(neigh_btn))


run = [True]
while run[0]:
    # print(neighbours)

    timer.tick(fps)

    if state == 0:
        state = draw_menu()
        path, nemu, searching, neighbours = reset_grid()
        con = 0
    if state == 1:
        state, con, searching, queue, cur, nemu, path, active, weight, neighbours = draw_djik(con, searching, queue, cur, nemu, path, active, weight, neighbours)
        nemu, path, searching = check_collide(con, nemu, path, searching)
    if state == 2:
        state, con, searching, stack, cur, nemu, path, neighbours = draw_dfs(con, searching, stack, cur, nemu, path, neighbours)
        nemu, path, searching = check_collide(con, nemu, path, searching)
    if state == 3:
        run[0] = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run[0] = False

    pygame.display.update()

pygame.quit()

