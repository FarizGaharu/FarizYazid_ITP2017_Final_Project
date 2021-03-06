'''
Whack_A_Mole.py
    A smasher game with Whack-A-Mole logic
original work Created by Excelino.Fernando/excelincode
            & William.Raharja/willraharja
        in 21.10.2017pp
Version 0.1a 21.10.2017
    Framework and Basic Logic
reference from William.Raharja/willraharja
        in 04.11.2017
        Version 0.9
Improved by Fariz Ihsan Yazid/FarizGaharu
        in 06.11.2017
        version 0.9A
'''

import pygame, random, time, os, sys
from pygame.locals import *
from pygame.font import *


background_image = 'guns-n-roses-1.jpg'
#RGB colours combination
Noir = (0, 0, 0) # == black
Blanc = (255, 255, 255) # == white
Rouge = (200, 0, 0) # == red
Vert = (0, 255, 0) # == green
VertBrillant = (50, 205, 50)# == brigth green
Bleu = (0, 0, 255)# == blue
BleuBrillant = (135,206,235) # == brigth blue

scrWidth = 800
scrHeight = 600
screen = pygame.display.set_mode((scrWidth, scrHeight))
# ---------------------------------------------------------
class Slash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("saul_hudson1.png").convert_alpha()
        self.rect = self.image.get_rect()

    # move Slash to a new random location when it gets hit
    def flee(self):
        x = random.randint(0, scrWidth-1-self.rect.width)
        y = random.randint(0, scrHeight-1-self.rect.height)
        self.rect.topleft = (x,y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# ---------------------------------------------------------
class Smasher(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("forbidden.png")
        self.rect = self.image.get_rect()


    # did the hammer hit the mole?
    def hit(self, target):
        self.image = pygame.image.load("forbidden.png")
        return self.rect.colliderect(target)

    # follows the mouse cursor
    def update(self, pt):
        self.image = pygame.image.load("forbidden.png")
        self.rect.center = pt

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# -----------------------------------

def center_Image(screen, im):
    x = (scrWidth - im.get_width() - 10)
    y = (scrHeight - im.get_height())
    screen.blit(im, (x, 0))

def center_Screen(screen, im):
    x = (scrWidth/4)
    y = (scrHeight/2)
    screen.blit(im, (x, y))

def scoreboard(input_screen, data, x, y, input_font_size, input_message_format = 'Dodged: %d'):
    #display the score
    font = pygame.font.SysFont(None, input_font_size)
    text = font.render(input_message_format%data, True, Blanc)
    input_screen.blit(text, (x, y))

#variables
pygame.init()
screen.fill(Noir)
pygame.display.set_caption("Hit leSlash")
background = pygame.image.load(background_image).convert()
scrWidth, scrHeight = screen.get_size()
Huge_Font = pygame.font.Font('brothers_of_metal.ttf', 45)
font = pygame.font.Font(None, 30)

hitSnd = pygame.mixer.Sound('Ha_01.wav')
hitSnd.set_volume(0.5)

zero = 0
if not os.path.exists("save_topScore.dat"):
    write_into_file = open("save_topScore.dat", 'w')
    write_into_file.write(str(zero))
    write_into_file.close()
read_into_file = open("save_topScore.dat")
saved_topScore = int(read_into_file.readline())
read_into_file.close()

# create sprites and a group
mole = Slash()
hammer = Smasher()
#pause = False

# game variables
mousePos = (scrWidth/2, scrHeight/2)
DELAY = 800
clock = pygame.time.Clock()
ticker_timer = pygame.time.get_ticks()
def scoreboard(screen, data, x, y,input_font_size, input_message_format):
    font = pygame.font.SysFont(None, input_font_size)
    text = font.render(input_message_format%data, True, (255, 255, 255))
    screen.blit(text, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, Noir)
    return textSurface, textSurface.get_rect()

def message_display(text):
    Big_Text = pygame.font.Font('brothers_of_metal.ttf', 100)
    Txt_Surf, Txt_Rect = text_objects(text, Big_Text)
    Txt_Rect.center = ((scrWidth / 2), (scrHeight / 2))
    screen.blit(Txt_Surf, Txt_Rect)

    pygame.display.update()

#Universal_Button
def button(msg,x,y,w,h,ic,ac,action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    small_txt = pygame.font.SysFont(None, 20)
    txt_surf, txt_Rect = text_objects(msg, small_txt)
    txt_Rect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(txt_surf, txt_Rect)


#menu UI
def introduction():
    pygame.mouse.set_visible(True)
    intro = True

    while intro:

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(Blanc)
        Big_Text = pygame.font.Font("metal lord.ttf", 55)
        Txt_Surf, Txt_Rect = text_objects("Hit Le Slash", Big_Text)
        Txt_Rect.center = ((scrWidth / 2), (scrHeight / 2))
        screen.blit(Txt_Surf, Txt_Rect)


        button("Start!", scrWidth*0.45, scrHeight*0.45 + 100, 110, 55, Vert, VertBrillant, game_run)
        button("Quit", scrWidth*0.45, scrHeight*0.45 + 200, 110, 55, Bleu,BleuBrillant, quit)

        pygame.display.update()
        clock.tick(100)

def pause_game():
    global pause
    pygame.mouse.set_visible(True)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(Blanc)
        big_text = pygame.font.Font('brothers_of_metal.ttf',110)
        Txt_Surf, Txt_Rect = text_objects('Paused', big_text)
        Txt_Rect.center =((scrWidth/2), (scrHeight/2))
        screen.blit(Txt_Surf, Txt_Rect)


        button('Continue', scrWidth*0.45, scrHeight*0.45 + 100, 110, 55, Vert, VertBrillant, game_run)
        button('Quit', scrWidth*0.45, scrHeight*0.45 + 200, 110, 55, Bleu, BleuBrillant, quit)

        pygame.display.update()
        clock.tick(60)


#in game concept
#return game is playing
def game_run():
    global saved_topScore
    init_time = pygame.time.get_ticks() #init_time, how long the game has run since it started
    running = True
    score = 0
    #global variable to declare mousePos inside the function
    while running:

        #hide the mouse cursor
        pygame.mouse.set_visible(False)

        # handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    pause_game()
                    running = True
            if event.type == MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                running = True

        # update game
        hammer.update(pygame.mouse.get_pos())
        ev = pygame.event.wait()
        if ev.type == QUIT:
            pygame.quit()
            break
        elif ev.type == MOUSEBUTTONDOWN:
            if hammer.hit(mole):
                hitSnd.play()
                mole.flee()
                score += 1
                pygame.time.set_timer(USEREVENT + 1, DELAY)
            else:
                hitSnd.play()
        elif ev.type == USEREVENT + 1:
            mole.flee()
        #time limit, approximately 30 sec
        if (pygame.time.get_ticks() - init_time) >= 30000:
            temp = pygame.time.get_ticks()
            if score < saved_topScore:
                while pygame.time.get_ticks() - temp <= 6000: #wait 5000 ms == 5 sec
                    screen.fill(Noir)
                    lose = Huge_Font.render("Slash Got away, You Lose! ", True, Blanc)
                    center_Screen(screen, lose)
                    pygame.display.update()
                else:
                    print("0: Hah!, You Lose")
                    introduction()
            else:
                while pygame.time.get_ticks()-temp <= 6000: #wait 5000ms
                    screen.fill(Blanc)
                    win = Huge_Font.render("Slash is down, You Win!", True, Noir)
                    center_Screen(screen, win)
                    pygame.display.update()
                else:
                    print("0: You Win!")
                    introduction()

        # redraw game background, (0, 0))

        screen.blit(background, (0, 0))

        # time elapsed (in secs)
        mole.draw(screen)
        hammer.draw(screen)
        time = int((pygame.time.get_ticks() - init_time)/1000)
        timeIm = font.render(str(time), True, Blanc)

        hitIm = font.render("Hits = " + str(score), True, Blanc)
        center_Image(screen, hitIm)

        scoreboard(screen, saved_topScore, scrWidth*0.45, 50, 50, "Top: %d")

        screen.blit(timeIm, (10,10))
        if score > saved_topScore:
            write_into_file = open("score_save.dat",'w')
            write_into_file.write(str(score))
            write_into_file.close()
            saved_topScore = score

        pygame.display.update()
        clock.tick(60)

introduction()
pygame.quit()
quit()
'''thank you and have a nice day'''
