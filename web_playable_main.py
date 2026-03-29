import pygame
import asyncio

from goobs import *
from text_box import Textbox
import os
import random
from gamestate import GameState
from button import Button
from event_manager import EventManager
from ending_manager import select_ending

from find_money_5 import find_money_5_event
from lose_money_5 import lose_money_5_event
from find_money_10 import find_money_10_event
from lose_money_10 import lose_money_10_event
from find_sweet import find_sweet_event
from lose_sweet import lose_sweet_event
from find_hat import find_hat_event
from lose_hat import lose_hat_event
from holly_molly import holly_molly_event
from holly_advice import holly_advice_event
from holly_uni import holly_uni_event
from molly_real_name import molly_real_name_event
from molly_advice import molly_advice_event
from molly_plan_present import molly_plan_present_event
from molly_give_present import molly_give_present_event
from meowntain import meowntain_event
from dont_mention_it import dont_mention_it_event
from jay_stops import jay_stops_event
from jay_meet import jay_meet_event
from joel_hangout import joel_hangout_event
from meet_cratin import meet_cratin_event
from learn_cratin import learn_cratin_event

event_pool = [
    {
        "event_name" : find_money_5_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : None,
    },
    {
        "event_name" : lose_money_5_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : None,
    },
    {
        "event_name" : find_money_10_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : None,
    },
    {
        "event_name" : lose_money_10_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : None,
    },
    {
        "event_name" : find_sweet_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : None,
    },
    {
        "event_name" : lose_sweet_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : None,
    },
    {
        "event_name" : find_hat_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : None,
    },
    {
        "event_name" : lose_hat_event,
        "requires" : [],
        "blocks" : [],
        "once" : False,
        "flag" : "None",
    },
    {
        "event_name" : holly_molly_event,
        "requires" : [],
        "blocks" : [],
        "once" : True,
        "flag" : "did_holly_molly_event",
    },
    {
        "event_name" : holly_advice_event,
        "requires" : ["did_holly_molly_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_holly_advice_event",
    },
    {
        "event_name" : holly_uni_event,
        "requires" : ["did_holly_advice_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_holly_uni_event",
    },
    {
        "event_name" : molly_real_name_event,
        "requires" : ["did_holly_molly_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_molly_real_name_event",
    },
    {
        "event_name" : molly_advice_event,
        "requires" : ["did_holly_molly_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_molly_advice_event",
    },
    {
        "event_name" : molly_plan_present_event,
        "requires" : ["did_molly_advice_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_molly_plan_present_event",
    },
    {
        "event_name" : molly_give_present_event,
        "requires" : ["did_molly_plan_present_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_molly_give_present_event",
    },
    {
        "event_name" : dont_mention_it_event,
        "requires" : [],
        "blocks" : [],
        "once" : True,
        "flag" : "did_dont_mention_it",
    },
    {
        "event_name" : jay_stops_event,
        "requires" : ['liar'],
        "blocks" : [],
        "once" : True,
        "flag" : "did_jay_stops_event",
    },
    {
        "event_name" : jay_meet_event,
        "requires" : ['honest'],
        "blocks" : [],
        "once" : True,
        "flag" : "did_jay_meet_event",
    },
    {
        "event_name" : joel_hangout_event,
        "requires" : ["did_jay_meet_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_joel_hangout_event",
    },
    {
        "event_name" : meowntain_event,
        "requires" : [],
        "blocks" : [],
        "once" : True,
        "flag" : "did_meowntain_event",
    },
    {
        "event_name" : meet_cratin_event,
        "requires" : [],
        "blocks" : [],
        "once" : True,
        "flag" : "did_meet_cratin_event",
    },
    {
        "event_name" : learn_cratin_event,
        "requires" : ["did_meet_cratin_event"],
        "blocks" : [],
        "once" : True,
        "flag" : "did_learn_cratin_event",
    },
]

class Game:
    MAX_DAYS = 25



    def __init__(self):
        pygame.init()

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Game 2')

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.game_state = GameState()
        self.event_manager = EventManager()

        #buttons
        self.start_buttons = []
        self.game_buttons = []
        self.event_buttons = []

        self.start_buttons.append(Button(7*self.screen_width/18, self.screen_height/2-(self.screen_height/10), 400, 100, self.title_font, self.start_game_func, 'Start Game', self.screen))
        self.game_buttons.append(Button(7*self.screen_width/18, self.screen_height/2+(self.screen_height/4), 400, 100, self.title_font, self.increment_day_func, 'Get through the day', self.screen)) #press this and current day goes up 

        self.game_started = False
        self.game_active = False
        self.game_complete = False

        self.title_font = pygame.font.Font('font/DigitalDisco.ttf', 50)
        self.text_font = pygame.font.Font('font/DigitalDisco.ttf', 25)
        
        #intro
        self.title_surface = self.title_font.render("Game 2", False, "white").convert_alpha()
        self.title_rect = self.title_surface.get_rect(center = (self.screen_width/2, (self.screen_height/2)-200))

        #main game
        self.main_surface = pygame.image.load('graphics/backgrounds/goobs_city.png').convert()
        self.main_surface = pygame.transform.scale(self.main_surface, (3*self.screen_width/5, 3*self.screen_height/5))
        self.main_rect = self.main_surface.get_rect(center = (2*self.screen_width/3, 2*self.screen_height/5))

        #terminal
        self.terminal_surface = pygame.Surface((int(2*self.screen_width/7), int(5*self.screen_height/7)))
        self.terminal_surface.fill("#AFEBFA")
        self.terminal_rect = self.terminal_surface.get_rect(topleft = (self.screen_width/20, self.screen_height/10))

        self.end_surface = self.text_font.render("Game 2 is over, well done!", False, "white").convert_alpha()
        self.end_rect = self.title_surface.get_rect(center = (self.screen_width/2, (self.screen_height/2)-200))

        self.current_day = 0
        

#fix the 5000000 other functions and make async then add minigame and polish stuff - proper endscreen, multiple sprites? music? idk - enough to get to the 7.5 hours left atleast
    def start_game_func():
        pass

    def increment_day_func():
        pass


    def make_terminal(self, screen, game_state, font, title_font, rect):
        self.padding = self.screen_height/45
        self.y = self.rect.top + self.padding

        pygame.draw.rect(screen, "#AFEBFA", rect)

        self.title = self.title_font.render("Goob's rewards:", True, "black")
        screen.blit(self.title, (self.rect.left + self.padding, self.y))
        self.y += self.screen_height/20

        for log in self.game_state.event_log:
            log_surf = font.render(log, True, "black")
            screen.blit(log_surf, (rect.left + self.padding, self.y))
            self.y += self.screen_height/25

        def format_stat(label, value, prefix=""):
            if value < 0:
                return f"{label}: -{prefix}{abs(value)}"
            else:
                return f"{label}: {prefix}{value}"

        stats = [
            format_stat("Money", self.game_state.money, "£"),
            format_stat("Sweets", self.game_state.sweets),
            format_stat("Hats", self.game_state.hats),
        ]
        stats_y = rect.bottom - self.screen_height/5

        for stat in stats:
            stat_surf = title_font.render(stat, True, "black")
            screen.blit(stat_surf, (rect.left + padding, stats_y))
            stats_y += screen_height/20



    def make_game_active_func():
        pass

    def toggle_horizontal_movement():
        pass

    def toggle_vertical_movement():
        pass

    def toggle_all_movement():
        toggle_vertical_movement()
        toggle_horizontal_movement()

    def decide_event():
        pass
    
    

    def pause_unpause_game_func():
        pass



    async def run(self):
        running = True
        while running:
           pygame.display.flip() 
        pygame.quit()


