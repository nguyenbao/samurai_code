__author__ = 'thienbao'
import sys, os
import random

class Lord:
    def __init__(self, militaryStrength):
        self.militaryStrength = militaryStrength
        self.revealedIntimacy = []
        self.realIntimacy = 0

def readLine():
    return list(map(int, raw_input().split()))

def policy(lords, realLove, negotiationCount, daylight):
    command = []
    if daylight == "D":
        for i in range(5):
            command.append(str(random.randrange(numLords)))
    else:
        for i in range(2):
            command.append(str(random.randrange(numLords)))
    return command

print('READY')
sys.stdout.flush()
totalTurns, numDaimyo, numLords = readLine()
militaryStrength = readLine()
lords = []

for i in range(numLords):
    lords.append(Lord(militaryStrength[i]))

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
