import pygame as pg
import pandas as pd
import os
from resources import leaderboard_txt
from game import SCORE

#Basic colors
BLACK   = (     0,  0,    0)
WHITE   = (   255,255,  255)
RED     = (   255,  0,    0)
BLUE    = (     0,  0,  255)

#Text render method
def message_to_screen(screen,msg,color,position,size):
    font = pg.font.SysFont(None, size)
    text = font.render(msg,True,color)
    screen.blit(text,position)

def record_score(player_name):
    pd_leaderboard = pd.read_csv(leaderboard_txt)
    new_score = (player_name,SCORE)
    pd_leaderboard.append(new_score)
    pd_leaderboard = pd_leaderboard.sort_values('score')
    pd_leaderboard.to_csv(leaderboard_txt)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = BLACK
        self.COLOR_ACTIVE = BLUE
        self.COLOR_INACTIVE = BLACK
        self.FONT = pg.font.Font(None, 32)
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

class Button():
    def __init__(self, image, effects, position, size, callback):
        self.image = image
        self.effects = effects
        self.position = position
        self.size = size
        self.callback = callback

        #Hitbox definition
        self.x = position[0] + (size[0] / 6)
        self.y = position[1] + (size[1] / 6)
        self.width = size[0]
        self.height = size[1]

        #Effects flag
        self.do_effects = False

    def draw(self,screen):
        #Call this method to draw the button on the screen
        screen.blit(self.image,self.position)
        if self.do_effects:
            screen.blit(self.effects, self.position)


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < (self.x + self.width):
            if pos[1] > self.y and pos[1] < (self.y + self.height):
                return True
        
        self.do_effects = False
        return False

    def hover_effects(self):
        self.do_effects = True

    def do_action(self, builder):
        builder.update(self.callback)