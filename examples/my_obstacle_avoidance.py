import picar_4wd as fc

forward_speed = 20
backward_speed = 100 
turn_speed = 10

def get_dist():
    dist = [fc.get_status_at(angle) for angle in range(-90, 90, 35) ]
    dist += [fc.get_status_at(angle) for angle in range(90, -90, -35) ]
    return dist

def avoid_edges(threshold = 60):
    if fc.is_on_edge(threshold, fc.get_grayscale_list() ):
        fc.backward(backward_speed )
        fc.turn_right(turn_speed)

        
def avoid_collision():
    dist = get_dist()
    print(dist)
    if dist[4:8] != [2]*4 :
        fc.backward(backward_speed)
        fc.turn_right(turn_speed)
    else:
        fc.forward(forward_speed)
    

def main():
    while True:
        avoid_edges()
        avoid_collision()

            
            

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
