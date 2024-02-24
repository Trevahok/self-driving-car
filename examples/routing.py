import numpy as np
import picar_4wd as fc
import mapping
import time
import matplotlib.pyplot as plt
import object_detection

def turn_right():
    fc.turn_right(40)
    time.sleep(0.605)
    fc.stop()

def turn_left():
    fc.turn_left(40)
    time.sleep(0.605)
    fc.stop()

def move_forward():
    fc.forward(2)
    time.sleep(0.03)
    fc.stop()

    fc.forward(2)
    time.sleep(0.03)
    fc.stop()

def heuristic(a, b):
    #Calculate the heuristic value between two points (Manhattan Dis)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

##Backward finding the path
def back_tracking(end_node, path_mapping):
    path = []
    current = end_node
    while current in path_mapping:
        path.append(current)
        current = path_mapping[current]
    return path[::-1]



def path_convert(path, start, initial_dir):
    neighborMap = {
        (1, 0): 0, #up
        (-1, 0): 2, #down
        (0, -1): 3, #left
        (0, 1): 1 #right
    }
    path = [start] + path
    directions = []
    for i in range(len(path)):
        if i == len(path) - 1:
            break
        direction = (path[i+1][0] - path[i][0], path[i+1][1] - path[i][1])
        directions.append(neighborMap[direction])
    
    orders = []
    current_dir = initial_dir
    for dir in directions:
        required_dir_change = (dir - current_dir)%4 ##record number of right turns needed
        current_dir = dir
        orders.append(required_dir_change)
    return orders


def a_star_search(env, start, end):


    if env[end[0]][end[1]] == 1 or env[start[0]][start[1]] == 1:
        raise ValueError("obstacle in start/end position, a*search not running")
        return False

    left = (0, -1)
    right = (0, 1)
    up = (1, 0)
    down = (-1, 0)

    neighbors = [left, right, down, up]

    measuredSet = set()
    
    nextStepMapping = {}
    gScore = {start: 0}
    fScore = {start: heuristic(start, end)}

    toVisit = [start]

    while toVisit:
        current = min(toVisit, key=lambda x:fScore[x])
        if current == end:
            path = back_tracking(current, nextStepMapping)
            return path
        toVisit.remove(current)
        measuredSet.add(current)

        for i, j in neighbors:
            neighborNode_x = current[0] + i
            neighborNode_y = current[1] + j

            ##Could be changed if with weighted edges (slope?)
            node_gScore = gScore[current] + 1

            if neighborNode_x < 0 or neighborNode_x >= env.shape[0]:
                continue
            if neighborNode_y < 0 or neighborNode_y >= env.shape[1]:
                continue

            if env[neighborNode_x][neighborNode_y] == 1:
                ##If neighbor is obstacle
                continue
            
            neighbor = (neighborNode_x, neighborNode_y)
            if neighbor in measuredSet and node_gScore >= gScore.get(neighbor, 0):
                continue

            else:
                nextStepMapping[neighbor] = current
                gScore[neighbor] = node_gScore
                fScore[neighbor] = node_gScore + heuristic(neighbor, end)
                if neighbor not in toVisit:
                    toVisit.append(neighbor)
    return False

def mark_path(path, env):
    env_copy = np.copy(env)
    for point in path:
        env_copy[point[0]][point[1]] = -30
    
    plt.imshow(env_copy, cmap='hot', origin='lower')
    plt.show()
    return 
        

def main(env, object_detection, start=(100, 100), goal=(100, 200), initial_dirction=1  ):
    last_detection = 0
    path = a_star_search(env, start, goal)
    mark_path(path, env)
    if path == False:
        return False
    
    orders_path = path_convert(path, start, initial_dirction)
    
    step = 0
    for order in orders_path:
        if order > 0:
            if order == 3:
                turn_left()
            else:
                for i in range(order):
                    print("TURNING", order)
                    turn_right()
                
        step += 1
        move_forward()
        
        if step % 3  == 0  : 
            category, isDetected = object_detection.run()
            print(category)
            current_time = time.time()
            if isDetected and category == "SIGN" :
                fc.stop()
                time.sleep(3)
            last_detection = time.time()
         


if __name__ == '__main__':

    env = mapping.rudimentary_map(1)
    env = mapping.env_enhancement(env, 2 )

    plt.imshow(env, cmap='hot', origin='lower')
    plt.show()

    ob = object_detection.ObjectDetection()

    main(env, ob, goal=(100, 200))

