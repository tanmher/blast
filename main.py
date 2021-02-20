import pygame
import pygame_menu
import random
import pandas as pd

pygame.init()
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("BLAST!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

button_font = pygame.font.SysFont("comicsans", 30)
guess_font = pygame.font.SysFont("comicsans", 50)
lost_font = pygame.font.SysFont('comicsans', 45)
def_font = pygame.font.SysFont('comicsans', 20)


word = ''
buttons = []
guessed = []
images = []
file = pd.read_csv('content.csv')
category = file.loc[file['category'] == 'science']
rand = random.randrange(0, 9)

# Load image and store in image variable
for i in range(7):
    image = pygame.image.load("dynamite" + str(i) + ".jpg")
    images.append(image)

click = False
dynamite_status = 0


# Display the game
def redraw_game_window(rand):
    global guessed
    global dynamite
    global dynamite_status
    word = randomWord(rand, category)
    win.fill(WHITE)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 3
                               )
            label = button_font.render(chr(buttons[i][5]), 2, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spaced_out(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]

    win.blit(label1, (winWidth / 2 - length / 2, 400))
    win.blit(images[dynamite_status], (winWidth / 2 - images[dynamite_status].get_width() / 2 + 20, 150))
    if dynamite_status == 6:
        any_key = def_font.render('Press any key to continue', 1, BLACK)
        rect = any_key.get_rect()
        length = rect[2]
        win.blit(any_key, (winWidth / 2 - length / 2, 450))

    pygame.display.update()


# Generate random word depending on the category
def randomWord(rand, category):
    global word
    word = category['words'][rand]
    return word


# Get the definition of the word depending on the category
def definition(rand, category):
    global word
    d = category['definition'][rand]
    return d


# Return boolean value if the word is right or wrong
def boom(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


# Display the Letters Selected by the user
def spaced_out(word, guessed):
    spaced_word =''
    guessed_letters= guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spaced_word += '_ '
            for i in range(len(guessed_letters)):
                if word[x].upper() == guessed_letters[i]:
                    spaced_word = spaced_word[:-2]
                    spaced_word += word[x].upper() + ' '
        elif word[x] == ' ':
            spaced_word += ' '
    return spaced_word


# Locate where the button hit
def button_hit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


# Reset Values for trying the game again
def reset():
    global dynamite_status
    global guessed
    global buttons
    global word
    global rand
    for i in range(len(buttons)):
        buttons[i][4] = True

    dynamite_status = 0
    guessed = []
    rand = random.randrange(0, 9)
    word = randomWord(rand, category)


# Create Game Over Menu
game_over = pygame_menu.Menu(winHeight, winWidth, 'Game Over', theme=pygame_menu.themes.THEME_DARK)


# Display Lose or Win, Word, and Definition. Try Again and Quit Button
def end(winner):
    global dynamite_status
    win.fill(WHITE)
    game_over.clear()
    if winner:
        game_over.add_label('Great Job :)', font_size=30)
    else:
        game_over.add_label('You lose :(', font_size=30)
    game_over.add_vertical_margin(40)
    game_over.add_label('The word was: ', font_size=20)
    game_over.add_label(word.upper(), font_size=40, font_color=YELLOW)
    game_over.add_label(definition(rand, category), font_size=15, max_char=75)
    game_over.add_vertical_margin(40)
    game_over.add_button('Try Again', menu)
    game_over.add_button('Quit', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if game_over.is_enabled():
            game_over.update(events)
            game_over.draw(win)

        pygame.display.update()
        reset()


increase = round(winWidth/13)

for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([WHITE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])


# Create Start Game function that runs the primary game
def start_game():
    global category
    global dynamite_status
    dynamite_status = 0
    while True:
        redraw_game_window(rand)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                letter = button_hit(click_pos[0], click_pos[1])
                if letter is not None:
                    guessed.append(chr(letter))
                    buttons[letter - 65][4] = False
                    if boom(chr(letter)):
                        if dynamite_status != 6:
                            dynamite_status += 1
                    else:
                        if spaced_out(word, guessed).count('_') == 0:
                            end(True)
            else:
                if dynamite_status >= 6:
                    if event.type == pygame.KEYDOWN:
                        end(False)

        pygame.display.update()


# Set Category for content reference
def set_category(value, num):
    global category
    name, index = value
    if index == 0:
        category = file.loc[file['category'] == 'science']
    elif index == 1:
        category = file.loc[file['category'] == 'language']
    elif index == 2:
        category = file.loc[file['category'] == 'comprog']
    elif index == 3:
        category = file.loc[file['category'] == 'mathematics']
    # Reset index of the category from 0 to 9
    category = category.reset_index()


# Create Menu Interface using pygame-menu
mymenu = pygame_menu.Menu(winHeight, winWidth, title='Select Category', theme=pygame_menu.themes.THEME_DARK)

# Add Selector for Selecting Category
mymenu.add_selector('',
                  [('Science', 1),
                   ('Language', 2),
                   ('Computer Programming', 3),
                   ('Mathematics', 4)],
                  onchange=set_category, font_size = 30)
mymenu.add_vertical_margin(75)

# Add Button Play or Quit
mymenu.add_button('Play', start_game)
mymenu.add_button('Quit', pygame_menu.events.EXIT)

play = True


# Create Menu Function
def menu():
    while play:
        win.fill(WHITE)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if mymenu.is_enabled():
            mymenu.update(events)
            mymenu.draw(win)

        pygame.display.update()

menu()