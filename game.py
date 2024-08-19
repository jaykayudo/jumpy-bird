import pygame
from state_machine import StateMachine
from states import *
from constants import SCALE_FACTOR


pygame.init()
class Game: 
    def __init__(self):
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        pygame.display.set_caption("Jumpy Bird")
        self.clock = pygame.time.Clock()
        self.FPS  = 20
        
        
        # game play
        self.state_machine = StateMachine(
            {
                'play': PlayState,
                'title': TitleState,
                'countdown': CountdownState,
                'score': ScoreState
            },
            self.screen
        )
        self.state_machine.change("title")
        self.game_play = True

        # music
        self.game_music = pygame.mixer.music.load("sounds/marios_way.mp3")
        
        # needed image assets
        self.background = pygame.image.load("assets/background.png")
        self.ground = pygame.image.load("assets/ground.png")

        self.background = pygame.transform.scale_by(self.background,SCALE_FACTOR)
        self.ground = pygame.transform.scale_by(self.ground,SCALE_FACTOR)

        # FOR SCROLLING
        self.scrolling = True
        self.background_x = 0
        self.BACKGROUND_SCROLL_SPEED = 5 * SCALE_FACTOR
        self.BACKGROUND_LOOPING_POINT = 413 * SCALE_FACTOR # to make sure the background scroll infinitely
        self.ground_x = 0
        self.GROUND_SCROLL_SPEED = 10 * SCALE_FACTOR
    def display_background(self):
        if self.scrolling:
            self.background_x = (self.background_x + self.BACKGROUND_SCROLL_SPEED) % self.BACKGROUND_LOOPING_POINT
        self.screen.blit(self.background,(-self.background_x,0))
    def display_ground(self):
        if self.scrolling:
            self.ground_x = (self.ground_x + self.GROUND_SCROLL_SPEED) % self.WINDOW_WIDTH
        self.screen.blit(self.ground,(-self.ground_x,self.WINDOW_HEIGHT - (16 * SCALE_FACTOR)))
    
    def game(self):
        pygame.mixer.music.play(-1)
        while self.game_play:
            # self.game_music.play
            self.display_background()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_play = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    
                    self.state_machine.key_event(event.key)
                if event.type == pygame.KEYUP:
                    self.state_machine.key_event_up(event.key)


            self.state_machine.render()
            self.state_machine.logic()
            self.display_ground()

            pygame.display.flip()
            self.clock.tick(self.FPS)




game = Game()
game.game()