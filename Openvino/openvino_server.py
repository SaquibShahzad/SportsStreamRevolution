#!/usr/bin/python3
import threading
import time
import cv2 as cv
import numpy as np
from detector import PedestrianDetector
import subprocess
import base64
import pika # pip install pika
from flask import Flask, request
app = Flask(__name__)


def readb64(uri):
   encoded_data = uri
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv.imdecode(nparr, cv.IMREAD_COLOR)
   return img

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

# def get_frames():
#     global channel, connection
#     channel.queue_declare(queue='video-feed')

#     def callback(ch, method, properties, body):
#         print(" [x] Received frame")
#         base64_image = body.decode("utf-8")
#         image = readb64(base64_image)

#         if image is not None:
#             x_scale = image.shape[1]
#             y_scale = image.shape[0]
#             detector = PedestrianDetector()
#             result = detector.detect(image)
#             for (image_id, label, conf, x_min, y_min, x_max, y_max) in result[0][0]:
#                 if label != 0 and conf > 0.2:
#                     x = (int(x_min * x_scale), int(y_min * y_scale))
#                     y = (int(x_max * x_scale), int(y_max * y_scale))
#                     color = (0, 0, 255)
#                     image = cv.rectangle(image, x, y, color)
           
#             retval, buffer = cv.imencode('.jpg', image)
#             jpg_as_text = base64.b64encode(buffer)
#             # needs this the subscriber side - data:image/jpeg;base64,
#             # Send data to rabbitMQ
#             channel.basic_publish(exchange='', routing_key='video-openvino', body=jpg_as_text)

#         if image is not None:
#             x_scale = image.shape[1]
#             y_scale = image.shape[0]
#             detector = PedestrianDetector()
#             result = detector.detect(image)
#             for (image_id, label, conf, x_min, y_min, x_max, y_max) in result[0][0]:
#                 if label != 0 and conf > 0.2:
#                     x = (int(x_min * x_scale), int(y_min * y_scale))
#                     y = (int(x_max * x_scale), int(y_max * y_scale))
#                     color = (0, 0, 255)
#                     image = cv.rectangle(image, x, y, color)
           
#             retval, buffer = cv.imencode('.jpg', image)
#             jpg_as_text = base64.b64encode(buffer)
#             # needs this the subscriber side - data:image/jpeg;base64,
#             # Send data to rabbitMQ
#             channel.basic_publish(exchange='', routing_key='video-openvino', body=jpg_as_text)
        
        
#     channel.basic_consume(queue='video-feed', on_message_callback=callback, auto_ack=True)
#     print(' [*] Waiting for messages. To exit press CTRL+C')
#     try:
#         test = connection.is_open
#         channel.start_consuming()
#     except pika.exceptions.AMQPConnectionError:
#         print("Connection was closed, retrying...")


@app.route('/')
def classification_sample():
    return 'body tracking sample'

@app.route('/image', methods=['POST'])
def do_classification():
    global channel, connection
    if request.headers['Content-Type'] == 'application/text/plain':
        print("processing image***")
        base64_image = request.data.decode("utf-8")
        image = readb64(base64_image)

        if image is not None:
            x_scale = image.shape[1]
            y_scale = image.shape[0]
            detector = PedestrianDetector()
            result = detector.detect(image)
            for (image_id, label, conf, x_min, y_min, x_max, y_max) in result[0][0]:
                if label != 0 and conf > 0.2:
                    x = (int(x_min * x_scale), int(y_min * y_scale))
                    y = (int(x_max * x_scale), int(y_max * y_scale))
                    color = (0, 0, 255)
                    image = cv.rectangle(image, x, y, color)
           
            retval, buffer = cv.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            # needs this the subscriber side - data:image/jpeg;base64,
            # Send data to rabbitMQ
            try:
                channel.basic_publish(exchange='', routing_key='video-openvino', body=jpg_as_text.decode("utf-8"))
            except:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
                channel = connection.channel()      
            return jpg_as_text
        else:
            return"bad"
        return "test"       
    else:
        return "415 Unsupported Media Type ;"

if __name__ == '__main__':
    # t1 = threading.Thread(target=get_frames)
    # t1.daemon = True
    # t1.start()
    app.run(debug=True,host='0.0.0.0')
