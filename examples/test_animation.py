
import picar_4wd as fc
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def get_distance_at_with_limit(angle, limit = 1000):
    ''' if distance is greater than limit, it returns limit'''
    return int( min( fc.get_distance_at(angle), limit) )

def scan(step = 35, angle_offset = 0):
    dist = [  get_distance_at_with_limit(angle) for angle in range(-60, 61, step) ]
    dist += [  get_distance_at_with_limit(angle) for angle in range(60, -61, -step) ]
    angles = [ angle_offset + i for i in range(-60, 61, step)] + [ angle_offset + i for i in range(60, -61, -step)]
    return dist, angles

    
    
def polar_to_cartesian(distances, angles):
    x_coordinates = distances * np.cos(np.radians(angles))
    y_coordinates = distances * np.sin(np.radians(angles))
    return x_coordinates, y_coordinates

def main():
    numframes = 100
    x, y = polar_to_cartesian(*scan(10))

    fig = plt.figure()
    scat = plt.scatter(x, y, s=100)

    def update_plot(*args):
        x, y = polar_to_cartesian(*scan(10))
        scat.set_offsets(np.column_stack([x,y])) 
        return scat,


    ani = animation.FuncAnimation(fig, update_plot, frames=range(numframes))
    plt.show()


if __name__ == '__main__':
    main()