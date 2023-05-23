import pygame
import random
import pygame.mixer

pygame.init()
pygame.mixer.init()
LEVEL = 4
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
font2048 = pygame.font.Font('freesansbold.ttf', 36)
font_lvl = pygame.font.Font('freesansbold.ttf', 24)

b_values = [[0 for _ in range(LEVEL)] for _ in range(LEVEL)]
cnt = 0
score = 0
direc = ''
sound = False
music = pygame.mixer.Sound("Clown.mp3")

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

def toggle_sound():
    global sound
    sound = not sound
    if sound:
        music.play(-1)  # Воспроизвести музыку в цикле
    else:
        music.stop()

# draw game over
def draw_over():
    pygame.draw.rect(screen, (255, 250, 242), [50, 230, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'red')
    game_over_text2 = font.render('Press Enter to Restart', True, 'black')
    screen.blit(game_over_text1, (130, 250))
    screen.blit(game_over_text2, (85, 290))


def show_direction(direc, board):
    global score
    merged = [[False for _ in range(LEVEL)] for _ in range(LEVEL)]

    if direc == 'UP':
        for j in range(LEVEL):
            for i in range(1, LEVEL):
                if board[i][j] != 0:
                    k = i
                    while k > 0 and (board[k-1][j] == 0 or (board[k][j] == board[k-1][j] and not merged[k][j] and not merged[k-1][j])):
                        if board[k-1][j] == 0:
                            board[k-1][j] = board[k][j]
                            board[k][j] = 0
                        elif board[k][j] == board[k-1][j] and not merged[k][j] and not merged[k-1][j]:
                            board[k-1][j] *= 2
                            score += board[k-1][j]
                            board[k][j] = 0
                            merged[k-1][j] = True
                        k -= 1

    elif direc == 'DOWN':
        for j in range(LEVEL):
            for i in range(LEVEL-2, -1, -1):
                if board[i][j] != 0:
                    k = i
                    while k < LEVEL-1 and (board[k+1][j] == 0 or (board[k][j] == board[k+1][j] and not merged[k][j] and not merged[k+1][j])):
                        if board[k+1][j] == 0:
                            board[k+1][j] = board[k][j]
                            board[k][j] = 0
                        elif board[k][j] == board[k+1][j] and not merged[k][j] and not merged[k+1][j]:
                            board[k+1][j] *= 2
                            score += board[k+1][j]
                            board[k][j] = 0
                            merged[k+1][j] = True
                        k += 1

    elif direc == 'LEFT':
        for i in range(LEVEL):
            for j in range(1, LEVEL):
                if board[i][j] != 0:
                    k = j
                    while k > 0 and (board[i][k-1] == 0 or (board[i][k] == board[i][k-1] and not merged[i][k] and not merged[i][k-1])):
                        if board[i][k-1] == 0:
                            board[i][k-1] = board[i][k]
                            board[i][k] = 0
                        elif board[i][k] == board[i][k-1] and not merged[i][k] and not merged[i][k-1]:
                            board[i][k-1] *= 2
                            score += board[i][k-1]
                            board[i][k] = 0
                            merged[i][k-1] = True
                        k -= 1

    elif direc == 'RIGHT':
        for i in range(LEVEL):
            for j in range(LEVEL-2, -1, -1):
                if board[i][j] != 0:
                    k = j
                    while k < LEVEL-1 and (board[i][k+1] == 0 or (board[i][k] == board[i][k+1] and not merged[i][k] and not merged[i][k+1])):
                        if board[i][k+1] == 0:
                            board[i][k+1] = board[i][k]
                            board[i][k] = 0
                        elif board[i][k] == board[i][k+1] and not merged[i][k] and not merged[i][k+1]:
                            board[i][k+1] *= 2
                            score += board[i][k+1]
                            board[i][k] = 0
                            merged[i][k+1] = True
                        k += 1

    return board, merged



# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, LEVEL-1)
        col = random.randint(0, LEVEL-1)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

RESTART_HEIGHT = 30
RESTART_WIDTH = 70

button_restart = pygame.Rect(240, 70, RESTART_WIDTH, RESTART_HEIGHT)
button_bot = pygame.Rect(322, 70, 50, 30)
button_level = pygame.Rect(25, 70, 65, 30)
button_sound = pygame.Rect(105, 70, 80, 30)
# draw background
def draw_board():
    main_text = font2048.render(f'2048', True, (0,0,0))
    pygame.draw.rect(screen, colors['bg'], [25, 110, 350, 350])
    score_text = font.render(f'Score: {score}', True, colors['bg'])
    bestScore_text = font.render(f'High Score: {bestScore}', True, colors['bg'])
    screen.blit(main_text, (25, 10))
    screen.blit(score_text, (130, 10))
    screen.blit(bestScore_text, (130, 40))

    pygame.draw.rect(screen, (250, 128, 114), button_restart,0,10)
    restart_text = pygame.font.SysFont(None, 20).render("Restart", True, (255, 250, 242))
    screen.blit(restart_text, (253, 78))

    pygame.draw.rect(screen, (233, 150, 122), button_bot,0,10)
    bot_text = pygame.font.SysFont(None, 20).render("Bot", True, (255, 250, 242))
    screen.blit(bot_text, (335, 78))

    pygame.draw.rect(screen, (240, 128, 128), button_level,0,10)
    level_text = pygame.font.SysFont(None, 20).render("Level", True, (255, 250, 242))
    screen.blit(level_text, (38, 78))

    pygame.draw.rect(screen, (205, 92, 92), button_sound,0,10)
    sound_text = pygame.font.SysFont(None, 20).render("Sound On" if sound else "Sound Off", True, (255, 250, 242))
    screen.blit(sound_text, (113, 78))
    pass




button_3 = pygame.Rect(115, 250, 60,30)
button_4 = pygame.Rect(115, 290, 60,30)
button_5 = pygame.Rect(217, 250, 60,30)
button_6 = pygame.Rect(217, 290, 60,30)

def draw_level():
    pygame.draw.rect(screen, (255, 250, 242), [50, 230, 300, 105], 0, 10)
    
    pygame.draw.rect(screen, colors[8], button_3,0,10)
    text_3 = font_lvl.render(f'3x3', True, (255, 250, 242))
    screen.blit(text_3, (125, 253))

    pygame.draw.rect(screen, colors[16], button_4,0,10)
    text_4 = font_lvl.render(f'4x4', True, (255, 250, 242))
    screen.blit(text_4, (125, 293))

    pygame.draw.rect(screen, colors[32], button_5,0,10)
    text_5 = font_lvl.render(f'5x5', True, (255, 250, 242))
    screen.blit(text_5, (228, 253))

    pygame.draw.rect(screen, colors[64], button_6,0,10)
    text_6 = font_lvl.render(f'6x6', True, (255, 250, 242))
    screen.blit(text_6, (228, 293))
    


x = 25
y = 110
# draw pieces
def draw_pieces(board):
    cell_size = 350 // LEVEL
    padding = cell_size // 10  # Размер отступа между ячейками
    cell_width = (350 - (LEVEL + 1) * padding) // LEVEL
    cell_height = (350 - (LEVEL + 1) * padding) // LEVEL
    for i in range(LEVEL):
        for j in range(LEVEL):
            value = board[i][j]
            if value > 8:
                value_color = colors['light']
            else:
                value_color = colors['dark']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['black']
            cell_x = 1+25 + padding + j * (cell_width + padding)  # Вычисление координаты X верхнего левого угла ячейки
            cell_y = 1+110 + padding + i * (cell_height + padding)  # Вычисление координаты Y верхнего левого угла ячейки

            pygame.draw.rect(screen, color, [cell_x, cell_y, cell_width, cell_height], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font2 = pygame.font.Font('freesansbold.ttf', 48 - (6 * value_len))
                value_text = font2.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, color, [cell_x, cell_y, cell_width, cell_height], 2, 5)

def has_available_moves(board):
    # Check if there are any empty cells
    for row in board:
        if 0 in row:
            return True

    # Check for adjacent cells with the same value
    for i in range(len(board)):
        for j in range(len(board[i])):
            if i > 0 and board[i][j] == board[i-1][j]:
                return True
            if i < len(board)-1 and board[i][j] == board[i+1][j]:
                return True
            if j > 0 and board[i][j] == board[i][j-1]:
                return True
            if j < len(board[i])-1 and board[i][j] == board[i][j+1]:
                return True

    return False

def board_full(board):
    for row in board:
        if 0 in row:
            return False
    return True


  



bot = False
run = True
directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
level = False
while run:
    timer.tick(fps)
    screen.fill((255, 250, 242))
    draw_board()
    draw_pieces(b_values)
    
    if bot:
        direc = random.choice(directions)
        pygame.time.wait(200)
    if level:
        draw_level()

    if not has_available_moves(b_values):
        if board_full(b_values):
            game_over = True
            bot = False
        else:
            continue 

    if create or cnt < 2:
        if has_available_moves(b_values):
            if board_full(b_values):
                create = False
            else:
                b_values, game_over = new_pieces(b_values)
                create = False
                cnt += 1
    if direc != '':
        b_values,merged = show_direction(direc, b_values)
        direc = ''
        create = True
        direct = ''
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                if button_restart.collidepoint(mouse_pos):  
                    b_values = [[0 for _ in range(LEVEL)] for _ in range(LEVEL)]
                    create = True
                    cnt = 0
                    score = 0
                    direc = ''
                    game_over = False
                    bot = False
                if button_bot.collidepoint(mouse_pos):  
                    if bot:
                        bot = False
                    else:
                        bot = True
                if button_level.collidepoint(mouse_pos):  
                    if level:
                        level = False
                    else:
                        level = True
                if button_3.collidepoint(mouse_pos):  
                    LEVEL = 3
                    b_values = [[0 for _ in range(LEVEL)] for _ in range(LEVEL)]
                    create = True
                    cnt = 0
                    score = 0
                    direc = ''
                    game_over = False
                    level = False
                if button_4.collidepoint(mouse_pos):  
                    LEVEL = 4
                    b_values = [[0 for _ in range(LEVEL)] for _ in range(LEVEL)]
                    create = True
                    cnt = 0
                    score = 0
                    direc = ''
                    game_over = False
                    level = False
                if button_5.collidepoint(mouse_pos):  
                    LEVEL = 5
                    b_values = [[0 for _ in range(LEVEL)] for _ in range(LEVEL)]
                    create = True
                    cnt = 0
                    score = 0
                    direc = ''
                    game_over = False
                    level = False
                if button_6.collidepoint(mouse_pos):  
                    LEVEL = 6
                    b_values = [[0 for _ in range(LEVEL)] for _ in range(LEVEL)]
                    create = True
                    cnt = 0
                    score = 0
                    direc = ''
                    game_over = False
                    level = False
                if button_sound.collidepoint(mouse_pos):  
                    if sound:
                        music.stop()
                        sound = False
                    else:
                        music.play(-1)
                        sound = True

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
                    b_values = [[0 for _ in range(LEVEL)] for _ in range(LEVEL)]
                    create = True
                    cnt = 0
                    score = 0
                    direc = ''
                    game_over = False
    if score > bestScore:
        bestScore = score

    pygame.display.flip()
pygame.quit()
