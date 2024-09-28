from flask import request
import logging
from routes import app
import json



def kazuma_solver(monsters):
    nums = []
    
    if len(monsters) < 2:
        return 0
    
    for i in range(1, len(monsters)):
        nums.append(monsters[i] - monsters[i-1])
    
    n = len(nums)
    if n <= 2:
        return max(sum(nums), 0)
    
    dp = [[0, 0] for _ in range(n)]
    
    # Base cases
    dp[0][0] = nums[0]
    dp[0][1] = 0
    
    # Fill dp table
    for i in range(1, n):
        if i >= 2:
            dp[i][0] = max(dp[i-1][0], dp[i-2][0] + nums[i])
        else:
            dp[i][0] = max(dp[i-1][0], 0)
        
        dp[i][1] = max(dp[i-1][1], dp[i-2][1])
    
    return max(dp[-1])



@app.route('/kazuma', methods=['POST'])
def solve_kazuma():
    data = request.get_json()
    result = []
    for i in range(len(data)):
        result.append({"efficiency": kazuma_solver(data[i].get("monsters"))})
    return json.dumps(result)