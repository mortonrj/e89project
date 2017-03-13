#!/usr/bin/env python
# -*- coding: utf-8 -*-
# zModule example2

# First of all, obviously import zModule
from zModule import *
#import mainloop as MainLoop
import os
import pygame
import pygame.font
from pygame.locals import *
import mainloop as MainLoop

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    import pygame

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.
    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface

def button(msg,x,y,w,h,ic,ac,action=None):
    screen = pygame.display.get_surface()
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font("./data/cubicfive10.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

# Define functions (You can do this in a separate file and then just import it)
def start_game():
    print("This should do a thing")
    MainLoop.main()

def game_info():
    screen = pygame.display.get_surface()
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                return
        #cb.update(events)    #update the checkbutton, requires events
        screen.fill(0x000000)

        my_font1 = pygame.font.Font(None, 30)
        my_font2 = pygame.font.Font(None, 22)

        my_string1 = "Welcome."
        my_string2 = "In this game, you are a web crawler, sliding from one website to another, plucking out the images you find.  Your journey is placed in context to a stop motion exploration through a smoother, less jarring physical world. "
        my_string3 = "In the start menu, you are given two options - a starting place for the crawler, and a starting place for the outdoor explorer.  If you choose simple start, these will be chosen for you.  Once you enter the crawler's world, you can use the joystick to increase and decrease your speed.  The button that will rest underneath you index finger can increase the number of crawled images shown on the screen at any one time.  Happy exploring!"
        my_rect1 = pygame.Rect((width/2 - width/6, height/2 - height/4, width/3, height/3))
        my_rect2 = pygame.Rect((width/2 - width/6, height/2-height/6 , width/3, height/3))
        my_rect3 = pygame.Rect((width/2 - width/6, height/2, width/3, height/3))
        rendered_text1 = render_textrect(my_string1, my_font1, my_rect1, (0, 255, 0), (0,0,0), 1)
        rendered_text2 = render_textrect(my_string2, my_font2, my_rect2, (216, 216, 216), (0,0,0))
        rendered_text3 = render_textrect(my_string3, my_font2, my_rect3, (216, 216, 216), (0,0,0))
        if rendered_text1 and rendered_text2 and rendered_text3:
            screen.blit(rendered_text1, my_rect1.topleft)
            screen.blit(rendered_text2, my_rect2.topleft)
            screen.blit(rendered_text3, my_rect3.topleft)

        button("Back",150,450,100,50,white,green,main)
        button("Quick Start",550,450,100,50,white,green,start_game)

        pygame.display.flip()

def main():
    # Call zEngine inizializer
    # In this example we only set the window title (that will be also the menu title)
    # and the title color
    #datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    #font = os.path.join(datadir,'cubicfive10.ttf')
    #game =zEngine(1026, 768,"Are you ready to start your journey?",titlepos=(30,200),titledim=40,titlefont=font,titlecolor=GREEN)
    #game.MainMenu.submenu("Start",start_game)
    #game.MainMenu.submenu("Game description", game_info)
    #cb = zTextButton("Where will it begin?", (600,600), nothing, nothing, 3, None, RED, RED, RED)
    #cb = zTextButton(game_info, (50, 100), "Where Will it begin?", 30, None, RED, BLUE)
    # We can also set the color of submenus when selected or not
    #game.MainMenu.set_normal_color(GREEN)        #non-selected
    #game.MainMenu.set_highlight_color(YELLOW) #selected

    #game.mainloop()

    pygame.init()
    print("hi")
    size = width, height = 1026, 768
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    print("hi")

    while 1:
        # Fills screen with a color
        screen.fill(black)

        # Checking for quit event, and if so exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        my_font1 = pygame.font.Font("./data/cubicfive10.ttf", 20)
        my_font2 = pygame.font.Font("./data/cubicfive10.ttf", 26)
        my_string1 = "Are you ready to start your journey?"
        my_string2 = "Where will it begin?"
        my_rect1 = pygame.Rect((width/2 - width/4, height/2 - height/4, width/2, height/3))
        my_rect2 = pygame.Rect((width/2 - width/4, height/2-height/6 , width/2, height/3))
        rendered_text1 = render_textrect(my_string1, my_font1, my_rect1, green, (0,0,0), 1)
        rendered_text2 = render_textrect(my_string2, my_font2, my_rect2, green, (0,0,0), 1)
        if rendered_text1 and rendered_text2:
            screen.blit(rendered_text1, my_rect1.topleft)
            screen.blit(rendered_text2, my_rect2.topleft)


        button("About",width/4 - 100,height-200,200,50,white,green,game_info)
        button("Simple Start",2*width/4 - 100,height-200,200,50,white,green,start_game)
        button("Choose Start",3*width/4 - 100,height-200,200,50,white,green,start_game)


        pygame.display.flip()

if __name__ == '__main__':
    main()
