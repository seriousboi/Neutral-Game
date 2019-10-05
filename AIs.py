memory= 0



def ai_combo_block(player,states):
    global memory
    
    if states[player][0] == "hitstun":
        memory= 30
        
    if memory == 0:
        return ["nothing",["neutral","neutral"]]
    
    else:
        memory= memory - 1
        if player == 0: 
            return ["nothing",["left","down"]]
        if player == 1:
            return ["nothing",["right","down"]]



def ai_block(player):
    if player == 0: 
        return ["nothing",["left","down"]]
    if player == 1:
        return ["nothing",["right","down"]]


def ai_reversal(player,states,reversal):
    global memory
    
    if states[player][0] == "blockstun":
        memory= 10
        
    if memory == 0:
        return ai_block(player)
    
    else:
        memory= memory - 1
        if player == 0: 
            return [reversal,["neutral","neutral"]]
        if player == 1:
            return [reversal,["neutral","neutral"]]
    
