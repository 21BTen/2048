import pygame
import random

pygame.init()

WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
font2048 = pygame.font.Font('freesansbold.ttf', 36)

b_values = [[0 for _ in range(4)] for _ in range(4)]
cnt = 0
score = 0
direc = ''

# 2048 colors
colors = {0: (179, 175, 167),
          2: (238, 226, 219),
          4: (239, 224, 201),
          8: (243, 178, 120),
          16: (245, 150, 100),
          32: (245, 125, 95),
          64: (246, 95, 59),
          128: (237, 207, 115),
          256: (237, 204, 98),
          512: (239, 200, 80),
          1024: (238, 197, 63),
          2048: (237, 195, 46),
          'light': (249, 246, 242),
          'dark': (119, 110, 101),
          'bg': (135, 133, 130)}




file = open('bestScore', 'r')
init_high = int(file.readline())
file.close()
bestScore = init_high

game_over = False
create = True

# draw game over
def draw_over():
    pygame.draw.rect(screen, (255, 250, 242), [50, 230, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'red')
    game_over_text2 = font.render('Press Enter to Restart', True, 'black')
    screen.blit(game_over_text1, (130, 250))
    screen.blit(game_over_text2, (85, 290))


def show_direction(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] \
                            and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] \
                            and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] \
                        and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] \
                            and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background
def draw_board():
    main_text = font2048.render(f'2048', True, colors['bg'])
    pygame.draw.rect(screen, colors['bg'], [25, 110, 350, 350], 0, 10)
    score_text = font.render(f'Score: {score}', True, colors['bg'])
    bestScore_text = font.render(f'High Score: {bestScore}', True, colors['bg'])
    screen.blit(main_text, (25, 10))
    screen.blit(score_text, (200, 10))
    screen.blit(bestScore_text, (200, 40))
    pass


# draw pieces
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light']
            else:
                value_color = colors['dark']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors[black]
            pygame.draw.rect(screen, color, [j * 85 + 35, i * 85 + 120, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 85 + 72, i * 85 + 157))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, color, [j * 85 + 35, i * 85 + 120, 75, 75], 2, 5)



run = True
while run:
    timer.tick(fps)
    screen.fill((255, 250, 242))
    draw_board()
    draw_pieces(b_values)
    if create or cnt < 2:
        b_values, game_over = new_pieces(b_values)
        create = False
        cnt += 1
    if direc != '':
        b_values = show_direction(direc, b_values)
        direc = ''
        create = True
    if game_over:
        draw_over()
        if bestScore > init_high:
            file = open('bestScore', 'w')
            file.write(f'{bestScore}')
            file.close()
            init_high = bestScore

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direc = 'UP'
            elif event.key == pygame.K_DOWN:
                direc = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direc = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direc = 'RIGHT'

            if game_over:
                if event.key == pygame.K_RETURN:
                    b_values = [[0 for _ in range(4)] for _ in range(4)]
                    create = True
                    cnt = 0
                    score = 0
                    direc = ''
                    game_over = False

    if score > bestScore:
        bestScore = score

    pygame.display.flip()
pygame.quit()