from flask import Flask, render_template
from flask_socketio import SocketIO
import picar_4wd as fc 


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


def get_distance_at_with_limit(angle, limit = 1000):
    ''' if distance is greater than limit, it returns limit'''
    dist = fc.get_distance_at(angle)
    if dist > limit: 
        return - 2 
    return dist

def us_map():
    l = []
    for i in range(-60, 61, 10):
        socketio.sleep(0.05)
        tmp = get_distance_at_with_limit(i, 150)
        l.append(tmp)
    return l


@app.route('/')
def index():
    return render_template('control.html')

def emit_ultrasound():
    while True: 
        dist = us_map()
        gs = fc.get_grayscale_list()
        socketio.emit('ultrasound', {'us': dist, 'gs': gs } )

def send_grayscale_pic(gray_scale_img = None):
    gray_scale_img_sample = [
        [120, 130, 140, 150, 160],
        [170, 180, 190, 200, 210],
        [220, 230, 240, 250, 60],
        [70, 80, 90, 100, 110],
        [10, 20, 30, 40, 50]
    ]

    if gray_scale_img:
        socketio.emit('grayscale_img', gray_scale_img)
    else:
        socketio.emit('grayscale_img', gray_scale_img_sample)

@socketio.on('connect')
def handle_connected(data):
    print('connected to socket: ' + str(data))
    socketio.start_background_task(target=emit_ultrasound)
    send_grayscale_pic()


@socketio.on('up')
def handle_up_event():
    fc.move_forward()

@socketio.on('down')
def handle_down_event():
    fc.move_backward()

@socketio.on('left')
def handle_left_event():
    fc.left()

@socketio.on('right')
def handle_right_event():
    fc.right()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)

