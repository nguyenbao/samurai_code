__author__ = 'thienbao'
import subprocess
import shlex
import sys
import os

class Lord:

    def __init__(self, strength):
        self.intimacy_degrees = (0, 0, 0, 0)
        self.strength =  strength

    def increase_intimacy_degree(self, player_id):
        if player_id in range(0, len(self.intimacy_degrees)):
            self.intimacy_degrees[player_id] += 1

    def provide_military_force(self, player_id):
        max_value = max(self.intimacy_degrees)
        min_value = min(self.intimacy_degrees)
        num_max   = self.intimacy_degrees.count(max_value)
        num_min   = self.intimacy_degrees.count(min_value)
        if self.intimacy_degrees[player_id] == max_value:
            return self.strength * 1.0 / num_max
        elif self.intimacy_degrees[player_id] == min_value:
            return 0 - self.strength * 1.0 / num_min
        else:
            return 0

def execute_process(cmd):
    if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return process
    else:
        print "%s is not existed or executable\n" % cmd
        return None

def write_to_process(value, process):
    process.stdin.write("%s\n" % value)

def read_from_process(process):
    line = process.stdout.readline()

def flush_process(process):
    process.stdin.flush()

def close_process(process):
    process.stdin.close()
    process.stdout.close()

def create_lord():
    lords = ()
    for i in range(4):
        pass
    return lords


def main():
    if len(sys.argv) != 5:
        print "Usage: game_engine.py [player1] [player2] [player3] [player4]\n"
        sys.exit(1)

    print "Generating lords....\n"
    lords = create_lord()
    print "Lords generation done.\n"
    print "Initializing players...\n"
    players = list()
    for i in range(1,len(sys.argv)):
        player = execute_process(sys.argv[i])
        if not player:
            print "Usage: game_engine.py [player1] [player2] [player3] [player4]\n"
            sys.exit(1)
        else:
            players.append(player)
    print "Done initializing players.\n"

    # game loop
    for turn in range(9):
        if turn % 2 == 0:
            # day turn
            pass
        else:
            # night turn
            pass

if __name__ == "__main__":
    main()