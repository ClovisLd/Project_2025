import json
import random as rd
import numpy as np

message = ["Never gonna give you up",
           "Never gonna let you down",
           "Never gonna run around and desert you",
           "Never gonna make you cry",
           "Never gonna say goodbye",
           "Never gonna tell a lie and hurt you "]

empty_cell = set(range(16))
full_cell = set()
Typelf = np.array([4,4,4,4,4,4,4,4])

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
    if Pe[0] == "B":
        Typelf[0]-=1
    elif Pe[0] == "S":
        Typelf[1]-=1
    elif Pe[1] == "D":
        Typelf[2]-=1
    elif Pe[1] == "L":
        Typelf[3]-=1
    elif Pe[2] == "E":
        Typelf[4]-=1
    elif Pe[2] == "F":
        Typelf[5]-=1
    elif Pe[3] == "C":
        Typelf[6]-=1
    elif Pe[3] == "P":
        Typelf[7]=1
    
def Piece_choice(pieces, board):

    Pe = rd.choice(pieces)
    pieces.remove(Pe)
    return (Pe, pieces)


def play(board, client,lives, state, pieces:list):
    try:
        if len(pieces) > 0:
            choix, pieces = Piece_choice(pieces, board)
            
    except:
        print(f"///{board}///")
        
    print(f"\033[92m{choix}\033[0m")
    client.send(json.dumps(
        {"response": "move",
        "move": {"pos": case_choice(board),
        "piece": choix},
        "message": rd.choice(message)}
        ).encode('utf-8'))
    
    return pieces
