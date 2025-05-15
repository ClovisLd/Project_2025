import json
import random as rd
import numpy as np

message = ["Never gonna give you up",
           "Never gonna let you down",
           "Never gonna run around and desert you",
           "Never gonna make you cry",
           "Never gonna say goodbye",
           "Never gonna tell a lie and hurt you "]

# gardue en local les endroit libre 
empty_cell = set(range(16))
full_cell = set()

# liste qui dit quelle caractérisitque sont les moins présentes
Typelf = np.array([8,8,8,8,8,8,8,8])
Letter = ["B","S","D","L","E","F","C","P"]
pieces_score = {'SDEC': 0, 'SDFP': 0, 'SLEC': 0, 'SLFP': 0, 'BDFC': 0, 'BDFP': 0, 'BLEP': 0, 'BDEP': 0, 'SDFC': 0, 'SLEP': 0, 'SLFC': 0, 'BLFP': 0, 'BDEC': 0, 'BLFC': 0, 'SDEP': 0, 'BLEC': 0}

def Max_indices(in_list:list, a:int, b:int):
    if in_list[a] > in_list[b]:
        return a
    else:
        return b

def case_choice(board):
    global empty_cell, full_cell
    a =set()
    b = set()
    #keep track of the empty cell where's what piece
    for cell in empty_cell:
        if board[cell] != None:
            full_cell.add(cell)
            a.add(cell)
    
    empty_cell -= a

    for cell in full_cell:
        if board[cell] == None:
            empty_cell.add(cell)
            b.add(cell)
    
    full_cell -= b
    return rd.choice(list(empty_cell))

    
def Type_left(Pe):
    # reduit le score de chaque caractéristique des qu'elle est joué
    global Typelf
    if Pe[0] == "B":
        Typelf[0]-=1
    if Pe[0] == "S":
        Typelf[1]-=1
    if Pe[1] == "D":
        Typelf[2]-=1
    if Pe[1] == "L":
        Typelf[3]-=1
    if Pe[2] == "E":
        Typelf[4]-=1
    if Pe[2] == "F":
        Typelf[5]-=1
    if Pe[3] == "C":
        Typelf[6]-=1
    if Pe[3] == "P":
        Typelf[7]-=1
    
def Piece_choice(pieces, board):
    global pieces_score
    for i in range(0,4):
        lll = Letter[Max_indices(Typelf, 2*i , 2*i+1)]
        for ppp in pieces:
            print(f"\033[92mRemoved {Letter} from pieces\033[0m")
            if ppp[i] == lll:
                pieces_score[ppp] += 1

    print(pieces_score)
    Pe = max(pieces_score, key=pieces_score.get)
    print(Pe)
    if Pe in board:
        try:
            pieces.remove(Pe)
            Type_left(Pe)
            Piece_choice(pieces, board)
            return(Pe, pieces)
        except:
            pass
    if Pe not in pieces:
        pieces_score[Pe] = 0
        Pe = max(pieces_score, key=pieces_score.get)
    Type_left(Pe)
    pieces.remove(Pe)
    pieces_score = {'SDEC': 0, 'SDFP': 0, 'SLEC': 0, 'SLFP': 0, 'BDFC': 0, 'BDFP': 0, 'BLEP': 0, 'BDEP': 0, 'SDFC': 0, 'SLEP': 0, 'SLFC': 0, 'BLFP': 0, 'BDEC': 0, 'BLFC': 0, 'SDEP': 0, 'BLEC': 0}
    return (Pe, pieces)



def play(board, client, lives, state, pieces:list):
    # envoit le move au serveur
    choix, pieces = Piece_choice(pieces, board)
    client.send(json.dumps(
        {"response": "move",
        "move": {"pos": case_choice(board),
        "piece": choix},
        "message": rd.choice(message)}
        ).encode('utf-8'))
    
    return pieces
