# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
init = [0, 0]
goal = [2, 0]
cost = [1, 2, 1, 20]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']
dir = 3

def optimum_policy(grid,goal,cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------
    global dir
    value = [[float('-inf') for row in range(len(grid[0]))] for col in range(len(grid))]
#     [[[0 for k in xrange(n)] for j in xrange(n)] for i in xrange(n)]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True


    while change:
        print "ll"
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] < 0:
                        value[x][y] = 0
                        policy[x][y] = '*'

                        change = True
                        

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + 1
#                             if a == dir:
#                                 v2 = value[x2][y2] + 1
#                             elif a == 1 or a == 0:
#                                 v2 = value[x2][y2] + 2
#                             elif a == 3 or a == 2:
#                                 v2 = value[x2][y2] + 20
                            if v2 > value[x][y]:
                                change = True
                                dir = a
                                value[x][y] = v2
                                policy[x][y] = delta_name[a]
    for i in policy:
        print i
    for i in value:
        print i
    print "yea!"
    return 0
print optimum_policy(grid,goal,cost)
