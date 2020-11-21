#!/usr/bin/env python
#https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive.py
import pika, sys, os, base64
import numpy as np
import cv2 as cv
import threading

frame = None

def getFrames():
    global frame 
    while True:
        if frame is not None: 
            cv.imshow('Receiver Video',frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

def readb64(uri):
   encoded_data = uri
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv.imdecode(nparr, cv.IMREAD_COLOR)
   return img

def main():
    global frame
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='video-feed')

    def callback(ch, method, properties, body):
        global frame
        base64_image = body.decode("utf-8")
        image = readb64(base64_image)
        frame = image

    channel.basic_consume(queue='video-feed', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=getFrames)
        t1.daemon = True
        t1.start()
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)