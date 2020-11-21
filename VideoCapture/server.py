# Python 3.6.7 - https://www.python.org/downloads/release/python-367/
import cv2 # pip install opencv-python
import time
import pika # pip install pika
import base64


videoFile = "/efs/data/3_415_dal_tbl_1920_h_whole_4000K_16x9_trimmed.mp4"
cap = cv2.VideoCapture(videoFile)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

while(cap.isOpened()):
    now = time.time()
    ret, frame = cap.read()

    if ret==True:
        frame = cv2.resize(frame, (600, 400), interpolation = cv2.INTER_AREA)
        """
        cv2.imshow("Producer Video",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        """
        print(time.time()-now)

        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)

        # Send data to rabbitMQ
        try:
            channel.basic_publish(exchange='', routing_key='video-feed', body=jpg_as_text)
        except:
            print("test")

    else:
        print('loop video')
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)