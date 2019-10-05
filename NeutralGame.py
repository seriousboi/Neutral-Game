from animations import *
from framedata import *
from stickman import *
from AIs import *
import pygame
pygame.init()



def text(message,size,color,anchor,x,y):
    global window

    font = pygame.font.SysFont("linuxbiolinumg", size)
    text = font.render(message,True,color)
    area = text.get_rect()
    width= area.width
    height= area.height

    vect= {"topleft":[0,0],
           "bottomleft":[0,-2],
           "topright":[-2,0],
           "bottomright":[-2,-2],
           "midtop":[-1,0],
           "midleft":[0,-1],
           "midbottom":[-1,-2],
           "midright":[-2,-1],
           "center":[-1,-1]}

    x= x + vect[anchor][0]*width/2
    y= y + vect[anchor][1]*height/2

    return window.blit(text,(x,y))



def get_output(mode,side,controller,controls,events):
    if mode == "controller":
        return get_output_controller(side,controller,controls["controller"],events)
    if mode == "keyboard":
        return get_output_keyboard(side,controller,controls["keyboard"],events)
   


def get_output_keyboard(side,keyboard,controls,events):
    global key_state

    output= ["nothing",["neutral","neutral"]]

    for event in events:

        if event.type == pygame.QUIT:
            return "quit"
        
        if event.type == pygame.KEYDOWN:
            
            if event.key in controls[1]:
                output[0]= controls[1][event.key]
            if event.key in controls[0]:
                key_state[keyboard][controls[0][event.key]]= "down"

        if event.type == pygame.KEYUP:

            if event.key in controls[0]:
                key_state[keyboard][controls[0][event.key]]= "up"

    if key_state[keyboard]["down"] == "down":
        output[1][1]= "down"

    if key_state[keyboard]["up"] == "down":
        output[1][1]= "up"
        
    
    if side == "left":
        if key_state[keyboard]["left"] == "down":
            output[1][0]= "left"
        if key_state[keyboard]["right"] == "down":
            output[1][0]= "right"

    if side == "right":
        if key_state[keyboard]["right"] == "down":
            output[1][0]= "right"
        if key_state[keyboard]["left"] == "down":
            output[1][0]= "left"

    return output



def get_output_controller(side,controller,controls,events):

    output= ["nothing",["neutral","neutral"]]    
    
    for event in events:

        if event.type == pygame.QUIT:
            return "quit"

        if  event.type == pygame.JOYBUTTONDOWN and event.joy == controller and event.button in controls:
            output[0]= controls[event.button]

    if get_down_controller(controller):
        output[1][1]= "down"

    if get_up_controller(controller):
        output[1][1]= "up"
        
    if side == "left":
        if get_left_controller(controller):
            output[1][0]= "left"
        if get_right_controller(controller):
            output[1][0]= "right"
        
    if side == "right":
        if get_right_controller(controller):
            output[1][0]= "right"
        if get_left_controller(controller):
            output[1][0]= "left"
        
    return output


 
def get_right_controller(controller):
    joystick = pygame.joystick.Joystick(controller)
    
    if joystick.get_numaxes() >= 1 and joystick.get_axis(0) >= 1/5:
        return True
    if joystick.get_numhats() >= 1 and joystick.get_hat(0)[0] >= 1/5:
        return True
    return False



def get_left_controller(controller):
    joystick = pygame.joystick.Joystick(controller)
    
    if joystick.get_numaxes() >= 1 and joystick.get_axis(0) <= -1/5:
        return True
    if joystick.get_numhats() >= 1 and joystick.get_hat(0)[0] <= -1/5:
        return True
    return False

def get_up_controller(controller):
    joystick = pygame.joystick.Joystick(controller)
    
    if joystick.get_numaxes() >= 2 and joystick.get_axis(1) <= -1/5:
        return True
    if joystick.get_numhats() >= 1 and joystick.get_hat(0)[1] >= 1/5:
        return True
    return False

