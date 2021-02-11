import base64 #for lossless encoding transfer
from datetime import datetime #to set frame timestamp
import os #write + read files
import numpy as np
import shutil
import socketio
from flask import Flask
#from flask import Flask
 #framework for web devices
from io import BytesIO #manipulate string and byte data in memory
import eventlet
import eventlet.wsgi 
import cv2

import tensorflow as tf
import keras
from keras.models import load_model
from PIL import Image

height = 75
width = 320     

def resize(image):
    return cv2.resize(image, (width, height), cv2.INTER_AREA)

#server init
#flask web app
sio = socketio.Server(always_connect=True)
application = socketio.WSGIApp(sio)

#init empty model and image array
net = None
image_array_before = None

#Speed limits
max_speed = 35
min_speed = 5

speed_limit = max_speed

#Server event handler       
@sio.on('telemetry')
def telemetry(sid, data):

    if data:
        steering_angle = float(data["steering_angle"])
        throttle = float(data["throttle"])
        speed = float(data["speed"])    
        image = Image.open(BytesIO(base64.b64decode(data["image"])))
        
        #save frame
        timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
        #image_filename = os.path.join(r'C:\Users\mindf\Documents\WorkandSchool\TKS\Focus(AI)\Replicate1\Image Folder', timestamp)
        #image.save('{}.jpg'.format(image_filename))
        
        try:
            image = np.asarray(image)
            image = resize(image)
            image = np.array([image])

            steering_angle = float(net.predict(image))

            global speed_limit
            if speed > speed_limit:   
                speed_limit = min_speed
            else:
                speed_limit = max_speed
            throttle = (1.0 - steering_angle**2 - (speed/speed_limit)**2)

            print ('{} {} {}'.format(steering_angle, throttle, speed))
            send_control(steering_angle, throttle)

        except Exception as e:
            print (e)

    else:
        
        sio.emit('manual', data={}, skip_sid = True)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0,0) 

def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data = {
            "steering_angle": steering_angle.__str__(),
            "throttle": throttle.__str__()
        },
        skip_sid = True)
# 004 006
if __name__ == "__main__":
    net = load_model(r'C:\Users\mindf\Documents\WorkandSchool\TKS\Focus\Replicate1\Code\model=002.h5')


    application = socketio.Middleware(sio, application)
    #deploy
    eventlet.wsgi.server(eventlet.listen(('localhost', 4567)), application)

# parsing command line arguments
# import argparse
# #decoding camera images
# import base64
# #for frametimestamp saving
# from datetime import datetime
# #reading and writing files
# import os
# #high level file operations
# import shutil
# #matrix math
# import numpy as np
# #real-time server
# import socketio
# #concurrent networking 
# import eventlet
# #web server gateway interface
# import eventlet.wsgi
# #image manipulation
# from PIL import Image
# #web framework
# from flask import Flask
# #input output
# from io import BytesIO
# import cv2

# #load our saved model
# from keras.models import load_model

# height = 320
# width = 160    

# def resize(image):
#     return cv2.resize(image, (width, height), cv2.INTER_AREA)

# #initialize our server
# sio = socketio.Server()
# #our flask (web) app
# app = Flask(__name__)
# #init our model and image array as empty
# model = None
# prev_image_array = None

# #set min/max speed for our autonomous car
# MAX_SPEED = 25
# MIN_SPEED = 10

# #and a speed limit
# speed_limit = MAX_SPEED

# #registering event handler for the server
# @sio.on('telemetry')
# def telemetry(sid, data):
#     if data:
#         # The current steering angle of the car
#         steering_angle = float(data["steering_angle"])
#         # The current throttle of the car, how hard to push peddle
#         throttle = float(data["throttle"])
#         # The current speed of the car
#         speed = float(data["speed"])
#         # The current image from the center camera of the car
#         image = Image.open(BytesIO(base64.b64decode(data["image"])))
#         try:
#             image = np.asarray(image)       # from PIL image to numpy array
#             image = resize(image) # apply the preprocessing
#             image = np.array([image])       # the model expects 4D array

#             # predict the steering angle for the image
#             steering_angle = float(model.predict(image, batch_size=1))
#             # lower the throttle as the speed increases
#             # if the speed is above the current speed limit, we are on a downhill.
#             # make sure we slow down first and then go back to the original max speed.
#             global speed_limit
#             if speed > speed_limit:
#                 speed_limit = MIN_SPEED  # slow down
#             else:
#                 speed_limit = MAX_SPEED
#             throttle = 1.0 - steering_angle**2 - (speed/speed_limit)**2

#             print('{} {} {}'.format(steering_angle, throttle, speed))
#             send_control(steering_angle, throttle)
#         except Exception as e:
#             print(e)

#         # save frame
#         if args.image_folder != '':
#             timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
#             image_filename = os.path.join(args.image_folder, timestamp)
#             image.save('{}.jpg'.format(image_filename))
#     else:
        
#         sio.emit('manual', data={}, skip_sid=True)


# @sio.on('connect')
# def connect(sid, environ):
#     print("connect ", sid)
#     send_control(0, 0)


# def send_control(steering_angle, throttle):
#     sio.emit(
#         "steer",
#         data={
#             'steering_angle': steering_angle.__str__(),
#             'throttle': throttle.__str__()
#         },
#         skip_sid=True)


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Remote Driving')
#     parser.add_argument(
#         'model',
#         type=str,
#         help='Path to model h5 file. Model should be on the same path.'
#     )
#     parser.add_argument(
#         'image_folder',
#         type=str,
#         nargs='?',
#         default='',
#         help='Path to image folder. This is where the images from the run will be saved.'
#     )
#     args = parser.parse_args()

#     #load model
#     model = load_model(args.model)

#     if args.image_folder != '':
#         print("Creating image folder at {}".format(args.image_folder))
#         if not os.path.exists(args.image_folder):
#             os.makedirs(args.image_folder)
#         else:
#             shutil.rmtree(args.image_folder)
#             os.makedirs(args.image_folder)
#         print("RECORDING THIS RUN ...")
#     else:
#         print("NOT RECORDING THIS RUN ...")

#     # wrap Flask application with engineio's middleware
#     app = socketio.Middleware(sio, app)

#     # deploy as an eventlet WSGI server
#     eventlet.wsgi.server(eventlet.listen(('', 4567)), app)