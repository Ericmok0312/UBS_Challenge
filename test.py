
def kazuma_solver(monsters, efficiency, can_shoot):
    if (len(monsters)==0):
        return efficiency
    else:
        if(not(can_shoot)):
            res1 = kazuma_solver(monsters[1:], efficiency-monsters[0], not can_shoot) # spell
            res2 = kazuma_solver(monsters[1:], efficiency, can_shoot)
            res3 = -999
        elif(can_shoot):
            res1 = kazuma_solver(monsters[2:], efficiency+monsters[0], not can_shoot) #shoot 
            res2 = kazuma_solver(monsters[1:], efficiency-monsters[0], can_shoot)
            res3 = kazuma_solver(monsters[1:], efficiency, can_shoot)
        
        return max(res1, res2,res3)



monsters = [1,4,5,0,4]
efficiency = kazuma_solver(monsters, 0, False)
print(efficiency)