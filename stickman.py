import pygame,math,copy
pi= math.pi



def draw_stickman(window,proportions,positions,color,width,x,y):

    body_lenght= proportions[0]
    shoulders_lenght= proportions[1]
    biceps_lenght= proportions[2]
    forearm_lenght= proportions[3]
    hips_lenght= proportions[4]
    thigh_lenght= proportions[5]
    calf_lenght= proportions[6]
    foot_lenght= proportions[7]
    neck_lenght= proportions[8]
    head_size= proportions[9]

    body_rot= positions[0]
    shoulders_rot= positions[1]
    right_biceps_rot= positions[2]
    left_biceps_rot= positions[3]
    right_forearm_rot= positions[4]
    left_forearm_rot= positions[5]
    hips_rot= positions[6]
    right_thigh_rot= positions[7]
    left_thigh_rot= positions[8]
    right_calf_rot= positions[9]
    left_calf_rot= positions[10]
    right_foot_rot= positions[11]
    left_foot_rot= positions[12]
    neck_rot= positions[13]
    body_pos= positions[14]

    
    pelvis= sig((x,y),body_pos)
    nape= sig(pelvis,rot((body_lenght,0),body_rot))
    pygame.draw.line(window,color,nape,pelvis, width)

    right_shoulder= sig(nape,rot((-shoulders_lenght//2,0),shoulders_rot))
    left_shoulder= sig(nape,rot((shoulders_lenght//2,0),shoulders_rot))
    pygame.draw.line(window,color,right_shoulder,left_shoulder, width)

    right_elbow= sig(right_shoulder,rot((biceps_lenght,0),right_biceps_rot))
    left_elbow= sig(left_shoulder,rot((biceps_lenght,0),left_biceps_rot))
    pygame.draw.line(window,color,right_shoulder,right_elbow, width)
    pygame.draw.line(window,color,left_shoulder,left_elbow, width)

    right_hand= sig(right_elbow,rot((forearm_lenght,0),right_forearm_rot))
    left_hand= sig(left_elbow,rot((forearm_lenght,0),left_forearm_rot))
    pygame.draw.line(window,color,right_elbow,right_hand, width)
    pygame.draw.line(window,color,left_elbow,left_hand, width)

    right_hip= sig(pelvis,rot((-hips_lenght//2,0),hips_rot))
    left_hip= sig(pelvis,rot((+hips_lenght//2,0),hips_rot))
    pygame.draw.line(window,color,right_hip,left_hip, width)
    
    right_knee= sig(right_hip,rot((thigh_lenght,0),right_thigh_rot))
    left_knee= sig(left_hip,rot((thigh_lenght,0),left_thigh_rot))
    pygame.draw.line(window,color,right_hip,right_knee, width)
    pygame.draw.line(window,color,left_hip,left_knee, width)

    right_ankle= sig(right_knee,rot((calf_lenght,0),right_calf_rot))
    left_ankle= sig(left_knee,rot((calf_lenght,0),left_calf_rot))
    pygame.draw.line(window,color,right_knee,right_ankle, width)
    pygame.draw.line(window,color,left_knee,left_ankle, width)

    right_foot= sig(right_ankle,rot((foot_lenght,0),right_foot_rot))
    left_foot= sig(left_ankle,rot((foot_lenght,0),left_foot_rot))
    pygame.draw.line(window,color,right_ankle,right_foot, width)
    pygame.draw.line(window,color,left_ankle,left_foot, width)

    head= sig(nape,rot((neck_lenght,0),neck_rot))
    pygame.draw.line(window,color,nape,head, width)
    pygame.draw.circle(window,color,(int(head[0]),int(head[1])),head_size//2)



def sig(vect_1,vect_2):
    vect_3= []
    for i in range(len(vect_1)):
        vect_3= vect_3 + [vect_1[i]+vect_2[i]]
    return vect_3



def rot(vect_1,angle):
    x= vect_1[0]
    y= vect_1[1]
    vect_2= [0,0]
    vect_2[0]= int(math.cos(angle)*x - math.sin(angle)*y)
    vect_2[1]= int(math.sin(angle)*x + math.cos(angle)*y)
    return vect_2



def mirror(positions):
    global pi
    mirror_pos= []
    for i in range(len(positions)-1):
        mirror_pos= mirror_pos + [pi-positions[i]]
    mirror_pos= mirror_pos + [(-positions[14][0],positions[14][1])]
    return mirror_pos



def fast_angle(angle_1,angle_2):
    global pi
    dist= min(abs(angle_2%(2*pi) - angle_1%(2*pi)),2*pi-abs(angle_2%(2*pi) - angle_1%(2*pi)))
    if (angle_1 + dist)%(2*pi) == angle_2%(2*pi):
        return dist
    else:
        return -dist



def test_stickman(stickman,new_stickman):
    window = pygame.display.set_mode((500,500))

    proportions= stickman[0]
    positions= stickman[1]

    new_proportions= new_stickman[0]
    new_positions= new_stickman[1]
    

    state= "original"
    done= False
    while not done:
        window.fill((200,200,200))
        if state == "original":
            draw_stickman(window,proportions,positions,(50,50,50),7,250,200)
            state = "new"
        elif state == "new":
            draw_stickman(window,new_proportions,new_positions,(50,50,50),7,250,200)
            state= "original"
        pygame.display.update()
        events= pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                done= True
                
        pygame.time.delay(500)



def animate_stickman(stickman,evol):
    proportions= stickman[0]
    positions= stickman[1]

    proportions_evol= evol[0]
    positions_evol= evol[1]

    new_proportions= copy.deepcopy(proportions)
    new_positions= copy.deepcopy(positions)

    for evolution in proportions_evol:
        new_proportions[evolution[0]]= new_proportions[evolution[0]] + evolution[1]

    for evolution in positions_evol:
        if evolution[0] == 14:
            new_positions[evolution[0]]= sig(new_positions[evolution[0]],evolution[1])
        else: 
            new_positions[evolution[0]]= new_positions[evolution[0]] + evolution[1]

    return [new_proportions,new_positions]



def fully_animate_stickman(stickman,animation):
    new_stickman= copy.deepcopy(stickman)
    for evol in animation:
        new_stickman= animate_stickman(new_stickman,evol)
    return new_stickman



def test_animation(original_stickman,animation):
    window = pygame.display.set_mode((500,500))
    
    while True:
        window.fill((200,200,200))
        stickman= copy.deepcopy(original_stickman)
        proportions= stickman[0]
        positions= stickman[1]
        draw_stickman(window,proportions,positions,(50,50,50),7,250,200)
        pygame.display.update()
        pygame.time.delay(250)
        
        for evol in animation:
            window.fill((200,200,200))
            stickman= animate_stickman(stickman,evol)
            proportions= stickman[0]
            positions= stickman[1]
            draw_stickman(window,proportions,positions,(50,50,50),7,250,200)
            pygame.display.update()
            pygame.time.delay(33)
            
            events= pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return
                    
                
                

        pygame.time.delay(250)



def generate_evolution(start_stickman,end_stickman):
    start_proportions= start_stickman[0]
    start_positions= start_stickman[1]
    end_proportions= end_stickman[0]
    end_positions= end_stickman[1]
    proportions_evol= []
    positions_evol= []
    for i in range(len(start_proportions)):
        if start_proportions[i] != end_proportions[i]:
            proportions_evol= proportions_evol + [[i,end_proportions[i]-start_proportions[i]]]         
    for i in range(len(start_positions)):
        if start_positions[i] != end_positions[i]:
            if i == 14:
                positions_evol= positions_evol + [[i,[end_positions[i][0]-start_positions[i][0],end_positions[i][1]-start_positions[i][1]]]]
            else:
                positions_evol= positions_evol + [[i,end_positions[i]-start_positions[i]]]
    return [proportions_evol,positions_evol]

    

def generate_animation(start_stickman,end_stickman,frames,precison):
    if frames <= 0:
        return [[],[]]

    start_proportions= start_stickman[0]
    start_positions= start_stickman[1]
    end_proportions= end_stickman[0]
    end_positions= end_stickman[1]

    evol= [[],[]]
    for i in range(len(start_proportions)):
        if start_proportions[i] != end_proportions[i]:
            evol[0]= evol[0] + [[i,(end_proportions[i]-start_proportions[i])/(frames)]]    
    for i in range(len(start_positions)):
        if start_positions[i] != end_positions[i]:
            if i == 14:
                evol[1]= evol[1] + [[i,[(end_positions[i][0]-start_positions[i][0])/(frames),(end_positions[i][1]-start_positions[i][1])/(frames)]]]
            else:
                if i in precison:
                    evol[1]= evol[1] + [[i,-(fast_angle(start_positions[i],end_positions[i]))/(frames)]]
                else:
                    evol[1]= evol[1] + [[i,(fast_angle(start_positions[i],end_positions[i]))/(frames)]]     

    animation= []
    for i in range(frames):
        animation= animation + [evol]

    return animation

    


























                    




