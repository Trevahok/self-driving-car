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
    return int( min( fc.get_distance_at(angle), limit) )

def scan_status(step = 35):
    dist = [fc.get_status_at(angle) for angle in range(-60, 60, step) ]
    dist += [fc.get_status_at(angle) for angle in range(90, -90, -step) ]
    return dist

def scan(step = 35, limit = 100, angle_offset = 0):
    dist = [  get_distance_at_with_limit(angle, limit) for angle in range(-60, 61, step) ]
    # dist += [  get_distance_at_with_limit(angle, limit) for angle in range(60, -61, -step) ]
    angles = [ angle_offset + i for i in range(-60, 61, step)] \
        # + [ angle_offset + i for i in range(60, -61, -step)]
    return dist, angles

def turn_around():
    fc.turn_left(100)
    time.sleep(0.99)
    fc.stop()

    
def polar_to_cartesian(distances, angles):
    x_coordinates = distances * np.cos(np.radians(angles))
    y_coordinates = distances * np.sin(np.radians(angles))
    return x_coordinates, y_coordinates

def mark_on_array(array, dist, angles, center= 100):
    x,y = polar_to_cartesian(dist, angles)
    print(list( zip(x,y)) ) 

    for i,j in zip(x,y):
        array[center + int(i)][ center+ int(j)] = 1
    return array

def map_env(scan_step = 10, limit =100):
    env = np.zeros((400, 400))

    dist, angles = scan(scan_step, limit)
    env = mark_on_array(env, dist, angles)

    # turn_around()

    # dist, angles = scan(1, angle_offset=180)
    # env = mark_on_array(env, dist, angles)

    return env
        

def mapper():
    env = np.zeros((150, 150))
    for i in range(-90, 91, 1):
        pass

    
    return env

def rudimentary_map():
    angle_step = 1
    env = np.zeros((150, 150))
    for i in range(-60, 61, angle_step):
        tmp = get_distance_at_with_limit(i* angle_step, 99)
        x = 49 +int(tmp * np.sin(np.radians(i*angle_step)))
        y = int(tmp* np.cos(np.radians(i*angle_step)))
        x = min(x, 150)
        y = min(y, 150)
        print(tmp, i, x,y)

        if tmp != 150 and tmp != -2 :
            env[x][y] = 1
  
    return env
        
    
    
def bres(env, x1,y1,x2,y2):
    x,y = x1,y1
    dx = abs(x2 - x1)
    dy = abs(y2 -y1)
    gradient = dy/float(dx)

    if gradient > 1:
        dx, dy = dy, dx
        x, y = y, x
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    p = 2*dy - dx
    print(f"x = {x}, y = {y}")

    env[x,y] = 1

    for k in range(2, dx + 2):
        if p > 0:
            y = y + 1 if y < y2 else y - 1
            p = p + 2 * (dy - dx)
        else:
            p = p + 2 * dy

        x = x + 1 if x < x2 else x - 1

        print(f"x = {x}, y = {y}")

        env[x,y] = 1
    return env
    
 

def main():
    # env = map_env(10, 100)
    env = rudimentary_map()
    print(env)
    plt.imshow(env, cmap='hot', origin='lower')

    # dist, angles = scan(10)
    # x, y = polar_to_cartesian(dist, angles)

    # im = plt.scatter(x, y )
    plt.show()





    
if __name__ == '__main__':
    main()  
        

