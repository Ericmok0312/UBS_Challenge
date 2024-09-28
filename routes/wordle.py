import json
import logging

from flask import request

from routes import app
import random

class WordleSolver:
    def __init__(self):
        self.wrong = [0] * 26
        self.halfCorrect = {}
        self.confirm = ["none"] * 5
        self.count = 0

    def solve(self, prevGuess, evaluation) -> dict:
        for i in range(5):
            if evaluation[i] == '?':
                continue
            elif evaluation[i] == '-':
                self.wrong[ord(prevGuess[i]) - ord('a')] = -1
            elif evaluation[i] == 'X':
                if prevGuess[i] not in self.halfCorrect:
                    self.halfCorrect[prevGuess[i]] = [i]
                else:
                    self.halfCorrect[prevGuess[i]].append(i)
            else:
                self.confirm[i] = prevGuess[i]
                # if prevGuess[i] in self.halfCorrect:
                #     del self.halfCorrect[prevGuess[i]]
                    
        nextGuess = ""
         
        for i in range(5):
            if self.confirm[i] != "none":
                nextGuess += self.confirm[i]
                continue
            else:

                for val in self.halfCorrect.keys():
                    if i not in self.halfCorrect[val]:
                        nextGuess += self.confirm[i]

                        break
                    


            j = random.choice(range(26))
            while not found:
                if self.wrong[j] == 0:
                    nextGuess += chr(97 + j)   
                    found = True
        
        self.count += 1
        
        return {"newGuess": nextGuess}



solver = WordleSolver()

# @app.route('/wordle-game', methods=['POST'])
@app.route('/wordle-game', methods=['POST'])
def solve_wordle():
    


    if solver.count == 0:
        solver.count += 1
        return {"guess": "slate"}
    
    data = request.get_json()
    
    logging.info("data sent for evaluation {}".format(data))
    
    
    prevGuess = data.get("guessHistory")[-1]
    evaluation = data.get("evaluationHistory")[-1]
    result = solver.solve(prevGuess, evaluation)
    
    logging.info("My result :{}".format(result))
    

    return {"guess": result["newGuess"]}