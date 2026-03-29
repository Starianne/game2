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


game_state = GameState()

event_manager = EventManager()

start_buttons = []
game_buttons = []
event_buttons = []

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1' #called after pygame.init()
info = pygame.display.Info() #called before set_mode()
screen_width, screen_height = info.current_w, info.current_h #grabs screen width and height
global screen
screen = pygame.display.set_mode((screen_width, screen_height)) #coords so must have another set of brackets around them to define them
pygame.display.set_caption('Game 2')

#game state vars
global game_started
game_started = False

global game_active
game_active = False

global game_complete
game_complete = False

clock = pygame.time.Clock()
running = True
dt = 0


#must be under pygame.init()
#font:
global title_font
title_font = pygame.font.Font('font/DigitalDisco.ttf', 50)

global text_font
text_font = pygame.font.Font('font/DigitalDisco.ttf', 25)


#intro:
title_surface = title_font.render("Game 2", False, "white").convert_alpha()
title_rect = title_surface.get_rect(center = (screen_width/2, (screen_height/2)-200))

#maingame:
main_surface = pygame.image.load('graphics/backgrounds/goobs_city.png').convert()
main_surface = pygame.transform.scale(main_surface, (3*screen_width/5, 3*screen_height/5))
main_rect = main_surface.get_rect(center = (2*screen_width/3, 2*screen_height/5))

#terminal:
terminal_surface = pygame.Surface((int(2*screen_width/7), int(5*screen_height/7)))
terminal_surface.fill("#AFEBFA")
terminal_rect = terminal_surface.get_rect(topleft = (screen_width/20, screen_height/10))

#make function for text in terminal:
def make_terminal(screen, game_state, font, title_font, rect):
    padding = screen_height/45
    y = rect.top + padding

    pygame.draw.rect(screen, "#AFEBFA", rect)

    title = title_font.render("Goob's rewards:", True, "black")
    screen.blit(title, (rect.left + padding, y))
    y += screen_height/20

    for log in game_state.event_log:
        log_surf = font.render(log, True, "black")
        screen.blit(log_surf, (rect.left + padding, y))
        y += screen_height/25

    def format_stat(label, value, prefix=""):
        if value < 0:
            return f"{label}: -{prefix}{abs(value)}"
        else:
            return f"{label}: {prefix}{value}"

    stats = [
        format_stat("Money", game_state.money, "£"),
        format_stat("Sweets", game_state.sweets),
        format_stat("Hats", game_state.hats),
    ]
    stats_y = rect.bottom - screen_height/5

    for stat in stats:
        stat_surf = title_font.render(stat, True, "black")
        screen.blit(stat_surf, (rect.left + padding, stats_y))
        stats_y += screen_height/20


#end
end_surface = text_font.render("Game 2 is over, well done!", False, "white").convert_alpha()
end_rect = title_surface.get_rect(center = (screen_width/2, (screen_height/2)-200))

#day:
global current_day
current_day = 0


#groups: 
#player sprite group
goob = pygame.sprite.GroupSingle()
goob.add(Goob(4, game_state, 2*screen_width/3, 2*screen_height/5 + screen_height/30))

def start_game_func():
    global game_started 
    game_started = True
    print('started game') #to check in terminal remove later
    make_game_active_func()
    toggle_all_movement()
    return game_started

def make_game_active_func():
    global game_active
    game_active = True
    print('active game') #same as started game
    return game_active

def tutorialFunc():
    global tutorial
    tutorial = True
    return tutorial

#movement toggles
def toggle_horizontal_movement():
    s = goob.sprite
    if s is None:       
        return
    s.horizontal_available = 0 if s.horizontal_available == 1 else 1 #ternary/conditional expression did not know this was a thing in python too
    return s.horizontal_available

def toggle_vertical_movement():
    z = goob.sprite
    if z is None:       
        return
    z.vertical_available = 0 if z.vertical_available == 1 else 1 #ternary/conditional expression did not know this was a thing in python too
    return z.vertical_available

def toggle_all_movement():
    toggle_horizontal_movement()
    toggle_vertical_movement()

#events--------------------------------------------------------------------
#uhhhh remakeeee
global events
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

def decide_event():
    valid_events = []

    for event in event_pool:
        if not all(game_state.get_flag(f) for f in event.get("requires", [])):
            continue

        if any(game_state.get_flag(f) for f in event.get("blocks", [])):
            continue

        if event.get("once") and game_state.get_flag(event.get("flag")):
            continue

        valid_events.append(event)
    
    if not valid_events:
        return
    
    chosen = random.choice(valid_events)
    event_manager.start_event(chosen["event_name"](game_state, text_font, (screen_width, screen_height), screen), flag=chosen.get("flag"))


#-----------------------------------------------------------------------------------
MAX_DAYS = 25

def increment_day_func():
    global current_day, game_complete
    current_day += 1

    if current_day >= MAX_DAYS:
        ending = select_ending(game_state)
        event_manager.start_event(ending["event"](game_state, text_font, (screen_width, screen_height), screen))
        game_complete = True
        return
    decide_event()
    return current_day, game_complete

def pause_unpause_game_func():
    global game_active
    game_active = False if game_active == True else True
    return game_active

start_buttons.append(Button(7*screen_width/18, screen_height/2-(screen_height/10), 400, 100, title_font, start_game_func, 'Start Game', screen))
game_buttons.append(Button(7*screen_width/18, screen_height/2+(screen_height/4), 400, 100, title_font, increment_day_func, 'Get through the day', screen)) #press this and current day goes up 

while running: #need to add async here i think
        #player inputs will be here
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        
        screen.fill("#4595DF")

        if game_started == False:
            screen.blit(title_surface,title_rect)
            for btn in start_buttons:
                btn.process(events)

        elif game_complete and not event_manager.is_active():
            print("game complete")
            running = False       
        
        elif event_manager.is_active():
            event_manager.update(events, screen)


        elif game_active:
                goob.sprite.control_mode = "idle"
                day_surface = title_font.render("GOOB - Day "+ str(current_day), False, "white").convert_alpha()
                day_rect = day_surface.get_rect(center = (screen_width/2, screen_height/16))
                screen.blit(day_surface,day_rect)
                screen.blit(main_surface, main_rect)
                make_terminal(screen, game_state, text_font, title_font, terminal_rect)
                #Actual game goes in here
                game_buttons[0].process(events) 

                goob.draw(screen)
                goob.update()   

        pygame.display.flip()
        dt = clock.tick(60) / 1000
pygame.quit()

    