def get_down_controller(controller):
    joystick = pygame.joystick.Joystick(controller)
    
    if joystick.get_numaxes() >= 2 and joystick.get_axis(1) >= 1/5:
        return True
    if joystick.get_numhats() >= 1 and joystick.get_hat(0)[1] <= -1/5:
        return True
    return False



def menu_action(hitboxes_options,current_option):
    global controls,joystick_count
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT,pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION,pygame.KEYDOWN,pygame.JOYBUTTONDOWN,pygame.JOYAXISMOTION,pygame.JOYHATMOTION])

    while True:
            
        event= pygame.event.wait()

        if event.type == pygame.QUIT:
                    return ["quit"]

        if event.type == pygame.MOUSEMOTION:
            for i in range(len(hitboxes_options)):
                if hitboxes_options[i].collidepoint(event.pos):
                    return ["change option",i]

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(hitboxes_options)):
                if hitboxes_options[i].collidepoint(event.pos):
                    return ["launch option",i]

        if event.type == pygame.KEYDOWN:

            if event.key in controls[0]["keyboard"][1]:
                if controls[0]["keyboard"][1][event.key] == "light" or controls[0]["keyboard"][1][event.key] == "start":
                    return ["launch option",current_option]
                if controls[0]["keyboard"][1][event.key] == "medium":
                    return ["back"]

            if event.key in controls[0]["keyboard"][0]:
                if controls[0]["keyboard"][0][event.key] == "up":
                    return ["change option",(current_option -1)%len(hitboxes_options)]
                if controls[0]["keyboard"][0][event.key] == "down":
                    return ["change option",(current_option +1)%len(hitboxes_options)]
                
                
        if pygame.joystick.get_count() >= 1:

            if event.type == pygame.JOYBUTTONDOWN and event.joy == 0 and event.button in controls[0]["controller"]:
                if controls[0]["controller"][event.button] == "light" or controls[0]["controller"][event.button] == "start":
                    return ["launch option",current_option]
                elif controls[0]["controller"][event.button] == "medium":
                    return ["back"]

            elif get_up_controller(0):
                return ["change option",(current_option -1)%len(hitboxes_options)]
            elif get_down_controller(0):
                return ["change option",(current_option +1)%len(hitboxes_options)]
            

        
        


 
def change_controls(sate):
    global window,controls,background
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT,pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION,pygame.KEYDOWN,pygame.JOYBUTTONDOWN,pygame.JOYAXISMOTION,pygame.JOYHATMOTION])
    moves_controller= ["light","medium","heavy","throw","start"]
    moves_keyboard= ["left","right","up","down"] + moves_controller
    current_options= [0,0]
    advancements= [-1,-1]

    while True:
        window.blit(background,(0,0))
        hitbox_back= text("back",30,(0,0,0),"bottomleft",30,785)
        hitboxes_p1= draw_controls(0,400,50)
        hitboxes_p2= draw_controls(1,1200,50)
        hitboxes_options= [hitboxes_p1[0] + [hitbox_back],hitboxes_p2[0]]
        hitboxes_moves= [hitboxes_p1[1],hitboxes_p2[1]]

        for i in range(2):    
            if advancements[i] == -1:
                text(">",30,(0,0,0),"topright",hitboxes_options[i][current_options[i]][0],hitboxes_options[i][current_options[i]][1])
            else:
                text(">",30,(0,0,0),"topright",hitboxes_moves[i][advancements[i]][0],hitboxes_moves[i][advancements[i]][1])
            
        pygame.display.update()

        events= pygame.event.get()
        action_p1= control_menu_action(0,hitboxes_options[0],current_options[0],advancements[0],events)
        action_p2= control_menu_action(1,hitboxes_options[1],current_options[1],advancements[1],events)
        actions= [action_p1,action_p2]
 
        for i in range(2):
            action= actions[i]
            if action != None:
                
                if action[0] == "quit":
                    return ["quit"]
                
                if action[0] == "change option":
                    current_options[i]= action[1]

                if action[0] == "launch option":

                    if action[1] == 0:
                        if modes[i] == "controller":
                            modes[i]= "keyboard"
                        elif modes[i] == "keyboard" and pygame.joystick.get_count() >= i+1:
                            modes[i]= "controller"

                    if action[1] == 1:
                        if modes[i] == "controller":
                            controls[i]["controller"]= {}                                                                                                                                                                                                                                                                  
                        if modes[i] == "keyboard":
                            controls[i]["keyboard"]= [{},{}]
                        advancements[i]= 0


                    if action[1] == 2:
                        if i == 0:
                            controls[i]= {"keyboard":[{97:"left",100:"right",115:"down",119:"up"},{257:"light",258:"medium",259:"heavy",256:"throw",13:"start"}],"controller":{0:"light",1:"medium",2:"throw",3:"heavy",7:"start"}}
                        if i == 1:
                            controls[i]= {"keyboard":[{97:"left",100:"right",115:"down",119:"up"},{257:"light",258:"medium",259:"heavy",256:"throw",13:"start"}],"controller":{0:"light",1:"medium",2:"throw",3:"heavy",7:"start"}}

                    if action[1] == 3:
                        return ["menu"]

                if action[0] == "change control":

                    if modes[i] == "controller":
                        controls[i]["controller"][action[1]]= moves_controller[advancements[i]]
                        advancements[i]= advancements[i] + 1
                        if advancements[i] == len(moves_controller):
                            advancements[i]= -1
                    if modes[i] == "keyboard":
                        if advancements[i] <= 3:
                            controls[i]["keyboard"][0][action[1]]= moves_keyboard[advancements[i]]
                        if advancements[i] >= 4:
                            controls[i]["keyboard"][1][action[1]]= moves_keyboard[advancements[i]]
                        advancements[i]= advancements[i] + 1
                        if advancements[i] == len(moves_keyboard):
                            advancements[i]= -1
                    
                            
                        
                    


