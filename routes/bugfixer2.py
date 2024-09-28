import json
import logging

from flask import request

from routes import app



def max_bugsfixed(bugseq1):
    # Sort bugs by their deadlines (second element in each pair)
    combination = generate_permutations(bugseq1)
    max_bugs = 0
    for bugseq in combination:
        current_time = 0
        bugs_fixed = 0

        for difficulty, limit in bugseq:
            if current_time + difficulty <= limit:
                current_time += difficulty
                bugs_fixed += 1
        
        if bugs_fixed > max_bugs:
            max_bugs = bugs_fixed

    return max_bugs



def generate_permutations(seqs):
    # Base case: if the list has only one sequence, return it
    if len(seqs) == 1:
        return [seqs]
    
    # Initialize result list
    result = []
    
    # Iterate over the sequences
    for i, seq in enumerate(seqs):
        # Get the remaining sequences
        remaining_seqs = seqs[:i] + seqs[i+1:]
        
        # Generate permutations of the remaining sequences
        remaining_perms = generate_permutations(remaining_seqs)
        
        # Add the current sequence to each permutation
        for perm in remaining_perms:
            result.append([seq] + perm)
    
    # Return the result
    return result


@app.route('/bugfixer/p2', methods=['POST'])
def bugfixerp2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    
    ans = []
    for i in range(len(data)):
        ans.append(max_bugsfixed(data[i].get("bugseq")))
        
    json_response = json.dumps(ans)
        
    return json_response, 200, {'Content-Type': 'application/json; charset=utf-8'}
