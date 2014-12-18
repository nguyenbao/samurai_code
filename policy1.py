#!/usr/bin/python

__author__ = 'thienbao'
import sys, os
import random

class Lord:
    def __init__(self, militaryStrength, lord_id):
        self.militaryStrength = militaryStrength
        self.revealedIntimacy = []
        self.realIntimacy = 0
        self._id = lord_id

def readLine():
    return list(map(int, raw_input().split()))

def policy(lords, realLove, negotiationCount, daylight):
    """
    This policy is quite simple:
    Day turn: Concentrate on three most strong lords
    Night turn: Concentrate on 1 most strongest lord and 1 weakest lord
    """
    command = []
    if daylight == "D":
        for i in range(5):
            sorted_lords = sorted(lords, key=lambda lord: lord.militaryStrength, reverse=True)
            chosen_lords = sorted_lords[:3]
            command      = [ str(chosen_lords[0]._id), str(chosen_lords[0]._id), 
                        str(chosen_lords[1]._id), str(chosen_lords[1]._id), 
                        str(chosen_lords[2]._id) ]
    else:
        for i in range(2):
            sorted_lords = sorted(lords, key=lambda lord: lord.militaryStrength, reverse=True)
            strong_lords    = sorted_lords[:3]
            weak_lords      = sorted_lords[2:]
            rand_1          = random.randint(0,2)
            rand_2          = random.randint(0,1)
            command         = [ str(strong_lords[rand_1]._id), str(weak_lords[rand_2]._id) ]
    return command

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