def control_menu_action(player,hitboxes_options,option,advancement,events):
    global modes
    
    for event in events:

        if event.type == pygame.QUIT:
                    return ["quit"]

        if advancement == -1:
                
            if event.type == pygame.MOUSEMOTION:
                for i in range(len(hitboxes_options)):
                    if hitboxes_options[i].collidepoint(event.pos):
                        return ["change option",i]
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(hitboxes_options)):
                    if hitboxes_options[i].collidepoint(event.pos):
                        return ["launch option",i]

            if  modes[player] == "controller":

                if event.type == pygame.JOYBUTTONDOWN and event.joy == player and event.button in controls[player]["controller"]:
                    if controls[player]["controller"][event.button] == "light" or controls[player]["controller"][event.button] == "start":
                        return ["launch option",option]

                elif get_up_controller(player):
                    return ["change option",(option -1)%len(hitboxes_options)]
                elif get_down_controller(player):
                    return ["change option",(option +1)%len(hitboxes_options)]

            if modes[player] == "keyboard" and event.type == pygame.KEYDOWN:

                if event.key in controls[player]["keyboard"][1]:
                    if controls[player]["keyboard"][1][event.key] == "light" or controls[player]["keyboard"][1][event.key] == "start":
                        return ["launch option",option]

                if event.key in controls[player]["keyboard"][0]:
                    if controls[player]["keyboard"][0][event.key] == "up":
                        return ["change option",(option -1)%len(hitboxes_options)]
                    if controls[player]["keyboard"][0][event.key] == "down":
                        return ["change option",(option +1)%len(hitboxes_options)]

        else:
            
            if modes[player] == "controller" and event.type == pygame.JOYBUTTONDOWN and event.joy == player:
                return ["change control",event.button]

            if modes[player] == "keyboard" and event.type == pygame.KEYDOWN:
                return ["change control",event.key]
                
                
            
        
