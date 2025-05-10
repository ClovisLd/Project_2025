import json
import random as rd

empty_cell = set(range(16))
full_cell = set()

def case_choice(board,a = set()):
    global empty_cell, full_cell
    #keep track of the empty cell where's what piece
    for cell in empty_cell:
        if board[cell] != None:
            full_cell.add(cell)
            a.add(cell)
    empty_cell -= a
    return rd.choice(list(empty_cell))

def play(board, client, errors, lives, state, pieces):
    if len(pieces) > 0:
        choix = rd.choice(pieces)
    print(f"this the choice |||{choix}|||, ,{full_cell}")
    client.send(json.dumps(
        {"response": "move",
        "move": {"pos": case_choice(board),
        "piece": choix},
        "message": "Fun message"}
        ).encode('utf-8'))
