
def solve(data):
    generation = data["generations"]
    colony = data["colony"]
    result = dict()
    for gen in range(generation+1):
        weight = 0
        for i in range(len(colony)-1):
            left = colony[i]
            right = colony[i+1]
            if not (left, right) in result:
                result[(left,right)]  =  int((10+int(left)-int(right))%10)

        for i in range(len(colony)):
            weight+=int(colony[i])

        next_colon = ""
        for i in range(len(colony)-1):
            next_colon += colony[i]
            next_colon += str(result[(colony[i], colony[i+1])]+weight)[-1]
        
        next_colon += colony[-1]
        print(weight)
        colony = next_colon
    return weight



data = { "generations": 50, "colony": "1000" }

solve(data)