def draw_controls(player,x,y):
    global modes,controls
    mode= modes[player]
    player_controls= controls[player][mode]

    hitboxes_options= []
    hitboxes_options= hitboxes_options + [text("switch device",30,(0,0,0),"midtop",x,y+40)]
    hitboxes_options= hitboxes_options + [text("change controls",30,(0,0,0),"midtop",x,y+80)]
    hitboxes_options= hitboxes_options + [text("reset controls",30,(0,0,0),"midtop",x,y+120)]
    text("Player "+str(player+1)+": "+mode,30,(0,0,0),"midtop",x,y)

    i= 0
    moves= []
    hitboxes_moves= []
    if mode == "keyboard":
        moves= ["left","right","up","down"]
        for move in moves:
            key= find_key(player_controls[0],move)
            hitboxes_moves= hitboxes_moves + [text(move+": "+str(key),30,(0,0,0),"midtop",x,y+200+40*i)]
            i= i+1
            
        moves= ["light","medium","heavy","throw","start"]
        for move in moves:
            key= find_key(player_controls[1],move)
            hitboxes_moves= hitboxes_moves + [text(move+": "+str(key),30,(0,0,0),"midtop",x,y+200+40*i)]
            i= i+1

    if mode == "controller":
        moves= ["light","medium","heavy","throw","start"]
        for move in moves:
            key= find_key(player_controls,move)
            hitboxes_moves= hitboxes_moves + [text(move+": "+str(key),30,(0,0,0),"midtop",x,y+200+40*i)]
            i= i+1

    return [hitboxes_options,hitboxes_moves]
 


def find_key(dic,value):
    for key in dic:
        if dic[key]==value:
            return key
    return ""



def get_body(player,state,body):
    global stickman,sprites,idle,animations_
    ways= {(0,"neutral"):"neutral",(0,"crouch"):"crouch",(0,"left"):"back",(0,"right"):"forward",(1,"neutral"):"neutral",(1,"crouch"):"crouch",(1,"left"):"forward",(1,"right"):"back"}
    if state[0] in ["startup","recovery","hitrecovery","blockrecovery"]:
        if state[1] == 0:
            if state[0] == "startup":
                return animate_stickman(stickman,animations_[state[2]][state[0]][0])
            elif state[0] in ["recovery","hitrecovery","blockrecovery"]:
                return animate_stickman([sprites[state[2]]["proportions"],sprites[state[2]]["positions"]],animations_[state[2]][state[0]][0])
        else:
            return animate_stickman(body,animations_[state[2]][state[0]][state[1]])
    elif state[0] in ["active"]:
        return [sprites[state[2]]["proportions"],sprites[state[2]]["positions"]]
    elif state[0] in ["neutral","left","right"]:
        way= ways[(player,state[0])]
        if state[1] == 0:
            return animate_stickman(stickman,animations_[way][(state[1])%len(animations_[way])])
        else:
            return animate_stickman(body,animations_[way][(state[1])%len(animations_[way])])
    elif state[0] == "crouch":
        if state[1] == 0:
            return animate_stickman([sprites["crouch"]["proportions"],sprites["crouch"]["positions"]],animations_["crouch"][(state[1])%len(animations_["crouch"])])
        else:
            return animate_stickman(body,animations_["crouch"][(state[1])%len(animations_["crouch"])])
    else:
        return stickman



def get_body_color(state):
    if state[0] == "hitstun":
        if state[1]%2 == 0:
            return (150,50,50)
    elif state[0] == "blockstun":
        if state[1]%2 == 0:
            return (50,50,150)
    return (50,50,50)
   


def draw_scene(pos,bodies,colors,lifes,time,fps):
    global window,background,sprites

    window.blit(background,(0,0))
    draw_stickman(window,bodies[0][0],bodies[0][1],colors[0],10,pos[0]-80,560)
    draw_stickman(window,bodies[1][0],mirror(bodies[1][1]),colors[1],10,pos[1]+80,560)
    rec_1= pygame.Surface((600,40))
    rec_2= pygame.Surface((600,40))
    rec_1.set_alpha(128)
    rec_2.set_alpha(128)
    rec_1.fill((200,200,200))
    rec_2.fill((200,200,200))
    window.blit(rec_1,(150,50))
    window.blit(rec_1,(850,50))
    pygame.draw.rect(window,(200, 200,200),(150+(1000-lifes[0])*6/10,50,lifes[0]*6/10,40),0)
    pygame.draw.rect(window,(200, 200,200),(850,50,lifes[1]*6/10,40),0)
    pygame.draw.rect(window,(100,100,100),(150,50,600,40),3)
    pygame.draw.rect(window,(100,100,100),(850,50,600,40),3)
    text(str(time),60,(50,50,50),"midtop",800,35)
    text(fps+" fps",15,(0,0,0),"topleft",15,15)

    

