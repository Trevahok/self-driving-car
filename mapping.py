import picar_4wd as fc
import numpy as np
import time
import matplotlib.pyplot as plt
import math

forward_speed = 20
backward_speed = 100 
turn_speed = 10

def get_distance_at_with_limit(angle, limit = 1000):
    ''' if distance is greater than limit, it returns limit'''
    dist = fc.get_distance_at(angle)
    if dist > limit: 
        return - 2 
    return dist


def rudimentary_map(angle_step = 1):
    env = np.zeros((250, 250))
    for i in range(-60, 61, angle_step):

        tmp = get_distance_at_with_limit(i, 150)
        if tmp == -2  : 
            continue

        x = 99 + int(tmp * np.sin(np.radians(i)))
        y = 99 + int(tmp* np.cos(np.radians(i)))

        if tmp != 150 and tmp != -2 :
            env[x][y] = 1
  
    return env
        

def env_enhancement(env):
    env_copy = np.copy(env)
    for x in range(len(env)):
        for y in range(len(env[0])):
            down = max(x - 8, 0)
            left = max(y - 8, 0)
            right = min(y + 8, len(env[0])-1)
            up = min(x + 8, len(env)-1)
            surrounding = env[down:up, left:right]
            env_copy[x][y] = np.max(surrounding)
    return env_copy

    
    
def bres():
    pass
   
    
 

def main():
    # env = map_env(10, 100)
    env = rudimentary_map(10)
    print(env)
    plt.imshow(env, cmap='hot', origin='lower')

    # dist, angles = scan(10)
    # x, y = polar_to_cartesian(dist, angles)

    # im = plt.scatter(x, y )
    plt.show()





    
if __name__ == '__main__':
    main()  
        

