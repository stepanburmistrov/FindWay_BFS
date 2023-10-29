import pygame
import time


pygame.init()
frame_counter = 0

WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


CELL_SIZE = 20

lab = [[0 for j in range(40)] for i in range(25)]

for i in range(30):
    lab[0][i] = 1

for i in range(10, 40):
    lab[9][i] = 1

for i in range(30):
    lab[14][i] = 1

for i in range(10, 40):
    lab[17][i] = 1

def find_steps(y, x, labirint):
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, 1], [-1, 1], [1, -1]
    steps = []
    for dy, dx in ways:
        if (0 <= y + dy < len(labirint) and
                0 <= x + dx < len(labirint[0]) and
                labirint[y + dy][x + dx] == 0):
            steps.append((y + dy, x + dx))
    return steps


def draw_window(labirint, n_lab, start=None, finish=None, way=[]):
    win.fill(WHITE)

    # Рисуем клетки
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            if labirint[i][j] == 1:
                pygame.draw.rect(win, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif (i, j) in way:
                pygame.draw.rect(win, GREEN, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Рисуем старт и финиш
    if start:
        pygame.draw.rect(win, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if finish:
        pygame.draw.rect(win, RED, (finish[1] * CELL_SIZE, finish[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Рисуем цифры поверх клеток
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            if n_lab[i][j] != -1:
                font = pygame.font.SysFont(None, 12)
                text = font.render(str(n_lab[i][j]), True, BLACK) 
                win.blit(text, (j * CELL_SIZE + CELL_SIZE // 4, i * CELL_SIZE + CELL_SIZE // 4))

    pygame.display.update()
    global frame_counter
    filename = f"images/step{frame_counter:04}.png"
    pygame.image.save(win, filename)
    frame_counter += 1
    time.sleep(0.1)


def find_way(labirint, start=None, finish=None):
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, 1], [-1, 1], [1, -1]
    graph = {}
    for i in range(len(labirint)):
        for j in range(len(labirint[i])):
            if labirint[i][j] == 0:
                graph[(i, j)] = find_steps(i, j, labirint)

    n = 0
    n_lab = [[-1 for j in i] for i in labirint]
    n_lab[start[0]][start[1]] = 0
    finding = True
    while finding and n < len(n_lab) * len(n_lab[0]):
        n += 1
        for i in range(len(n_lab)):
            for j in range(len(n_lab[i])):
                if n_lab[i][j] == n - 1:
                    for point in graph[(i, j)]:
                        if n_lab[point[0]][point[1]] == -1:
                            dy = i - point[0]
                            dx = j - point[1]
                            if [dy, dx] in ways[4:]:
                                n_lab[point[0]][point[1]] = n + 2
                            else:
                                n_lab[point[0]][point[1]] = n + 1
                            if (point[0], point[1]) == finish:
                                finding = False
        draw_window(labirint, n_lab, start, finish)
        time.sleep(0.01)

    path_n_lab = [row.copy() for row in n_lab]
    way = []
    if finding:
        return []
    else:
        way.append(finish)
        curr_point = finish
        while curr_point != start:
            min_point = 99999
            temp_point = 0
            for dy, dx in ways:
                if (n_lab[curr_point[0] + dy][curr_point[1] + dx] <
                        n_lab[curr_point[0]][curr_point[1]] and
                        n_lab[curr_point[0] + dy][curr_point[1] + dx] != -1):
                    if (-1 < n_lab[curr_point[0] + dy][curr_point[1] + dx] < min_point):
                        temp_point = (curr_point[0] + dy, curr_point[1] + dx)
                        min_point = n_lab[curr_point[0] + dy][curr_point[1] + dx]
            curr_point = temp_point
            way.append(curr_point)
            draw_window(labirint, path_n_lab, start, finish, way)
            time.sleep(5.5)
        way = way[::-1]
        return way


def main():
    start_point = (1, 5)
    finish_point = (20, 30)

    way = find_way(lab, start_point, finish_point)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(lab, [[-1 for j in i] for i in lab], start_point, finish_point, way)

    pygame.quit()

if __name__ == "__main__":
    main()