def draw_hitboxes(hurtboxes,hitboxes):
    for i in range(2):
        pygame.draw.line(window,(250,200,50),(hurtboxes[i],400),(hurtboxes[i],700),2)
        if hitboxes[i] != None:
            pygame.draw.line(window,(250,50,50),(hitboxes[i],400),(hitboxes[i],700),2)
    return


def is_blocking(state,player):

    if player == 0:
        if state[0] in ["left","crouch","blockstun"]:
            return True
    else:
        if state[0] in ["right","crouch","blockstun"]:
            return True
    return False



def ready(state):
    global window,controls,background,stickman
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT,pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN,pygame.JOYBUTTONDOWN])
    states= [["neutral",0,None],["neutral",0,None]]
    players_ready= ["not ready","not ready"]
    bodies= [stickman,stickman]
    hitboxes= []
    hitboxes= hitboxes + [text(players_ready[0],30,(50,50,50),"midbottom",560,380)]
    hitboxes= hitboxes + [text(players_ready[1],30,(50,50,50),"midbottom",1040,380)]
    hitboxes= hitboxes + [text("back",30,(0,0,0),"bottomleft",30,785)]
    
    while True:
        events= pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return ["quit"]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(hitboxes)):
                    if hitboxes[i].collidepoint(event.pos):
                        if i in [0,1]:
                            players_ready[i]= "ready"
                        elif i == 2:
                            return ["menu"]
            elif event.type == pygame.JOYBUTTONDOWN and event.button in controls[event.joy]["controller"] and controls[event.joy]["controller"][event.button] == "light":
                players_ready[event.joy]= "ready"
            elif event.type == pygame.KEYDOWN:
                if event.key in controls[0]["keyboard"][1]:
                    if controls[0]["keyboard"][1][event.key] == "light":
                        players_ready[0]= "ready"
                    elif controls[0]["keyboard"][1][event.key] == "medium":
                        return ["menu"]
                if event.key in controls[1]["keyboard"][1]:
                    if controls[1]["keyboard"][1][event.key] == "light":
                        players_ready[1]= "ready"
        
        window.blit(background,(0,0))
        bodies= [get_body(0,states[0],bodies[0]),get_body(1,states[1],bodies[1])]
        draw_stickman(window,bodies[0][0],bodies[0][1],(50,50,50),10,520,560)
        draw_stickman(window,bodies[1][0],mirror(bodies[1][1]),(50,50,50),10,1080,560)
        text(players_ready[0],30,(50,50,50),"midbottom",560,380)
        text(players_ready[1],30,(50,50,50),"midbottom",1040,380)
        text("back",30,(0,0,0),"bottomleft",30,785)
        pygame.display.update()
        
        if players_ready[0] == "ready" and players_ready[1] == "ready":
            pygame.time.wait(500)
            return ["play",states[0][1]]

        states[0][1]= states[0][1] + 1
        states[1][1]= states[1][1] + 1
        pygame.time.wait(30)
        


 
