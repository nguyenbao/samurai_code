#!/usr/bin/python

__author__ = 'thienbao'
import subprocess
import shlex
import sys
import os
import random
import operator
import time
from optparse import OptionParser

class Lord:

    def __init__(self, strength):
        self.real_intimacy      = [0, 0, 0, 0] # the real intimacy for each player
        self.reveal_intimacy    = [0, 0, 0, 0] # the reveal intimacy for each player
        self.nighttime_visit    = [0, 0, 0, 0] # this is to store visit in previous night turn
        self.nighttime_intimacy = [0, 0, 0, 0] # this is to store intimacy for night tunr 1 and 2
        self.strength           =  strength

    def increase_intimacy_degree(self, player_id, daily_or_nightime, turn=0):
        """
        increase intimacy for specific player_id
        """
        if player_id in range(0, len(self.real_intimacy)):
            if daily_or_nightime == "D":
                self.real_intimacy[player_id]   += 1
                self.reveal_intimacy[player_id] += 1
            else:
                self.real_intimacy[player_id] += 2
                self.nighttime_visit[player_id] += 1
                if turn == 1 or turn == 3:
                    self.nighttime_intimacy[player_id] += 2

    def reset_nighttime_intimacy(self):
        self.nighttime_visit = [0, 0, 0, 0]

    def get_nighttime_visit_str(self):
        return "%d" % sum(self.nighttime_visit)

    def provide_military_force(self, player_id):
        max_value = max(self.real_intimacy)
        min_value = min(self.real_intimacy)
        if max_value == min_value:
            return 0
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

    def get_reveal_intimacy_str(self, player_id, turn=0):
        using_initimacy = self.reveal_intimacy if turn <= 4 else [ i+j for i,j in zip(self.reveal_intimacy, self.nighttime_intimacy) ]
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

def terminate_all_processes(processes):
    for process in processes:
        close_process(process)
        process.terminate()

def create_lord():
    lords = []
    for i in range(6):
        lord = Lord(random.randint(3,6))
        lords.append(lord)
    return lords

def main():
    parser = OptionParser("Usage: game_engine.py [player1] [player2] [player3] [player4] <option>")
    parser.add_option("-m", dest="manually", help="Manually Continue at each turns.", action="store_true")
    parser.add_option("--sleep", dest="sleep_time", help="When auto runs, the number of seconds to sleep each turn. Default is 0.", type=int, default=0)
    parser.add_option("--time", dest="match_time", help="Number of matches to run. Default is 1.", default=1, type=int)

    options, args = parser.parse_args()
    if len(args) != 4:
        parser.print_help()
        sys.exit(1)
    
    players_win_status = [0, 0, 0, 0]
    players_name       = []

    manually   = options.manually
    sleep_time = options.sleep_time
    match_time = options.match_time

    for match_id in range(match_time):
        print "=============================="
        print "Starting match %d" % match_id
        print "Generating lords...."
        player_mitlitary_force = [0, 0, 0, 0]
        lords = create_lord()
        print "Lords generation done."
        print "Initializing players..."
        players = list()
        for i in range(0,len(args)):
            player = execute_process(args[i])
            if not player:
                print "Usage: game_engine.py [player1] [player2] [player3] [player4]"
                terminate_all_processes(players)
                sys.exit(1)
            else:
                players.append(player)
                players_name.append(args[i])
        print "Done initializing players."
    
        # game loop
        for i in range(len(players)):
            player = players[i]
            ready = read_from_process(player)
            print "AI%d>>%s" % (i, ready)
            if ready == "READY":
                pass
            else:
                pass

        for i in range(len(players)):
            player = players[i]
            print "AI%d>>Writing to stdin. Waiting for stdout." % i
            print "9 4 6"
            write_to_process("9 4 6", player)
            print " ".join(["%d" % lord.get_strength() for lord in lords ])
            write_to_process("%s" % " ".join(["%d" % lord.get_strength() for lord in lords ]), player)
        
        for turn in range(9):
            # day turn
            players_result = [None, None, None, None]
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
                    print "AI%d>>STDOUT: %s" % (i, result)
                    lord_idx = list(map(int, result.split()))
                    players_result[i] = lord_idx
                
                # Update the result to lord
                for player_id in range(len(players_result)):
                    lord_idx = players_result[player_id]
                    for idx in lord_idx:
                        lords[idx].increase_intimacy_degree(player_id, "D", turn=turn)

            else: # night turn
                for lord in lords:
                    lord.reset_nighttime_intimacy()
                for i in range(len(players)):
                    player = players[i]
                    print "(Turn %d)AI%d>>Writing to stdin. Waiting for output" % (turn+1, i) 
                
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
                    print "AI%d>>STDOUT: %s" % (i, result)
                    lord_idx = list(map(int, result.split()))
                    players_result[i] = lord_idx

                # Update the result to lord
                for player_id in range(len(players_result)):
                    lord_idx = players_result[player_id]
                    for idx in lord_idx:
                        lords[idx].increase_intimacy_degree(player_id, "N", turn=turn)

            # print result for turn 5 and turn 9
            if turn == 4 or turn == 8:
                for i in range(len(players)):
                    player_mitlitary_force[i] += sum([lord.provide_military_force(i) for lord in lords])
                print "(Turn %d)Result>>" % (turn+1)
                scores = {}
                for i in range(len(players)):
                    scores[i] = player_mitlitary_force[i]
                sorted_items = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
                for item in sorted_items:
                    print "Player %d>> score=(%f)" % (item[0], item[1])

                if turn == 8 and sorted_items[0][1] > sorted_items[1][1]: # we have a winner
                    players_win_status[sorted_items[0][0]] += 1
            if manually:
                input_from_user = raw_input("Press key for next turn>>")
            elif sleep_time > 0:
                time.sleep(sleep_time)
            
        # Close PIPE and terminate child process
        for player in players:
            close_process(player)
            player.terminate()

    # print out status:
    print "======== Overall Statistic ========="
    print "Number of match: %d" % match_time
    for i in range(len(players_win_status)):
        print "AI%d(%s) win: %d" % (i, players_name[i],players_win_status[i])
    
if __name__ == "__main__":
    main()
