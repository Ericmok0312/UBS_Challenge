# import json
# import logging

# from flask import request

# from routes import app

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





from flask import Flask, request, jsonify
import json
from collections import defaultdict, Counter

import json
import logging

from flask import request

from routes import app

# Sample Word List
# For a complete solution, replace this list with the full Wordle word list.
WORD_LIST = [line.lower() for line in open("./routes/word.txt", "r").read().splitlines()]

# Precompute letter frequency for heuristic
letter_freq = Counter()
for word in WORD_LIST:
    unique_letters = set(word)
    letter_freq.update(unique_letters)

def validate_input(guess_history, evaluation_history):
    if not isinstance(guess_history, list) or not isinstance(evaluation_history, list):
        return False
    if len(guess_history) != len(evaluation_history):
        return False
    for guess, evaluation in zip(guess_history, evaluation_history):
        if not isinstance(guess, str) or not isinstance(evaluation, str):
            return False
        if len(guess) != len(evaluation):
            return False
        for char in guess:
            if char not in WORD_LIST[0]:
                return False
        for char in evaluation:
            if char not in ['?', 'O', 'X', '-']:
                return False
    return True

def filter_words(guess_history, evaluation_history):
    possible_words = set(WORD_LIST)

    # To keep track of letters that must be present somewhere
    required_letters = defaultdict(int)

    # To keep track of letters that must not be present
    excluded_letters = set()

    for guess, evaluation in zip(guess_history, evaluation_history):
        guess = guess.lower()
        evaluation = evaluation.upper()
        for idx, (g_char, e_char) in enumerate(zip(guess, evaluation)):
            if e_char == '?':
                continue  # Feedback is masked; cannot apply constraints
            if e_char == 'O':
                # Correct position
                possible_words = {word for word in possible_words if word[idx] == g_char}
            elif e_char == 'X':
                # Wrong position but present in the word
                possible_words = {word for word in possible_words if g_char in word and word[idx] != g_char}
                required_letters[g_char] += 1
            elif e_char == '-':
                # Not present in the word
                # However, need to consider multiple occurrences
                # If the letter was marked as 'X' elsewhere, it is present
                # So only exclude if it's not required elsewhere
                if required_letters[g_char] == 0:
                    excluded_letters.add(g_char)
        # After processing all positions, update possible_words by excluding excluded_letters
        if excluded_letters:
            possible_words = {word for word in possible_words if not any(letter in word for letter in excluded_letters)}
    # Further filter words that satisfy required_letters counts
    for letter, count in required_letters.items():
        possible_words = {word for word in possible_words if word.count(letter) >= count}

    return list(possible_words)

def select_best_guess(possible_words):
    if not possible_words:
        return None
    # Heuristic: choose the word with the highest sum of letter frequencies
    scores = {}
    for word in possible_words:
        unique_letters = set(word)
        score = sum(letter_freq[letter] for letter in unique_letters)
        scores[word] = score
    # Select the word with the highest score
    best_guess = max(scores, key=scores.get)
    return best_guess

@app.route('/wordle-game', methods=['POST'])
def wordle_game():
    try:
        data = request.get_json()
        guess_history = data.get('guessHistory', [])
        evaluation_history = data.get('evaluationHistory', [])

        if not validate_input(guess_history, evaluation_history):
            return jsonify({"error": "Invalid input format. 'guessHistory' and 'evaluationHistory' should be lists of strings."}), 400

        # If no guesses yet, suggest an opening guess
        if not guess_history:
            # A common good starting word is 'crane'
            opening_guess = "crane" if "crane" in WORD_LIST else WORD_LIST[0]
            return jsonify({"guess": opening_guess})

        # Filter possible words based on history
        possible_words = filter_words(guess_history, evaluation_history)

        if not possible_words:
            return jsonify({"error": "No possible words found based on the provided history."}), 400

        # Select the best guess
        next_guess = select_best_guess(possible_words)

        if not next_guess:
            return jsonify({"error": "Unable to determine the next guess."}), 400

        return jsonify({"guess": next_guess})

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON input."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500









