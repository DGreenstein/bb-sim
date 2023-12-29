import logging, logging.handlers
import sys
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
bblogs = logging.getLogger()
bblogs.setLevel(logging.NOTSET)

toFile = logging.handlers.RotatingFileHandler(filename='bbsim.log', maxBytes=102400, backupCount=10)
toFile.setLevel(logging.DEBUG)
toFile.setFormatter(logFormatter)
bblogs.addHandler(toFile)

toConsole = logging.StreamHandler(sys.stdout)
toConsole.setLevel(logging.INFO)
toConsole.setFormatter(logFormatter)
bblogs.addHandler(toConsole)

import random
import uuid

class BaseballSimulator:
    def __init__(self):
        self.outcomes = ["strike", "ball", "single", "double", "triple", "home_run", "out", "strike", "out", "ball", "out"]
        self.hometeam = ""
        self.homescore = 0
        self.awayteam = ""
        self.awayscore = 0
        self.inning = 0
        self.atbat = ""
        self.strikes = 0
        self.balls = 0
        self.outs = 0
        self.bases = [0,0,0]
        self.runs_scored = 0

    def pitch(self):
        outcome = random.choice(self.outcomes)
        if outcome == "strike":
            self.strikes += 1
            pitch_result = "Strike"
            if self.strikes == 3:
                pitch_result = "Three strikes! Batter is out!"
                self.strikes = 0
                self.balls = 0
                self.outs += 1
        elif outcome == "ball":
            self.balls += 1
            pitch_result = "Ball"
            if self.balls == 4:
                pitch_result = "Ball Four! Batter, takes your base."
                self.run_bases("single")
                self.strikes = 0
                self.balls = 0
        elif outcome in ["single", "double", "triple", "home_run"]:
            pitch_result = "It's a "+ outcome.replace('_', ' ') + "!"
            self.run_bases(outcome)
            self.strikes = 0
            self.balls = 0
        elif outcome == "out":
            pitch_result = "Out"
            self.strikes = 0
            self.balls = 0
            self.outs += 1
        bblogs.debug(f"{self.game_id}: Pitch: {pitch_result} | Current Runs: {self.runs_scored}")
        return(pitch_result)

    def run_bases(self, hit_type):
        if hit_type == 'home_run':
            self.runs_scored += sum(self.bases) + 1
            self.bases = [0, 0, 0]
            return(self.runs_scored)
        elif hit_type == 'triple':
            self.runs_scored += sum(self.bases)
            self.bases = [0, 0, 1]
            return(self.runs_scored)
        elif hit_type == 'double':
            self.runs_scored += self.bases[2] + self.bases[1]
            self.bases = [0] + [1] + self.bases[:-2]
            return(self.runs_scored)
        elif hit_type == 'single':
            if self.bases[2] == 1:
                self.runs_scored += 1
            self.bases = [1] + self.bases[:-1]
            return(self.runs_scored)
        else:
            return -1

    def reset_inning(self):
        self.strikes = 0 # clear the strike count
        self.balls = 0 # clear the ball count
        self.outs = 0 # clear the outs
        self.bases = [0,0,0] # clear the bases
        self.runs_scored = 0 # clear runs scored

    def play_inning(self):
        while self.outs < 3:
            self.pitch()

    def play_game(self, game_id = uuid.uuid4(), max_innings = 3, hometeam = "Rebels", awayteam = "Senators"):
        self.game_id = game_id
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.inning = 1
        self.atbat = "awayteam"
        while self.inning <= max_innings:
            if self.atbat == "hometeam":
                bblogs.info(f"{self.game_id}: Bottom of inning {self.inning} - {self.hometeam} at bat.")
                self.play_inning()
                bblogs.info(f"{self.game_id}: {self.hometeam} scored {self.runs_scored} runs and left {sum(self.bases)} runners on base.")
                self.homescore += self.runs_scored
                bblogs.info(f"{self.game_id}: Score - {self.awayteam}: {self.awayscore} | {self.hometeam}: {self.homescore}")
                self.reset_inning()
                self.inning += 1 # progress inning
                self.atbat = "awayteam"
            else:
                bblogs.info(f"{self.game_id}: Top of inning {self.inning} - {self.awayteam} at bat.")
                self.play_inning()
                bblogs.info(f"{self.game_id}: {self.awayteam} scored {self.runs_scored} runs and left {sum(self.bases)} runners on base.")
                self.awayscore += self.runs_scored
                bblogs.info(f"{self.game_id}: Score - {self.awayteam}: {self.awayscore} | {self.hometeam}: {self.homescore}")
                self.reset_inning()
                self.atbat = "hometeam"

        bblogs.info(str(self.game_id) + ": Game Over")
        bblogs.info(f"{self.game_id}: Final Score - {self.awayteam}: {self.awayscore} | {self.hometeam}: {self.homescore}")

def getHometeam():
    looper = True
    while looper:
        try:
            hometeam = input("Enter the name of the home team: ")
            if hometeam.isalpha():
                return(hometeam)
                looper = False
            else:
                raise TypeError
        except TypeError:
            print("Please use only letters for the team name.")
            bblogs.debug("Invalid hometeam input - " + hometeam)
            continue
        except EOFError:
            return("Rebels")
            looper = False

def getAwayteam():
    looper = True
    while looper:
        try:
            awayteam = input("Enter the name of the away team: ")
            if awayteam.isalpha():
                return(awayteam)
                looper = False
            else:
                raise TypeError
        except TypeError:
            print("Please use only letters for the team name.")
            bblogs.debug("Invalid awayteam input - " + awayteam)
            continue
        except EOFError:
            return("Senators")
            looper = False

if __name__ == "__main__":
    hometeam = getHometeam()
    bblogs.debug("Home team is " + hometeam)
    awayteam = getAwayteam()
    bblogs.debug("Away team is " + awayteam)
    innings = int(input("How many innings would you like to play?"))
    gameid = uuid.uuid4()
    simulator = BaseballSimulator()
    bblogs.info(str(gameid) + ": Game Starting")
    simulator.play_game(gameid, innings, hometeam, awayteam)
