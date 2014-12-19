#!/usr/bin/python

__author__ = 'thienbao'
import sys, os
import random
import logging

# Check for the file .heuristic.log in the same folder 
# to see the output of this heuristic.
logging.basicConfig(filename=".heuristic.log",level=logging.DEBUG)

class Lord:
    def __init__(self, militaryStrength, lord_id):
        self.militaryStrength  = militaryStrength
        self.revealedIntimacy  = []
        self.guessRealIntimacy = []
        self.realIntimacy      = 0
        self.last_night_time_visit = 0
        self._id = lord_id
    
    def guess_strength(self, player_id):
        """ 
        Calculate strengh base on what we guessed.
        """
        max_value = max(self.guessRealIntimacy)
        min_value = min(self.guessRealIntimacy)
        max_count = self.guessRealIntimacy.count(max_value)
        min_count = self.guessRealIntimacy.count(min_value)

        if max_value == min_value:
            return 0

        if self.guessRealIntimacy[player_id] == max_value:
            return self.militaryStrength * 1.0 / max_count
        elif self.guessRealIntimacy[player_id] == min_value:
            return 0 - self.militaryStrength * 1.0 / min_count
        else:
            return 0

    def apply_guess_intimacy(self, player_id, value):
        self.guessRealIntimacy[player_id] += value


    

def readLine():
    return list(map(int, raw_input().split()))

def policy(lords, realLove, negotiationCount, daylight):
    """
    Heuristic rules
    We guess other players move by randomizing their 
    moves in this turn. Then we explore which move 
    will give us the best score.
    """
    command = []
    # Simulate the other players by randomizing. Sound very stupid^^.
    guess_players_move(lords, daylight)

    my_score = -1000000
    if daylight == "D":
        """
        A crazy fifth-level loop to explore 
        all possible move for our player.
        """
        for i1 in range(6):
            for i2 in range(i1,6):
                for i3 in range(i2,6):
                    for i4 in range(i3,6):
                        for i5 in range(i4,6):
                            cmd = [i1,i2,i3,i4,i5]
                            tmp_score = calculate_score(lords, cmd, daylight)
                            if (tmp_score > my_score):
                                my_score = tmp_score
                                command = list( map( str, cmd ) )
    else:
        for i1 in range(6):
            for i2 in range(i1,6):
                cmd = [i1, i2]
                tmp_score = calculate_score(lords, cmd, daylight)
                if (tmp_score > my_score):
                    my_score = tmp_score
                    command = list( map( str, cmd ) )
    logging.info("CMD=(%s), tmp_score=(%f)" % (' '.join(command), my_score))
    return command

def calculate_score(lords, cmd, daylight):
    for lord_id in cmd:
        lords[lord_id].apply_guess_intimacy(0, 1) if daylight == "D" else lords[lord_id].apply_guess_intimacy(0,2)
    my_score = 0
    for lord in lords:
        my_score += lord.guess_strength(0)
    for lord_id in cmd:
        lords[lord_id].apply_guess_intimacy(0, -1) if daylight == "D" else lords[lord_id].apply_guess_intimacy(0, -2)
    return my_score
        

def guess_players_move(lords, daylight, turn=0):
    """ 
    We guess other players move by supposing they 
    will use random move
    """
    for lord in lords:
        lord.guessRealIntimacy = lord.revealedIntimacy
    
    if turn == 2:
        """ Guessing the previous night time (turn 1)  move of other players """
        pass 
    elif turn == 4:
        """ Guessing the previous night time (turn 3)  move of other players """
        pass
    elif turn == 6:
        """ Guessing the previous night time (turn 5)  move of other players """
        pass 
    elif turn == 8:
        """ Guessing the previous night time (turn 7)  move of other players """
        pass
    
    # Now guessing move of other players
    # A smarter heuristic should consider the best move for each player.
    # But for now, we just random to see how it works.
    if daylight == "D":
        for i in range(1,4):
            cmd = [random.randint(0,5), random.randint(0,5), random.randint(0,5), random.randint(0,5), random.randint(0,5)]
            for lord_id in cmd:
                lords[lord_id].apply_guess_intimacy(i, 1)
    else: 
        for i in range(1,4):
            cmd = [random.randint(0,5), random.randint(0,5)]
            for lord_id in cmd:
                lords[lord_id].apply_guess_intimacy(i, 2)
    

print('READY')
sys.stdout.flush()
totalTurns, numDaimyo, numLords = readLine()
militaryStrength = readLine()
lords = []

for i in range(numLords):
    lords.append(Lord(militaryStrength[i],i))

for t in range(totalTurns):
    turn, time = raw_input().split()
    turn = int(turn)
    for i in range(numLords):
        lords[i].revealedIntimacy = readLine()
    realLove = readLine()
    for i in range(numLords):
        lords[i].realIntimacy = realLove[i]
    if time == 'D':
        negotiationCount = readLine()
    else:
        negotiationCount = [0] * numLords

    command = policy(lords, realLove, negotiationCount, time)
    print(' '.join(command))
    sys.stdout.flush()
