import pygame as pg
import sys
import csv
import random
from states import States
from objects import Hero

class Simulator(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
        self.party_exp = 0
    def cleanup(self):
        self.party = []
    def startup(self):
        self.screen.fill(self.white)
        
        def name_data():
            with open('./ab_data/names.csv', "r") as name:
                name_reader = csv.reader(name)
                self.names = list(tuple(row) for row in name_reader)
        name_data()
        #we didn't create hero objects
        self.party = random.sample(self.names, 3)
        States.party_heroes = self.party
        
        States.current_adventure = "dark_forest"
        locations = Data.location_data(States.current_adventure)
        locations["desc"] = "tree1", "content"
        #tree1-tree2-bush2-cave
        #tree1-bush2-bush3-cave
        #bush1-tree3-bush4-cave
        #bush1-tree4-bush4-cave
        
        #load monster content for path nodes(other info)
        #do fight, check exp, add talents/stats if levelup
        #if [] or troll dead, data dump, end
    #Simulator interface
    #Draw simulator interface
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True

        elif event.type == pg.MOUSEBUTTONDOWN:
            pass

    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        self.screen.blit(self.ground, (0,0))
        self.selection_sprites.draw(self.screen)
        self.screen.blit(self.bubble, self.bubble_rect)
        self.screen.blit(self.hood, self.hood_rect)

        [pg.draw.rect(self.screen, self.red, [f_hero.pos_x, f_hero.pos_y, f_hero.width, f_hero.height], 2) for f_hero in self.selection if f_hero.spot_frame == True]
        
        if len(States.party_heroes) == self.max_party_size:
            self.screen.blit(self.ready_text, self.continue_rect)    
        else:
            self.screen.blit(self.continue_text, self.continue_rect)
        
        for shero in self.selection:
            if shero.rect.collidepoint(pg.mouse.get_pos()):
                COORDS_INFO = ((shero.pos_x), (shero.pos_y + (self.height / 7.1)))
                info = shero.name.capitalize() + ", " + shero.type.capitalize()
                info_text = self.info_font.render(info, True, self.black)
                info_text_rect = info_text.get_rect(topleft=COORDS_INFO)
                self.screen.blit(info_text, info_text_rect)