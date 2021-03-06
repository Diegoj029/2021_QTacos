import pygame as pg
import random
import copy
from qiskit import QuantumCircuit, Aer, execute
from resources import *
from Qtools import *
from tools import *

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60
TIME_LIMIT = 100
MAX_INGREDIENTS = 6
NAME = "DEFECTO"
CNOT_COUNT = 0
CNOT_CHANNEL1 = 0
SCORE = 0

"""
///////////////////////////////////////////////////////////
   QUANTUM ENGINE
///////////////////////////////////////////////////////////
"""

#Circuit and initial state
qc, state = inicioRandom()
rqc = copy.deepcopy(qc)
state_objetivo = randomQuantumState()
state_objetivo_str = dictostr(state_objetivo)


def newCircuit():
    global qc, state, state_objetivo, state_objetivo_str, rqc
    
    qc, state = inicioRandom()
    rqc = copy.deepcopy(qc)
    state_objetivo = randomQuantumState()
    state_objetivo_str = dictostr(state_objetivo)
    
def reiniciarCicuito():
    global qc, rqc
    qc = copy.deepcopy(rqc)

class QTaco():
    def __init__(self, QTortilla):
        self.QTortilla = QTortilla
        self.num_ingredients = 0

        #List with every ingredient in the QTaco
        self.ingredients_list = []

        #Position of the QTortilla
        if QTortilla == 'Tortilla1':
            self.x = 510
            self.y = 100
        elif QTortilla == 'Tortilla2':
            self.x = 390
            self.y = 285
            
        elif QTortilla == 'Tortilla3':
            self.x = 620
            self.y = 290

        self.pos = (self.x + 30,self.y + 20)

    def draw(self,screen):
        #Call this method to draw the ingredients on the QTortilla
        for ingredient in self.ingredients_list:
            screen.blit(ingredient.image, self.pos)
    
    def add_ingredient(self,ingredient):
        #Call this method to add an ingredient to the QTaco
        if self.num_ingredients <= MAX_INGREDIENTS:
            self.ingredients_list.append(ingredient)
            self.num_ingredients += 1

class ingredient():
    def __init__(self, image, gate):
        self.image = image
        self.gate = gate

#Ingredient init
In_desHebrada = ingredient(deshebrada, 'hadamard')
In_Xicken = ingredient(chicken, 'x')
In_onYon = ingredient(cebolla, 'y')
In_Zilantro = ingredient(cilantro, 'z')
In_pasNOT = ingredient(pastor, 'cnot')

class QTaco_builder():
    def __init__(self):
        self.queue = None
        #List with every taco
        self.QTaco_list = []

        #QTaco init
        self.QTaco_list.append(QTaco('Tortilla1'))
        self.QTaco_list.append(QTaco('Tortilla2'))
        self.QTaco_list.append(QTaco('Tortilla3'))

    def update(self, callback):
        if self.queue != None:
            global CNOT_COUNT, CNOT_CHANNEL1
            if self.queue.gate == "cnot":
                if CNOT_COUNT == 0:
                    if callback == "Tortilla1":
                        CNOT_CHANNEL1 = 0
                    elif callback == "Tortilla2":
                        CNOT_CHANNEL1 = 1
                    elif callback == "Tortilla3":
                        CNOT_CHANNEL1 = 2
                    CNOT_COUNT += 1
                else:
                    if callback == 'Tortilla1':
                        self.QTaco_list[0].add_ingredient(self.queue)
                        add_gate(qc,gate=self.queue.gate,channel=CNOT_CHANNEL1,channel_op=0)
                        self.queue = None
                    elif callback == 'Tortilla2':
                        self.QTaco_list[1].add_ingredient(self.queue)
                        add_gate(qc,gate=self.queue.gate,channel=CNOT_CHANNEL1,channel_op=1)
                        self.queue = None
                    elif callback == 'Tortilla3':
                        self.QTaco_list[2].add_ingredient(self.queue)
                        add_gate(qc,gate=self.queue.gate,channel=CNOT_CHANNEL1,channel_op=2)
                        self.queue = None
            else:
                if callback == 'Tortilla1':
                    self.QTaco_list[0].add_ingredient(self.queue)
                    add_gate(qc,gate=self.queue.gate,channel=0)
                    self.queue = None
                elif callback == 'Tortilla2':
                    self.QTaco_list[1].add_ingredient(self.queue)
                    add_gate(qc,gate=self.queue.gate,channel=1)
                    self.queue = None
                elif callback == 'Tortilla3':
                    self.QTaco_list[2].add_ingredient(self.queue)
                    add_gate(qc,gate=self.queue.gate,channel=2)
                    self.queue = None
        
        if callback == 'Deshebrada':
            self.queue = In_desHebrada
        elif callback == 'Chicken':
            self.queue = In_Xicken
        elif callback == 'Cebolla':
            self.queue = In_onYon
        elif callback == 'Cilantro':
            self.queue = In_Zilantro
        elif callback == 'Pastor':
            self.queue = In_pasNOT

        if callback == 'Paper':
            for QTaco in self.QTaco_list:
                QTaco.ingredients_list = []
            qc.barrier()
            qc.measure([0,1,2],[0,1,2])
    
            simulator = Aer.get_backend('qasm_simulator')
            rqs = measuring(qc, backend=simulator)
            resp = similarity(state_objetivo,rqs)
            global SCORE
            if resp[0]:
                SCORE += 1
                newCircuit()
            else:
                SCORE += -1
                newCircuit()
            
            
        elif callback == 'Canasta':
            for QTaco in self.QTaco_list:
                QTaco.ingredients_list = []
            reiniciarCicuito()
    
    def draw(self,screen):
        #Call this method to draw the ingredients on the QTortilla
        for QTaco in self.QTaco_list:
            QTaco.draw(screen)

