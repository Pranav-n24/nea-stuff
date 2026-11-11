import pygame
import sys
import threading 
import queue
from info import getLaps, getTtLimit, getAtLimit
from monte_carlo import isValidScSequence
from strategy_generator import generateCompleteStrategySequence
pygame.init()
#creating fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("F1 Strategy Simulator")
clock = pygame.time.Clock()
#screen backgrounds loading
background = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\Selection.png").convert_alpha()
bahrain = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\bahrain.png").convert_alpha()
saudiArabia = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\saudi arabia.png").convert_alpha()
australia = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\australia.png").convert_alpha()
azerbaijan = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\azerbaijan.png").convert_alpha()
miami = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\miami.png").convert_alpha()
monaco = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\monaco.png").convert_alpha()
spain = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\spain.png").convert_alpha()
canada = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\canada.png").convert_alpha()
austria = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\austria.png").convert_alpha()
britain = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\britain.png").convert_alpha()
hungary = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\hungary.png").convert_alpha()
belgium = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\belgium.png").convert_alpha()
netherlands = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\netherlands.png").convert_alpha()
italy = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\italy.png").convert_alpha()
singapore = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\singapore.png").convert_alpha()
japan = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\japan.png").convert_alpha()
austin = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\austin.png").convert_alpha()
mexico = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\mexico.png").convert_alpha()
saoPaulo = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\sao paulo.png").convert_alpha()
abuDhabi = pygame.image.load(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\abu dhabi.png").convert_alpha()
screen_width, screen_height = screen.get_size()
font = pygame.font.SysFont(None, 50)
selection_text = font.render(f"Track selection", False, (100, 200, 255))
selection_rect = selection_text.get_rect()
gap = 20
bw = (screen_width-40-(gap*3))/4
bh = (screen_height-60-(gap*2)-selection_rect.height)/3
#tracks and screen backgrounds scaling
background = pygame.transform.scale(background, (screen_width, screen_height))
bahrain = pygame.transform.scale(bahrain, (bw,bh))
saudiArabia = pygame.transform.scale(saudiArabia, (bw, bh))
australia = pygame.transform.scale(australia, (bw,bh))
azerbaijan = pygame.transform.scale(azerbaijan, (bw,bh))
miami = pygame.transform.scale(miami, (bw,bh))
monaco = pygame.transform.scale(monaco, (bw,bh))
spain = pygame.transform.scale(spain, (bw,bh))
canada = pygame.transform.scale(canada, (bw,bh))
austria = pygame.transform.scale(austria, (bw,bh))
britain = pygame.transform.scale(britain, (bw,bh))
hungary = pygame.transform.scale(hungary, (bw,bh))
belgium = pygame.transform.scale(belgium, (bw,bh))
netherlands = pygame.transform.scale(netherlands, (bw,bh))
italy = pygame.transform.scale(italy, (bw,bh))
singapore = pygame.transform.scale(singapore, (bw,bh))
japan = pygame.transform.scale(japan, (bw,bh))
austin = pygame.transform.scale(austin, (bw,bh))
mexico = pygame.transform.scale(mexico, (bw,bh))
saoPaulo = pygame.transform.scale(saoPaulo, (bw,bh))
abuDhabi = pygame.transform.scale(abuDhabi, (bw,bh))
#button class
class Button:
    def __init__(self, x, y, width, height, text, font, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.image = image
    # drawing the button
    def draw(self, surface):
        # detect hover
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            colour = (255, 255, 255)
        else:
            colour = (100, 200, 255)
        # drawing the rectangle outline
        pygame.draw.rect(surface, colour, self.rect, 2)
        # draw image if there is one
        if self.image:
            image_rect = self.image.get_rect(center=self.rect.center)
            surface.blit(self.image, image_rect)
        # draw text if there is any
        if self.text:
            text_surf = self.font.render(self.text, False, colour)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
    # detecting clicks
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False  
#input box class
class InputBox():
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.active = False
    #handle mouse / keyboard input
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    #drawing it
    def draw(self, surface):
        pygame.draw.rect(surface, (100,200,255), self.rect, 2)
        text_surface = self.font.render(self.text, False, (100,200,255))
        surface.blit(text_surface, (self.rect.x+10, self.rect.y+10))
#margins for button placement
margin_x, margin_y = 20, 20
#button setup -> x, y, width, height, text, fon
ds_button = Button((screen_width-margin_x-450), 50, 450, 80, "Deterministic Simulations", font)
ps_button = Button((screen_width-margin_x-450), 150, 450, 80,  "Probabilistic Simulations", font)
tutorial_button = Button((screen_width-margin_x-280), (screen_height-margin_y-180), 280, 80, "Play Tutorial", font)
info_button = Button((screen_width-margin_x-450), (screen_height-margin_y-80), 450, 80, "More about F1 strategies", font)
rightArrow_button = Button((screen_width-margin_x-100), (screen_height-margin_y-80), 100,  80, "-->",font)
leftArrow_button = Button((margin_x), (screen_height-margin_y-80), 100, 80, "<--", font)
bahrain_button = Button(margin_x, margin_y+selection_rect.height+20, bw, bh, "", font, bahrain)
saudiArabia_button = Button(screen_width-margin_x-bw, margin_y+selection_rect.height+20, bw, bh, "", font, saudiArabia) 
australia_button = Button(margin_x+bw+gap, margin_y+selection_rect.height+20, bw, bh, "", font, australia)
azerbaijan_button = Button(screen_width-margin_x-bw-gap-bw, margin_y+selection_rect.height+20, bw, bh, "", font, azerbaijan)
miami_button = Button(margin_x, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, miami)
monaco_button = Button(screen_width-margin_x-bw, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, monaco) 
spain_button = Button(margin_x+bw+gap, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, spain)
canada_button = Button(screen_width-margin_x-bw-gap-bw, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, canada)
britain_button = Button(screen_width-margin_x-bw-gap-bw, margin_y+bh+gap+bh+gap+selection_rect.height+20, bw, bh, "", font, britain) 
hungary_button = Button(margin_x+bw+gap, margin_y+bh+gap+bh+gap+selection_rect.height+20, bw, bh, "", font, hungary)
austria_button = Button(margin_x, margin_y+selection_rect.height+20, bw, bh, "", font, austria)
belgium_button = Button(screen_width-margin_x-bw, margin_y+selection_rect.height+20, bw, bh, "", font, belgium) 
netherlands_button = Button(margin_x+bw+gap, margin_y+selection_rect.height+20, bw, bh, "", font, netherlands)
italy_button = Button(screen_width-margin_x-bw-gap-bw, margin_y+selection_rect.height+20, bw, bh, "", font, italy)
singapore_button = Button(margin_x, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, singapore)
japan_button = Button(screen_width-margin_x-bw, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, japan) 
austin_button = Button(margin_x+bw+gap, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, austin)
mexico_button = Button(screen_width-margin_x-bw-gap-bw, margin_y+bh+gap+selection_rect.height+20, bw, bh, "", font, mexico)
saoPaulo_button = Button(screen_width-margin_x-bw-gap-bw, margin_y+bh+gap+bh+gap+selection_rect.height+20, bw, bh, "", font, saoPaulo) 
abuDhabi_button = Button(margin_x+bw+gap, margin_y+bh+gap+bh+gap+selection_rect.height+20, bw, bh, "", font, abuDhabi)
#menu display
def display_menu(events): 
    clicked_button = None
    #input handling
    for event in events:
        if ds_button.is_clicked(event):
            clicked_button = "ds_button"
        elif ps_button.is_clicked(event):
            clicked_button = "ps_button"
        elif tutorial_button.is_clicked(event):
            clicked_button = "tutorial_button"
        elif info_button.is_clicked(event):
            clicked_button = "info_button"
    #drawing the menu
    screen.blit(background, (0, 0))
    ds_button.draw(screen)
    ps_button.draw(screen)
    tutorial_button.draw(screen)
    info_button.draw(screen)
    return clicked_button
#initialising stuff inside the main loop
state = "menu"
simulation_type = "probabilistic"
track = None
ttemp_box, atemp_box = None, None
lttl, uttl, latl, uatl = None, None, None, None
s_box, m_box, h_box = None, None, None
track_temp, air_temp = None, None
error_time = None
s, m, h = None, None, None
sc1_box, sc2_box = None, None
starts, length = None, None
ttv, atv, scv, sv, mv, hv = False, False, True, False, False, False
mps = False
#stuff that should definitely be outside the loop
ttemp_text = font.render("Track surface temperature:", False, (100, 200, 255))
ttemp_width = ttemp_text.get_rect().width
atemp_text = font.render("Air temperature: ", False, (100, 200, 255))
compound_text = font.render("Tyre compounds: ", False, (100, 200, 255))
climits_text = font.render("Limits: (S, M, H) = (0-8, 1-3, 1-2)", None, (100, 200, 255))
sc_text = font.render("Safety cars (0-6): start lap, length", False, (100, 200, 255))
sce_text = font.render("Unavailable for this simulation type", False, (255, 100, 100))
error_text = font.render("Invalid input(s). Try again", False, (255, 100, 100))
et_width = error_text.get_rect().width
#main calculation method, gonna use queue for the main loop for this
result_queue = queue.Queue()
def performAllCalculations(s, m, h, mps, track, track_temp, air_temp, simulation_type): #all used variables, st probably wont get used
    allStrategies = generateCompleteStrategySequence(s, m, h, mps, track)
    results = 0 
    #the rest of the calculation code
    return None #many many variables
calculation_started = False
calculation_completed = False
allStrategies = None
#main loop
while True:
    events = pygame.event.get()
    for event in events:
        #handling inputs
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN and state == "options":
                try:     
                    track_temp = float(ttemp_box.text)
                    if track_temp < lttl or track_temp > uttl:
                        raise ValueError
                    ttv = True
                except ValueError:
                    error_time = pygame.time.get_ticks()
                try:
                    air_temp = float(atemp_box.text)
                    if air_temp < latl or air_temp > uatl:
                        raise ValueError
                    atv = True
                except ValueError:
                    error_time = pygame.time.get_ticks()
                try:
                    s = int(s_box.text)
                    if s < 0 or s > 8:
                        raise ValueError
                    sv = True
                except ValueError:
                    error_time = pygame.time.get_ticks()
                try:
                    m = int(m_box.text)
                    if m < 1 or m > 3:
                        raise ValueError
                    mv = True
                except ValueError:
                    error_time = pygame.time.get_ticks()
                try:
                    h = int(h_box.text)
                    if h < 1 or h > 2:
                        raise ValueError
                    hv = True
                except ValueError:
                    error_time = pygame.time.get_ticks()
                if track is not None and simulation_type == "deterministic":
                    try:
                        starts = sc1_box.text
                        length = sc2_box.text
                        if not isValidScSequence(starts, length, track):
                            scv = False
                            raise ValueError
                    except ValueError:
                        error_time = pygame.time.get_ticks()
        if state == "options" and ttemp_box is not None:
            ttemp_box.handle_event(event)
        if state == "options" and atemp_box is not None:
            atemp_box.handle_event(event)
        if state == "options" and s_box is not None:
            s_box.handle_event(event)
        if state == "options" and m_box is not None:
            m_box.handle_event(event)
        if state == "options" and h_box is not None:
            h_box.handle_event(event)
        if state == "options" and sc1_box is not None:
            sc1_box.handle_event(event)
        if state == "options" and sc2_box is not None:
            sc2_box.handle_event(event)
    #menu
    if state == "menu":
        clicked_button = display_menu(events)
        if clicked_button == "ds_button":
            state = "selection_1"
            simulation_type = "deterministic"
            pygame.time.wait(250)
        elif clicked_button == "ps_button":
            state = "selection_1"
            simulation_type = "probabilistic"
            pygame.time.wait(250)
        elif clicked_button == "tutorial_button":
            state = "tutorial_1"
        elif clicked_button == "info_button":
            state = "info_1"
            pygame.time.wait(250)
    #tutorial
    elif state == "tutorial_1":
        screen.blit(background, (0,0))
        rightArrow_button.draw(screen)
        if rightArrow_button.is_clicked(event):
            state = "tutorial_2"
            pygame.time.wait(200)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state = "menu"
                display_menu(events)
            elif event.key == pygame.K_RIGHT:
                state = "tutorial_2"
                pygame.time.wait(200)
    elif state == "tutorial_2":
        screen.blit(background, (0,0))
        leftArrow_button.draw(screen)
        rightArrow_button.draw(screen)
        if leftArrow_button.is_clicked(event):
            state = "tutorial_1"
            pygame.time.wait(200)
        elif rightArrow_button.is_clicked(event):
            state = "tutorial_3"
            pygame.time.wait(200)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state = "menu"
                display_menu(events)
            elif event.key == pygame.K_RIGHT:
                state = "tutorial_3"
                pygame.time.wait(200)
            elif event.key == pygame.K_LEFT:
                state = "tutorial_1"
                pygame.time.wait(200)
    elif state == "tutorial_3":
        screen.blit(background, (0,0))
        leftArrow_button.draw(screen)
        if leftArrow_button.is_clicked(event):
            state = "tutorial_2"
            pygame.time.wait(200)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state = "menu"
                display_menu(events)
            elif event.key == pygame.K_LEFT:
                state = "tutorial_2"
                pygame.time.wait(200)
    #info
    elif state == "info_1":
        screen.blit(background, (0,0))
        rightArrow_button.draw(screen)
        if rightArrow_button.is_clicked(event):
            state = "info_2"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state = "menu"
                display_menu(events)
            elif event.key == pygame.K_RIGHT:
                state = "info_2"
    elif state == "info_2":
        screen.blit(background, (0,0))
        leftArrow_button.draw(screen)
        if leftArrow_button.is_clicked(event):
            state = "info_1"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state = "menu"
                display_menu(events)
            elif event.key == pygame.K_LEFT:
                state = "info_1"
    #track selection 
    elif state == "selection_1":
        screen.blit(background, (0,0))
        screen.blit(selection_text, ((screen_width/2 - selection_rect.width/2), margin_y))
        bahrain_button.draw(screen)
        saudiArabia_button.draw(screen)
        australia_button.draw(screen)
        azerbaijan_button.draw(screen)
        miami_button.draw(screen)
        monaco_button.draw(screen)
        spain_button.draw(screen)
        canada_button.draw(screen)
        britain_button.draw(screen)
        hungary_button.draw(screen)
        rightArrow_button.draw(screen)
        if rightArrow_button.is_clicked(event):
            state = "selection_2"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state = "menu"
                display_menu(events)
            elif event.key == pygame.K_RIGHT:
                state = "selection_2"
        if bahrain_button.is_clicked(event):
            track = "Bahrain"
        if saudiArabia_button.is_clicked(event):
            track = "Saudi Arabia"
        if australia_button.is_clicked(event):
            track = "Australia"
        if azerbaijan_button.is_clicked(event):
            track = "Azerbaijan"
        if miami_button.is_clicked(event):
            track = "Miami"
        if monaco_button.is_clicked(event):
            track = "Monaco"
        if spain_button.is_clicked(event):
            track = "Spain"
        if canada_button.is_clicked(event):
            track = "Canada"
        if britain_button.is_clicked(event):
            track = "Britain"
        if hungary_button.is_clicked(event):
            track = "Hungary"
        if bahrain_button.is_clicked(event) or saudiArabia_button.is_clicked(event) or australia_button.is_clicked(event) or azerbaijan_button.is_clicked(event) or miami_button.is_clicked(event) or monaco_button.is_clicked(event) or spain_button.is_clicked(event) or canada_button.is_clicked(event) or britain_button.is_clicked(event) or hungary_button.is_clicked(event):
            state = "options"
    elif state == "selection_2":
        screen.blit(background, (0,0))
        screen.blit(selection_text, ((screen_width/2 - selection_rect.width/2), margin_y))
        austria_button.draw(screen)
        belgium_button.draw(screen)
        netherlands_button.draw(screen)
        italy_button.draw(screen)
        singapore_button.draw(screen)
        japan_button.draw(screen)
        austin_button.draw(screen)
        mexico_button.draw(screen)
        saoPaulo_button.draw(screen)
        abuDhabi_button.draw(screen)
        leftArrow_button.draw(screen)
        if leftArrow_button.is_clicked(event):
            state = "selection_1"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                state = "menu"
                display_menu(events)
            elif event.key == pygame.K_LEFT:
                state = "selection_1"
        if austria_button.is_clicked(event):
            track = "Austria"
        if belgium_button.is_clicked(event):
            track = "Belgium"
        if netherlands_button.is_clicked(event):
            track = "Netherlands"
        if italy_button.is_clicked(event):
            track = "Italy"
        if singapore_button.is_clicked(event):
            track = "Singapore"
        if japan_button.is_clicked(event):
            track = "Japan"
        if austin_button.is_clicked(event):
            track = "Austin"
        if mexico_button.is_clicked(event):
            track = "Mexico"
        if saoPaulo_button.is_clicked(event):
            track = "Sao Paulo"
        if abuDhabi_button.is_clicked(event):
            track = "Abu Dhabi"
        if austria_button.is_clicked(event) or belgium_button.is_clicked(event) or netherlands_button.is_clicked(event) or italy_button.is_clicked(event) or singapore_button.is_clicked(event) or japan_button.is_clicked(event) or austin_button.is_clicked(event) or mexico_button.is_clicked(event) or saoPaulo_button.is_clicked(event) or abuDhabi_button.is_clicked(event):
            state = "options"
    #options selection
    elif state == "options":
        screen.blit(background, (0,0))
        #drawing the track lmao
        if track == "Bahrain":
            screen.blit(bahrain, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Saudi Arabia":
            screen.blit(saudiArabia, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Australia":
            screen.blit(australia, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Azerbaijan":
            screen.blit(azerbaijan, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Miami":
            screen.blit(miami, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Monaco":
            screen.blit(monaco, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Spain":
            screen.blit(spain, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Canada":
            screen.blit(canada, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Austria":
            screen.blit(austria, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Britain":
            screen.blit(britain, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Hungary":
            screen.blit(hungary, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Belgium":
            screen.blit(belgium, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Netherlands":
            screen.blit(netherlands, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Italy":
            screen.blit(italy, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Singapre":
            screen.blit(singapore, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Japan":
            screen.blit(japan, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Austin":
            screen.blit(austin, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Mexico":
            screen.blit(mexico, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Sao Paulo":
            screen.blit(saoPaulo, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        elif track == "Abu Dhabi":
            screen.blit(abuDhabi, (screen_width-margin_x-bw, (screen_height/2)-(bh/2)))
        #track related
        track_text = font.render(f"Chosen track: {track}", False, (100, 200, 255))
        text_height = track_text.get_rect().height
        screen.blit(track_text, (margin_x, margin_y))
        #laps related
        laps = getLaps(track)
        laps_text = font.render(f"No. of laps: {laps}", False, (100, 200, 255))
        screen.blit(laps_text, (margin_x, margin_y+text_height+20))
        #simulation related
        if simulation_type == "deterministic":
            sim_text = font.render("Simulation type: Deterministic", False, (100, 200, 255))
        elif simulation_type == "probabilistic":
            sim_text = font.render("Simulation type: Probabilistic", False, (100, 200, 255))
        screen.blit(sim_text, (margin_x, margin_y+(text_height*2)+40))
        #track temp related
        screen.blit(ttemp_text, (margin_x, margin_y+(th3 := text_height*3)+60))
        lttl, uttl = getTtLimit(track)
        ttl_text = font.render(f"({lttl} <= track temp <= {uttl})", False, (100, 200, 255))
        if ttemp_box is None:
            ttemp_box = InputBox(margin_x+ttemp_width+20, margin_y+th3+60, 200, 60, font)
        ttemp_box.draw(screen)
        screen.blit(ttl_text, (margin_x, margin_y+(text_height*4+80)))
        #air temp related
        screen.blit(atemp_text, (margin_x, margin_y+(th5 := text_height*5)+100))
        latl, uatl = getAtLimit(track)
        atl_text = font.render(f"({latl} <= air temp <= {uatl})", False, (100, 200, 255))
        atl_width = atl_text.get_rect().width
        screen.blit(atl_text, (margin_x, margin_y+(text_height*6)+120))
        if atemp_box is None:
            atemp_box = InputBox(margin_x+atl_width+20, margin_y+th5+100, 200, 60, font)
        atemp_box.draw(screen)
        #tyres related
        screen.blit(compound_text, (margin_x, margin_y+(text_height*7)+140))
        screen.blit(climits_text, (margin_x, margin_y+(text_height*8)+160))
        if s_box is None:
            s_box = InputBox(margin_x, margin_y+(th9 := text_height*9)+180, 60, 60, font)
        s_box.draw(screen)
        if m_box is None:
            m_box = InputBox(margin_x+80, margin_y+th9+180, 60, 60, font)
        m_box.draw(screen)
        if h_box is None:
            h_box = InputBox(margin_x+160, margin_y+th9+180, 60, 60, font)
        h_box.draw(screen)
        #SC related
        screen.blit(sc_text, (margin_x, margin_y+(th9)+260))
        if simulation_type == "deterministic":
            if sc1_box is None:
                sc1_box = InputBox(margin_x, margin_y+(th10 := text_height*10)+280, 320, 60, font)
            sc1_box.draw(screen)
            if sc2_box is None:
                sc2_box = InputBox(margin_x+340, margin_y+th10+280, 190, 60, font)
            sc2_box.draw(screen)
        else:
            screen.blit(sce_text, (margin_x, margin_y+(text_height*10)+280))
        if ttv and atv and scv and sv and mv and hv:
            state = "final"
        #error handling
        if error_time is not None:
            if pygame.time.get_ticks() - error_time < 2000:
                screen.blit(error_text, (screen_width-margin_x-et_width, margin_y))
        else:
            error_time = None
    elif state == "final":
        screen.blit(background, (0,0))
        if not calculation_started:
            if track == "Monaco":
                mps = True
            thread = threading.Thread(target=lambda: result_queue.put(performAllCalculations(s, m, h, mps, track, track_temp, air_temp, simulation_type)), daemon=True)
            thread.start()
            calculation_started = True
            if not result_queue.empty():
                result = result_queue.get() #and other variables: v1, v2....... = etc
                calculation_completed = True
            if not calculation_completed:
                #drawing the calculation animation and allat 
                pass
    #updating the display and setting the fps
    pygame.display.flip()
    clock.tick(25) 