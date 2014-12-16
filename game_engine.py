#!/usr/bin/python

__author__ = 'thienbao'
import subprocess
import shlex
import sys
import os
import random
import operator
import time

class Lord:

    def __init__(self, strength):
        self.real_intimacy      = [0, 0, 0, 0]
        self.reveal_intimacy    = [0, 0, 0, 0]
        self.nighttime_visit    = [0, 0, 0, 0]
        self.strength =  strength

    def increase_intimacy_degree(self, player_id, daily_or_nightime):
        if player_id in range(0, len(self.real_intimacy)):
            if daily_or_nightime == "D":
                self.real_intimacy[player_id]   += 1
                self.reveal_intimacy[player_id] += 1
            else:
                self.real_intimacy[player_id] += 2
                self.nighttime_visit[player_id] += 1

    def reset_nighttime_intimacy(self):
        self.nighttime_visit = [0, 0, 0, 0]

    def get_nighttime_visit_str(self):
        return "%d" % sum(self.nighttime_visit)

    def provide_military_force(self, player_id):
        max_value = max(self.real_intimacy)
        min_value = min(self.real_intimacy)
        num_max   = self.real_intimacy.count(max_value)
        num_min   = self.real_intimacy.count(min_value)
        if self.real_intimacy[player_id] == max_value:
            return self.strength * 1.0 / num_max
        elif self.real_intimacy[player_id] == min_value:
            return 0 - self.strength * 1.0 / num_min
        else:
            return 0

    def get_strength(self):
        return self.strength

    def get_reveal_intimacy_str(self, player_id):
        using_initimacy = self.reveal_intimacy
        initimacy = list(map(str,using_initimacy[player_id:] + using_initimacy[:player_id]))
        return " ".join(initimacy)
    
    def get_real_intimacy_str(self, player_id):
        return "%d" % self.real_intimacy[player_id]
    

def execute_process(cmd):
    if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return process
    else:
        print "%s is not existed or executable" % cmd
        return None

def write_to_process(value, process):
    process.stdin.write("%s\n" % value)

def read_from_process(process):
    line = process.stdout.readline()
    return line.strip()

def flush_process(process):
    process.stdin.flush()

def close_process(process):
    process.stdin.close()
    process.stdout.close()

def create_lord():
    lords = []
    for i in range(6):
        lord = Lord(random.randint(3,6))
        lords.append(lord)
    return lords


def main():
    if len(sys.argv) != 5:
        print "Usage: game_engine.py [player1] [player2] [player3] [player4]\n"
        sys.exit(1)

    print "Generating lords...."
    lords = create_lord()
    print "Lords generation done."
    print "Initializing players..."
    players = list()
    for i in range(1,len(sys.argv)):
        player = execute_process(sys.argv[i])
        if not player:
            print "Usage: game_engine.py [player1] [player2] [player3] [player4]"
            sys.exit(1)
        else:
            players.append(player)
    print "Done initializing players."

    # game loop
    for i in range(len(players)):
        player = players[i]
        ready = read_from_process(player)
        print "AI%d>>%s" % (i, ready)
        if ready == "READY":
            pass
            #print "AI%d>>READY" % i
        else:
            pass
            #print "AI%d>>not READY.Remove it from." %i
    
    for i in range(len(players)):
        player = players[i]
        print "AI%d>>Writing to stdin. Waiting for stdout." % i
        print "9 4 6"
        write_to_process("9 4 6", player)
        print " ".join(["%d" % lord.get_strength() for lord in lords ])
        write_to_process("%s" % " ".join(["%d" % lord.get_strength() for lord in lords ]), player)
    
    for turn in range(9):
        # day turn
        if turn % 2 == 0:
            for i in range(len(players)):
                player = players[i]
                print "(Turn %d)AI%d>>Writing to stdin. Waiting for stdout." % (turn+1, i) 
                
                print "%d D" % (turn+1)
                write_to_process("%d D" % (turn+1), player)
                # reveal intimacy 
                for lord in lords:
                    print "%s" % lord.get_reveal_intimacy_str(i)
                    write_to_process(lord.get_reveal_intimacy_str(i), player)
                
                # real intimacy 
                print "%s" % " ".join( [lord.get_real_intimacy_str(i) for lord in lords] )
                write_to_process(" ".join( [lord.get_real_intimacy_str(i) for lord in lords] ), player)
                # nighttime negotiation time
                print "%s" % " ".join( [lord.get_nighttime_visit_str() for lord in lords] )
                write_to_process(" ".join( [lord.get_nighttime_visit_str() for lord in lords] ), player)
                
                # flush so that the child process can read it 
                flush_process(player)
                result = read_from_process(player)
                lord_idx = list(map(int, result.split()))
                for idx in lord_idx:
                    lords[idx].increase_intimacy_degree(i, "D")
                
        else:
        # night turn
            for lord in lords:
                lord.reset_nighttime_intimacy()
            for i in range(len(players)):
                player = players[i]
                print "(Turn %d)AI%d>>Writing to stdin" % (turn+1, i) 
                
                print "%d N" % (turn+1)
                write_to_process("%d N" % (turn+1), player)
                # reveal intimacy 
                for lord in lords:
                    print "%s" % lord.get_reveal_intimacy_str(i)
                    write_to_process(lord.get_reveal_intimacy_str(i), player)
                
                # real intimacy 
                print "%s" % " ".join( [lord.get_real_intimacy_str(i) for lord in lords] )
                write_to_process(" ".join( [lord.get_real_intimacy_str(i) for lord in lords] ), player)
                
                # flush so that the child process can read it 
                flush_process(player)
                result = read_from_process(player)
                lord_idx = list(map(int, result.split()))
                for idx in lord_idx:
                    lords[idx].increase_intimacy_degree(i, "N")

        # print result 
        print "(Turn %d)Result>>" % (turn+1)
        scores = {}
        for i in range(len(players)):
            score_i = sum([lord.provide_military_force(i) for lord in lords])
            scores[i] = score_i
        sorted_items = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        for item in sorted_items:
            print "Player %d>> score=(%f)" % (item[0], item[1])

        time.sleep(1)
    
    for player in players:
        close_process(player)
    
if __name__ == "__main__":
    main()