def play(state):
    global window,controls,background,key_state,frame_data
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.KEYUP,pygame.KEYDOWN,pygame.JOYBUTTONDOWN,pygame.QUIT])
    key_state=[{"left":"up","right":"up","down":"up","up":"up"},{"left":"up","right":"up","down":"up","up":"up"}]
    not_free= ["startup","active","recovery","hitrecovery","blockrecovery","hitstun","blockstun"]
    free= ["neutral","left","right","crouch"]
    states= [["neutral",state[1],None],["neutral",state[1],None]]
    bodies= [stickman,stickman]
    lifes=[1000,1000]
    pos= [600,1000]
    hurtboxes= [600,1000]
    hitboxes= [None,None]
    outputs=[0,0]
    speeds=[[8,10],[10,8]]
    time= 99
    clock =pygame.time.Clock()
    ticks= 0
    fps= "0"

    while True:
        events= pygame.event.get()
        outputs[0]= get_output(modes[0],"left",0,controls[0],events)
        outputs[1]= get_output(modes[1],"right",1,controls[1],events)

        

        for i in range(2):

            if outputs[i] == "quit":
                return ["quit"]

            elif hitboxes[1-i] != None and (1-2*i)*(hurtboxes[i]-hitboxes[1-i]) >= 0:
                if is_blocking(states[i],i):
                    lifes[i]= max(lifes[i] - frame_data[states[1-i][2]]["chip"],0)
                    states[i]= ["blockstun",0,states[1-i][2]]
                    states[1-i]= ["blockrecovery",0,states[1-i][2]]
                    hurtboxes[i]= pos[i]
                    hitboxes[i]= None
                    hitboxes[1-i]= None
                
                elif not is_blocking(states[i],i):
                    lifes[i]= max(lifes[i] - frame_data[states[1-i][2]]["damage"],0)
                    states[i]= ["hitstun",0,states[1-i][2]]
                    states[1-i]= ["hitrecovery",0,states[1-i][2]]
                    hurtboxes[i]= pos[i]
                    hitboxes[i]= None
                    hitboxes[1-i]= None

            elif states[i][0] in not_free:

                if states[i][1] >= frame_data[states[i][2]][states[i][0]]-1:

                    if states[i][0] == "startup":
                        states[i][0]= "active"
                        states[i][1]= 0
                        hurtboxes[i]= pos[i] + (1-2*i)*frame_data[states[i][2]]["hurtbox"]
                        hitboxes[i]= pos[i] + (1-2*i)*frame_data[states[i][2]]["hitbox"]
                    elif states[i][0] == "active":
                        states[i][0]= "recovery"
                        states[i][1]= 0
                        hitboxes[i]= None
                    elif states[i][0] == "recovery":
                        states[i]= ["neutral",0,None]
                        hurtboxes[i]= pos[i]
                    elif states[i][0] == "hitrecovery":
                        states[i]= ["neutral",0,None]
                    elif states[i][0] == "blockrecovery":
                        states[i]= ["neutral",0,None]
                    elif states[i][0] == "hitstun":
                        states[i]= ["neutral",0,None]
                    elif states[i][0] == "blockstun":
                        states[i]= ["neutral",0,None]
                        hurtboxes[i]= pos[i]

                else:
                    states[i][1]= states[i][1] + 1

                if states[i][0] in ["hitrecovery","blockrecovery","hitstun","blockstun"]:
                    pos[i]= max(min(pos[i] + (1-2*i)*frame_data[states[i][2]]["pushback"][states[i][0]],1500),100)
                    hurtboxes[i]= pos[i]

            elif outputs[i][1][0] == "left" and outputs[i][0] == "nothing" and states[i][0] in free:
                if outputs[i][1][1] == "down" and i == 0:
                    if states[i][0] == "crouch":
                        states[i][1] = states[i][1] + 1
                    else:
                        states[i][0] = "crouch"
                        states[i][1] = 0
                else:
                    if (i==0 or pos[1] >= pos[0]) and pos[i] >= 100:
                        pos[i]= pos[i] - speeds[i][0]
                        hurtboxes[i]= pos[i]
                    if states[i][0] == "left":
                        states[i][1] = states[i][1] + 1
                    else:
                        states[i][0] = "left"
                        states[i][1] = 0
                

            elif outputs[i][1][0] == "right" and outputs[i][0] == "nothing" and states[i][0] in free:
                if outputs[i][1][1] == "down" and i == 1:
                    if states[i][0] == "crouch":
                        states[i][1] = states[i][1] + 1
                    else:
                        states[i][0] = "crouch"
                        states[i][1] = 0
                else:
                    if (i==1 or pos[0] <= pos[1]) and pos[i] <= 1500:
                        pos[i]= pos[i] + speeds[i][1]
                        hurtboxes[i]= pos[i]
                    if states[i][0] == "right":
                        states[i][1] = states[i][1] + 1
                    else:
                        states[i][0] = "right"
                        states[i][1] = 0
                

            elif outputs[i][1][0] == "neutral" and outputs[i][0] == "nothing" and states[i][0] in free:
                if states[i][0] == "neutral":
                    states[i][1] = states[i][1] + 1
                else:
                    states[i][0] = "neutral"
                    states[i][1] = 0

            elif outputs[i][0] in ["light","medium","heavy"] and states[i][0] in free:
                states[i]= ["startup",0,outputs[i][0]]
                
                

    
        bodies= [get_body(0,states[0],bodies[0]),get_body(1,states[1],bodies[1])]
        colors= [get_body_color(states[0]),get_body_color(states[1])]
        draw_scene(pos,bodies,colors,lifes,time,fps)
        #draw_hitboxes(pos,hurtboxes,hitboxes)
        pygame.display.update()

        ticks= ticks + clock.tick()
        if ticks >= 1000:
            time= max(time -1,0)
            ticks= ticks -1000
        fps= str(int(clock.get_fps()))

        if 0 in lifes or time == 0:

            if lifes[0] == lifes[1]:
                return ["end","draw"]
            elif lifes[0] > lifes[1]:
                return ["end","p1 wins"]
            elif lifes[0] < lifes[1]:   
                return ["end","p2 wins"]



