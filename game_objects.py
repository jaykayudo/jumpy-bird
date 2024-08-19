from typing import Any
import pygame
from constants import SCALE_FACTOR

class Bird:
    def __init__(self,screen):
        self.image = pygame.image.load("assets/bird.png").convert_alpha()   
        self.image = pygame.transform.scale_by(self.image,SCALE_FACTOR)    
        self.rect:"pygame.Rect" = self.image.get_rect()
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.rect.center = (self.screen_width/2,self.screen_height/2)
        self.dy = 0
        self.GRAVITY_FORCE = (5 * SCALE_FACTOR) # for the falling of the bird
        self.gravity = True
        
    def __call__(self):
        return self.rect
    def render(self):
        self.screen.blit(self.image,self.rect)
    def detect_collision(self,rect):
        if self.rect.colliderect(rect):
            return True
        return False
    
    def detect_floor_collision(self):
        if self.rect[1] + self.rect.height >= self.screen_height:
            return True
        return False


    def logic(self):
        if self.gravity:
            if self.dy > 0:
                self.dy = 0
            self.dy += (self.GRAVITY_FORCE * 1.5)
            self.rect.centery  = self.rect.centery + self.dy
        else:
            self.dy = -(10 * SCALE_FACTOR)
            self.rect.centery  = self.rect.centery + self.dy

    def update_y(self,y):
        self.rect.center = (self.rect.centerx,y)


class Pipe:
    def __init__(self,screen, x,y, orientation="bottom"):
        self.screen = screen
        self.posx = x
        self.posy = y
        self.pipe = pygame.image.load("assets/pipe.png").convert_alpha()
        self.pipe = pygame.transform.scale_by(self.pipe,SCALE_FACTOR)
        self.rect = self.pipe.get_rect()
        
        self.orientation = orientation
        if self.orientation =="bottom":
            self.rect.topleft = (self.posx,self.posy)
        else:
            self.rect.bottomleft = (self.posx,self.posy)
        self.remove = False
        
        self.pipe_speed = (3 * SCALE_FACTOR)
    def render(self):
        if self.orientation == "bottom":
            image = self.pipe
            self.screen.blit(image,self.rect)
        else:
            image = pygame.transform.flip(self.pipe,False,True)
            self.screen.blit(image,self.rect)
    def logic(self):
        if not self.remove:
            self.rect.topleft = (self.rect[0] - self.pipe_speed, self.rect[1]) 
            
            if self.rect[0] + self.rect.width < 0:
                self.remove = True


class PipePair:
    def __init__(self,screen,y):
        self.screen = screen
        self.posx = self.screen.get_width() + (32 * SCALE_FACTOR)
        self.posy = y
        self.pipe_margin = (90 * SCALE_FACTOR)
        self.pipes ={
            'upper': Pipe(self.screen,self.posx,self.posy,"top"),
            'lower': Pipe(self.screen,self.posx,self.posy + self.pipe_margin),
        }
        self.remove = False
        self.scored = False
    def render(self):
        for pipe_key in self.pipes:
            self.pipes[pipe_key].render()
    def logic(self):
        for pipe_key in self.pipes:
            self.pipes[pipe_key].logic()
        if self.pipes["upper"].remove and self.pipes["lower"].remove:
            self.remove = True 
    def collide(self,rect):
        if self.pipes["upper"].rect.colliderect(rect) or self.pipes["lower"].rect.colliderect(rect):
            return True
        return False
    def is_evaded(self,x):
        if self.pipes["upper"].rect.x + self.pipes["upper"].rect.width < x and self.pipes["lower"].rect.x + self.pipes["lower"].rect.width <x:
            return True
        return False
    
class Score:
    def __init__(self,screen):
        self.screen = screen
        self.BIG_FONT = pygame.font.Font("fonts/flappy.ttf", (30 * round(SCALE_FACTOR)))
    def render(self,score):
        color = (255,255,255)
        score_display = self.BIG_FONT.render(f"Score: {score}",1,color)
        score_display_rect = score_display.get_rect()
        score_display_rect.topleft = ((10 * SCALE_FACTOR), (30 * SCALE_FACTOR))
        self.screen.blit(score_display,score_display_rect)




    
    