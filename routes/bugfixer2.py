import json
import logging

from flask import request

from routes import app



def max_bugsfixed(bugseq1):
    # Sort bugs by their deadlines (second element in each pair)
    bugseq1.sort(key=lambda x: x[1])
    
    # Find the maximum deadline
    max_deadline = max(bugseq1, key=lambda x: x[1])[1]
    
    # Initialize the dp array with zeros
    dp = [0] * (max_deadline + 1)
    
    # Iterate over each bug
    for difficulty, limit in bugseq1:
        # Update the dp array in reverse to avoid overwriting values
        for t in range(limit, difficulty - 1, -1):
            dp[t] = max(dp[t], dp[t - difficulty] + 1)
    
    # The maximum number of bugs fixed is the maximum value in the dp array
    return max(dp)

# # Example usage
# bugseq1 = [(20, 330), (30, 135), (110, 330), (210, 330)]
# print(max_bugsfixed(bugseq1))  # Output should be 3




@app.route('/bugfixer/p2', methods=['POST'])
def bugfixerp2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    
    ans = []
    for i in range(len(data)):
        ans.append(max_bugsfixed(data[i].get("bugseq")))
        
    json_response = json.dumps(ans)
        
    return json_response, 200, {'Content-Type': 'application/json; charset=utf-8'}