def end(state):
    global window,background
    window.blit(background,(0,0))
    text(state[1],100,(0,0,0),"center",800,350)
    pygame.display.update()
    pygame.time.wait(1500)
    return ["ready"]



def menu(state):
    global window,controls,background
    pygame.event.set_blocked(None)
    hitboxes_options= []
    hitboxes_options= hitboxes_options + [text("play",30,(0,0,0),"midtop",800,350)]
    hitboxes_options= hitboxes_options + [text("controls",30,(0,0,0),"midtop",800,400)]
    hitboxes_options= hitboxes_options + [text("quit",30,(0,0,0),"midtop",800,450)]
    options= ["ready","controls","quit"]
    current_option= 0


    while True:
        window.blit(background,(0,0))
        text("play",30,(0,0,0),"midtop",800,350)
        text("controls",30,(0,0,0),"midtop",800,400)
        text("quit",30,(0,0,0),"midtop",800,450)
        text(">",30,(0,0,0),"topright",hitboxes_options[current_option][0],hitboxes_options[current_option][1])
        pygame.display.update()

        action= menu_action(hitboxes_options,current_option)

        if action[0] == "quit":
            return action

        elif action[0] == "change option":
            current_option= action[1]

        elif action[0] == "launch option":
            return [options[action[1]]]



def main():
    global window,modes,controls,background
    window = pygame.display.set_mode((1600,800))
    pygame.display.set_caption("NeutralGame (work in progress)")

    background= pygame.image.load("data/backgrounds/summer landscape.png")
    controls= [
    {"keyboard":[{97:"left",100:"right",115:"down",119:"up"},{257:"light",258:"medium",259:"heavy",256:"throw",13:"start"}],"controller":{0:"light",1:"medium",2:"throw",3:"heavy",7:"start"}},
    {"keyboard":[{276:"left",275:"right",274:"down",273:"up"},{49:"light",50:"medium",51:"heavy",52:"throw",27:"start"}],"controller":{0:"light",1:"medium",2:"throw",3:"heavy",7:"start"}}]
    modes= ["keyboard","keyboard"]
    state= ["menu"]

    joystick_count = pygame.joystick.get_count()
    for i in range(min(2,joystick_count)):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        modes[i]= "controller"
        
    while state[0] != "quit":

        if state[0] == "menu":
            state= menu(state)
        if state[0] == "controls":
            state= change_controls(state)
        if state[0] == "ready":
            state= ready(state)
        if state[0] == "play":
            state= play(state)
        if state[0] == "end":
            state= end(state)
            
    pygame.display.quit()
    




        

    





main()