"""
///////////////////////////////////////////////////////////
   GAME ENGINE
///////////////////////////////////////////////////////////
"""

class Game(object):
    def __init__(self):
        global SCORE
        global songs
        song = random.choice(songs)
        self.builder = QTaco_builder()

        #List with every game element (buttons)
        self.button_list = []

        #Button init
        self.button_list.append(Button(tortilla, tortilla_glow, (510,100),(180,180),'Tortilla1'))
        self.button_list.append(Button(tortilla, tortilla_glow, (390,285),(180,180),'Tortilla2'))
        self.button_list.append(Button(tortilla, tortilla_glow, (620,290),(180,180),'Tortilla3'))
        self.button_list.append(Button(trompo, trompo_glow, (0,310),(160,250),'Pastor'))
        self.button_list.append(Button(deshebrada, deshebrada_glow, (230,410),(150,150),'Deshebrada'))
        self.button_list.append(Button(chicken, chicken_glow, (180,260),(140,140),'Chicken'))
        self.button_list.append(Button(cilantro, cilantro_glow, (0,200),(155,80),'Cilantro'))
        self.button_list.append(Button(cebolla, cebolla_glow, (180,130),(120,100),'Cebolla'))
        self.button_list.append(Button(paper, paper_glow, (10,-10),(250,120),'Paper'))
        self.button_list.append(Button(canasta, canasta_glow, (320, 30),(95,80),'Canasta'))

        #Music
        pg.mixer.music.load(song)
        pg.mixer.music.play()


    def process_events(self):
        pos = pg.mouse.get_pos()

        for event in pg.event.get():
            #Quit game
            if event.type == pg.QUIT:
                return True
            
            #Click on screen
            #(Button implementation)
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in self.button_list:
                    if button.isOver(pos):
                        button.do_action(self.builder)
            
            #Hover effects trigger
            if event.type == pg.MOUSEMOTION:
                for button in self.button_list:
                    if button.isOver(pos):
                        button.hover_effects()
                


        return False

    def display_frame(self, screen, time_bar_width):
        #Background elements
        screen.fill(BLACK)
        screen.blit(game_bg,(0,0))
        screen.blit(plate,(370,90))

        #Display game elements
        for button in self.button_list:
            button.draw(screen)

        #Display ingredients in the QTortillas
        self.builder.draw(screen)

        #Display score
        score_msg = "Score: " + str(SCORE)
        message_to_screen(screen,score_msg,BLUE,(660,50),60)

        #Display order
        order_msg = state_objetivo_str
        message_to_screen(screen,order_msg,BLACK,(40,40),40)

        #Display initial states
        state_msg1 = "q0:|{}>".format(state[1])
        message_to_screen(screen,state_msg1,BLACK,(600,140),40)

        state_msg2 = "q1:|{}>".format(state[2])
        message_to_screen(screen,state_msg2,BLACK,(500,350),40)

        state_msg3 = "q2:|{}>".format(state[3])
        message_to_screen(screen,state_msg3,BLACK,(700,350),40)

        #Display timer bar
        pg.draw.rect(screen, RED,(0,0,time_bar_width,20))

        pg.display.flip()

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.back_btn = Button(back,back_glow,(0,0),(50,50),"Back")
        self.input_box1 = InputBox(100, 100, 140, 32)
        self.input_boxes = []

        self.input_boxes.append(self.input_box1)

        #Launch app
        self.main_menu()


    def process_events(self,button_list):
        pos = pg.mouse.get_pos()

        for event in pg.event.get():
            #Quit game
            if event.type == pg.QUIT:
                pg.mixer.music.stop()
                return True
            
            #Click on screen
            #(Button implementation)
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in button_list:
                    if button.isOver(pos):
                        self.menu_open(button)
            
            #Hover effects trigger
            if event.type == pg.MOUSEMOTION:
                for button in button_list:
                    if button.isOver(pos):
                        button.hover_effects()
            
            #Input boxes
            for box in self.input_boxes:
                box.handle_event(event)


    def main_menu(self):
        done = False

        button_list = []

        button_list.append(Button(play, play_glow, (-15,100),(200,100),'Play'))
        button_list.append(Button(leaderboard, leaderboard_glow, (0,200),(350,80),'Leaderboard'))
        button_list.append(Button(howtoplay, howtoplay_glow, (0,280),(300,65),'How to Play'))
        button_list.append(Button(options, options_glow, (0,350),(200,65),'Options'))
        button_list.append(Button(cred, cred_glow, (440,530),(150,80),'Credits'))

        while not done:
            done = self.process_events(button_list)
            
            #Display elements
            self.screen.fill(BLUE)
            self.screen.blit(main_menu_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()
    

    def game_rt(self):
        global songs
        song = random.choice(songs)
        
        done = False
        clock = pg.time.Clock()
        timer = TIME_LIMIT
        time_bar_width = SCREEN_WIDTH
        time_bar_speed = SCREEN_WIDTH / TIME_LIMIT
        game = Game()

        pg.mixer.music.load(os.path.join(game_folder,song))
        pg.mixer.music.play()

        global SCORE
        while not done:
            done = game.process_events()
            game.display_frame(self.screen, time_bar_width)
            clock.tick(FPS)
            timer -= 1
            time_bar_width -= time_bar_speed
            if timer <= 0:
                player_name = self.game_over()
                record_score(player_name)
                SCORE = 0
                done = True
        pg.mixer.music.stop()


    def leaderboard(self):
        done = False

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list) #or back_btn_Pressed()

            #Display elements
            self.screen.fill(RED)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()

    def howtoplay(self):
        done = False

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list) #or back_btn_Pressed()

            #Display elements
            self.screen.fill(BLUE)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()

    def options(self):
        done = False

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list) #or back_btn_Pressed()

            #Display elements
            self.screen.fill(RED)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()

    def credits(self):
        done = False

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list) #or back_btn_Pressed()

            #Display elements
            self.screen.fill(RED)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()
    
    def game_over(self):
        done = False
        player_name = ""

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list)# or back_btn_Pressed()

            #Display elements
            self.screen.fill(WHITE)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)
            for box in self.input_boxes:
                    box.update()

            for box in self.input_boxes:
                box.draw(self.screen)
                player_name = box.text

            message_to_screen(self.screen,"GAME OVER",RED,(300,50),80)
            message_to_screen(self.screen,"SCORE: " + str(SCORE),WHITE,(300,500),80)

            pg.display.flip()

        
        return player_name

    def menu_open(self,button):
        callback = button.callback
        if callback == 'Play':
            self.game_rt()
        elif callback == 'Leaderboard':
            self.leaderboard()
        elif callback == 'How to Play':
            self.howtoplay()
        elif callback == 'Options':
            self.options()
        elif callback == 'Credits':
            self.credits()
        elif callback == 'Back':
            pg.event.custom_type()
            

"""
///////////////////////////////////////////////////////////
   RUN
///////////////////////////////////////////////////////////
"""
def main():
    pg.init()

    screen = pg.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

    Menu(screen)

    pg.quit()


if __name__ == "__main__":
	main()
