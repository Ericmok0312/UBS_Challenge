# import json
# import logging

# from flask import request

# from routes import app
# import random

# class WordleSolver:
#     def __init__(self):
#         self.wrong = [0] * 26
#         self.halfCorrect = {}
#         self.confirm = ["none"] * 5
#         self.count = 0
#         self.characters = "abcdefghijklmnopqrstuvwxyz"

#     def solve(self, prevGuess, evaluation) -> dict:
#         for i in range(5):
#             if evaluation[i] == '?':
#                 continue
#             elif evaluation[i] == '-':
#                 self.wrong[ord(prevGuess[i]) - ord('a')] = -1
#             elif evaluation[i] == 'X':
#                 if prevGuess[i] not in self.halfCorrect:
#                     self.halfCorrect[prevGuess[i]] = [i]
#                 else:
#                     self.halfCorrect[prevGuess[i]].append(i)
#             else:
#                 self.confirm[i] = prevGuess[i]
#                 # if prevGuess[i] in self.halfCorrect:
#                 #     del self.halfCorrect[prevGuess[i]]
                    
#         nextGuess = ""
         
#         for i in range(5):
#             if self.confirm[i] != "none":
#                 nextGuess += self.confirm[i]
#                 continue
#             else:

#                 for val in self.halfCorrect.keys():
#                     if i not in self.halfCorrect[val]:
#                         nextGuess += self.confirm[i]

#                         break
                    

#             for j in range(26):
#                 if self.characters[j] in tested:
#                     continue
#                 elif self.characters[j] == self.halfCorrect.keys():
#                     continue
#                 elif self.wrong[j] == -1:
#                     continue
#                 else:    
#                     nextGuess += self.characters[j]
#                     break
                
        
#         self.count += 1
        
#         return nextGuess



# solver = WordleSolver()

# # @app.route('/wordle-game', methods=['POST'])
# @app.route('/wordle-game', methods=['POST'])
# def solve_wordle():
    


#     if solver.count == 0:
#         solver.count += 1
#         return {"guess": "slate"}
    
#     data = request.get_json()
    
#     logging.info("data sent for evaluation {}".format(data))
    
    
#     prevGuess = data.get("guessHistory")[-1]
#     evaluation = data.get("evaluationHistory")[-1]
#     result = solver.solve(prevGuess, evaluation)
    
#     logging.info("My result :{}".format(result))
    

#     return {"guess": result}




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
        self.characters = "abcdefghijklmnopqrstuvwxyz"

    def solve(self, prevGuess, evaluation) -> dict:
        for i in range(5):
            if evaluation[i] == '?':
                continue
            elif evaluation[i] == '-':
                self.wrong[ord(prevGuess[i]) - ord('a')] = -1
            elif evaluation[i] == 'X':
                if prevGuess[i] not in self.halfCorrect.keys():
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
                        nextGuess += val
                        break
                
                # for j in range(26):
                #     if self.wrong[j] != -1:
                #         nextGuess += self.characters[j]
                #         break
                
                for j in range(26):
                    if self.characters[j] in self.halfCorrect.keys():
                        continue
                    elif self.wrong[j] == -1:
                        continue
                    else:    
                        nextGuess += self.characters[j]
                        break
        
        self.count += 1
        
        return {"newGuess": nextGuess}


solver = WordleSolver()

@app.route('/wordle-game', methods=['POST'])
def solve_wordle():
    if solver.count == 0:
        solver.count += 1
        return {"guess": "slate"}
    
    data = request.get_json()
    
    logging.info("data sent for evaluation: %s", data)
    
    prevGuess = data.get("guessHistory")[-1]
    evaluation = data.get("evaluationHistory")[-1]
    result = solver.solve(prevGuess, evaluation)
    
    logging.info("My result: %s", result)
    
    return {"guess": result["newGuess"]}