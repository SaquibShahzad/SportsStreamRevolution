#!/usr/bin/env python
import pika
import sys
import json
import time
import datetime


def parseUTC(utcfloat: float) -> datetime.datetime:
    return datetime.datetime.utcfromtimestamp(utcfloat)

def runMetaData():
    i = 0
    curTime = 1601166021.0003235
    curDt = parseUTC(curTime)
    with open(filepath) as infile:
        for line in infile:
            
            if ('[' == line[0] or ']' == line[0]):
                continue
            strippedLine = line
            if len(strippedLine) == 0:
                continue
            # trim the line of the comma so we can json.loads
            if(',' in line[-2]):
                strippedLine = line[0: -2]

            msg = json.loads(strippedLine)
            packetTime = parseUTC(msg["PacketSendUTC"])
            delta = packetTime - curDt
            # make sure time is positive number
            t = delta.total_seconds()
            if t < 0:
                t *= -1

            # send data
            channel.basic_publish(exchange='', routing_key='player-tracker', body=str(msg))
            print(" [x] Sent %r" % msg["PacketSendUTC"])
            print("Waiting for %r seconds." % delta.total_seconds())

            # Wait for next packet
            time.sleep(t)
            curDt = packetTime

    runMetaData()


# Entity tracking file
filepath = "../2019030415/EntityTracking.JSON"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
runMetaData()

