import random
from fastapi import FastAPI
from flask import request

class WordleSolver:
    def __init__(self):
        self.wrong = [0] * 26
        self.halfCorrect = {}
        self.confirm = [None] * 6
        self.count = 0

    def solve(self, prevGuess, evaluation) -> dict:
        for i in range(5):
            if evaluation[i] == '?':
                continue
            elif evaluation[i] == '-':
                self.wrong[int(prevGuess[i] - 'a')] = -1
            elif evaluation[i] == 'X':
                if not self.halfCorrect[prevGuess[i]]:
                    self.halfCorrect[prevGuess[i]] = [i]
                else:
                    self.halfCorrect[prevGuess[i]] += [i]
            else:
                self.confirm[i] = prevGuess[i]
                if prevGuess[i] in self.halfCorrect:
                    del self.halfCorrect[prevGuess[i]]
                    
        nextGuess = ""
         
        for i in range(5):
            if not self.confirm[i]:
                nextGuess += self.confirm[i]
        else:
            found = False
            for val in self.halfCorrect:
                if i not in self.halfCorrect[val]:
                    nextGuess += self.confirm[i]
                    found = True
                    break
            if not found:
                found  = False
                j = random.choice(range(26))
                while not found:
                    if self.wrong[j] == 0:
                        nextGuess += chr(97 + j)   
                        found = True
        
        self.count += 1
        
        return {"newGuess": nextGuess}

app = FastAPI()

solver = WordleSolver()

# @app.route('/wordle-game', methods=['POST'])
@app.post('/wordle-game')
def solve_wordle():
    if solver.count == 0:
        solver.count += 1
        return {"newGuess": "ideas"}
    data = request.get_json()
    prevGuess = data.get("guessHistory")[-1]
    evaluation = data.get("evaluationHistory")[-1]
    result = solver.solve(prevGuess, evaluation)
    return {"newGuess": result["newGuess"]}