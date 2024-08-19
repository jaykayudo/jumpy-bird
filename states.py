from game_objects import Bird, PipePair, Score
import pygame
import random
from constants import SCALE_FACTOR

class BaseState:
    """
    Abstract state class for all state
    """
    def __init__(self, state_machine,screen):
        pass
    def key_event_up(self,key):
        pass
    def key_event(self,key):
        raise NotImplementedError("Key Event method must be implement")
    def render(self):
        raise NotImplementedError("Render method must be implement")
    def logic(self):
        raise NotImplementedError("Logic method must be implemented")
    





class PlayState(BaseState):
    def __init__(self, state_machine,screen):
        self.state_machine = state_machine
        self.screen = screen
        self.bird = Bird(screen)
        self.bird_rect = self.bird()
        self.bird_dy = (20 * SCALE_FACTOR)
        self.sounds = {
            'hurt': pygame.mixer.Sound("sounds/hurt.wav"),
            'explosion': pygame.mixer.Sound("sounds/explosion.wav"),
            'jump': pygame.mixer.Sound("sounds/jump.wav"),
            'score': pygame.mixer.Sound("sounds/score.wav"),
        }
        self.pipe_height = (60 * SCALE_FACTOR)
        self.lastY = (20 * SCALE_FACTOR)
        self.timer = 0
        self.pipe_pairs = []
        self.score = 0
        self.score_display = Score(self.screen)
    def render(self):
        self.bird.render()
        for pair in self.pipe_pairs:
            pair.render()
        self.score_display.render(self.score)
    def logic(self):
        self.bird.logic()
        
        floor_collision = self.bird.detect_floor_collision()
        if floor_collision:
            self.sounds['hurt'].play()
            self.sounds['explosion'].play()
            self.state_machine.change("score",{'score':self.score})
        self.timer += 0.05
        if self.timer > 2:
            # print("Greater")
            y = max(self.pipe_height/2 - (20 * SCALE_FACTOR), min(self.lastY + random.randint(-(20 * round(SCALE_FACTOR)), (40 * round(SCALE_FACTOR))), self.screen.get_height() - (90 * round(SCALE_FACTOR)) - self.pipe_height/2))
            # y = 20
            self.lastY = y
            self.pipe_pairs.append(PipePair(self.screen,y))
            self.timer = 0
        for pair in self.pipe_pairs:
            pair.logic()
            if pair.collide(self.bird.rect):
                self.sounds['hurt'].play()
                self.sounds['explosion'].play()
                self.state_machine.change("score",{'score':self.score})
                break
            if not pair.scored:
                if pair.is_evaded(self.bird.rect.x):
                    pair.scored = True
                    self.score += 1
                    self.sounds['score'].play()
            if pair.remove:
                self.pipe_pairs.remove(pair)

    def key_event(self, key):
        if key == pygame.K_SPACE:
            self.bird.gravity = False
            self.sounds['jump'].play()
    def key_event_up(self, key):
        if key == pygame.K_SPACE:
            self.bird.gravity = True

class TitleState(BaseState):
    def __init__(self, state_machine, screen):
        self.state_machine = state_machine
        self.screen = screen
        self.BIG_FONT = pygame.font.Font("fonts/flappy.ttf", (30 * round(SCALE_FACTOR)))
        self.SMALL_FONT = pygame.font.Font("fonts/font.ttf",(16 * round(SCALE_FACTOR)))

    def render(self):
        color = (255,255,255)
        self.welcome_text = self.BIG_FONT.render("Welcome to Jumpy Bird",1,color)
        self.welcome_text_rect = self.welcome_text.get_rect()
        self.welcome_text_rect.center = (self.screen.get_width()/2, (50 * SCALE_FACTOR))
        self.continue_text = self.SMALL_FONT.render("Press Enter to Start",1,color)
        self.continue_text_rect = self.continue_text.get_rect()
        self.continue_text_rect.center = (self.screen.get_width()/2, (100 * SCALE_FACTOR))

        self.screen.blit(self.welcome_text,self.welcome_text_rect)
        self.screen.blit(self.continue_text,self.continue_text_rect)
    def key_event(self, key):
        if key == pygame.K_RETURN:
            self.state_machine.change("countdown")

    def logic(self):
        pass
            

class ScoreState(BaseState):
    def __init__(self, state_machine, screen, score = 0):
        self.state_machine = state_machine
        self.screen = screen
        self.score = score
        self.BIG_FONT = pygame.font.Font("fonts/flappy.ttf", 30 * round(SCALE_FACTOR))
        self.SMALL_FONT = pygame.font.Font("fonts/font.ttf",16 * round(SCALE_FACTOR))

    def render(self):
        color = (255,255,255)
        self.welcome_text = self.BIG_FONT.render(f"OOpps you Failed",1,color)
        self.welcome_text_rect = self.welcome_text.get_rect()
        self.welcome_text_rect.center = (self.screen.get_width()/2, 50 * SCALE_FACTOR)
        self.score_text = self.BIG_FONT.render(f"Score: {self.score}",1,color)
        self.score_text_rect = self.score_text.get_rect()
        self.score_text_rect.center = (self.screen.get_width()/2, 100 * SCALE_FACTOR)
        self.continue_text = self.SMALL_FONT.render("Press Enter to Play Again",1,color)
        self.continue_text_rect = self.continue_text.get_rect()
        self.continue_text_rect.center = (self.screen.get_width()/2, 150 * SCALE_FACTOR)

        self.screen.blit(self.welcome_text,self.welcome_text_rect)
        self.screen.blit(self.continue_text,self.continue_text_rect)
        self.screen.blit(self.score_text,self.score_text_rect)
    def key_event(self, key):
        if key == pygame.K_RETURN:
            self.state_machine.change("countdown")
    def logic(self):
        pass
class CountdownState(BaseState):
    def __init__(self, state_machine, screen, score = 0):
        self.state_machine = state_machine
        self.screen = screen
        self.score = score
        self.BIG_FONT = pygame.font.Font("fonts/flappy.ttf", 30 * round(SCALE_FACTOR))
        self.SMALL_FONT = pygame.font.Font("fonts/font.ttf",16 * round(SCALE_FACTOR))
        self.countdown = 4
        self.timer = 1
        self.coundown_sound = pygame.mixer.Sound("sounds/score.wav")
    def render(self):
        color = (255,255,255)
        self.countdown_text = self.BIG_FONT.render(f"{self.countdown}",1,color)
        self.countdown_text_rect = self.countdown_text.get_rect()
        self.countdown_text_rect.center = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.screen.blit(self.countdown_text,self.countdown_text_rect)
    def key_event(self, key):
        pass
    def logic(self):
        self.timer += 0.05
        if self.timer > 1:
            self.countdown -= 1
            self.coundown_sound.play()
            if self.countdown == 0:
                self.state_machine.change("play")
            self.timer = 0
        