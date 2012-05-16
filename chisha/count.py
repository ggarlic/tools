#!/usr/bin/env python
# -*- coding:utf8 -*-
#code by joycc liu
def countfood():
    ocount = open('./.count.log', 'w')
    foodcount = {}
    foodc = "\n"
    with open('./.food.log') as of:
        lines = of.readlines()
        for i in lines:
            foodtype = i.split(" ")[-1]
            if foodtype in foodcount:
                foodcount[foodtype] += 1
            else:
                foodcount[foodtype] = 1 
    
    for foodt in foodcount:
        ocount.write(foodt)
        foodc = foodc + foodt
        foodc += '\n'
        for i in range(foodcount[foodt]):
            foodc += ('*')
            ocount.write("*")
        foodc += ('\n')
        ocount.write("\n")    
    ocount.close()
    return foodc
        
