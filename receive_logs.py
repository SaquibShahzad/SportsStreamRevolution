#!/usr/bin/env python
import pika
import ast
queue_name = 'puck-tracker'
goalies = {}
gpos= {}
ppos={}
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    i = body.decode("utf-8")
    j = ast.literal_eval(i)
    k = j["EntityRegistration"]
    l = k["Entities"]
    
    for player in l:
        if player["Position"] == "G":
            
            goalies[player.get("EntityId")] = player.get("EntityTeamId")
    
    if len(goalies) >= 4:
        channel.stop_consuming()
            
    
    
    

conTag = channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()


    
queue_name = 'player-tracker'
channel.queue_declare(queue=queue_name)

def callback2(ch, method, properties, body):
    i = body.decode("utf-8")
    j = ast.literal_eval(i)
    k = j["EntityTracking"]
    l = k["TrackingData"]
    
    for player in l:
        if player["EntityId"] in goalies and player["OnPlayingSurface"] == True:
            gpos[player["EntityId"]] = player["Location"]
        
        elif player["EntityId"] == "1":
            
            loc = player["Location"]
            
            cpyer = ['', 100000]
            cpyer2g = ['', 100000, False]
            for p in ppos:
                pyer = ppos[p]
                
                if abs(pyer["X"] - loc["X"]) + abs(pyer["Y"] - loc["Y"]) < cpyer[1]:
                    cpyer[1] = abs(pyer["X"] - loc["X"]) + abs(pyer["Y"] - loc["Y"])
                    cpyer[0] = p

            for g in gpos:
                h = gpos[g]
                
                for p in ppos:
                    pyer = ppos[p]
                    
                    if abs(pyer["X"] - h["X"]) + abs(pyer["Y"] - h["Y"]) < cpyer2g[1]:
                        cpyer2g[1] = abs(pyer["X"] - h["X"]) + abs(pyer["Y"] - h["Y"])
                        cpyer2g[0] = p
                        cpyer2g[2] = abs(int(p)- int(g)) < 100
                
                if cpyer2g[0] == cpyer[0] and not cpyer2g[2]:
                    print("Breakaway!")
                    print("Player's Position: " + ppos[cpyer2g[0]])
                    print("Goalie's Position: "+gpos[g])
                    print("Puck's Location: " + loc)
                    
            
                
        
        else:
            if player["OnPlayingSurface"]:
                ppos[player["EntityId"]] = player["Location"]
            elif player["EntityId"] in ppos:
                ppos.pop(player["EntityId"])
           


conTag = channel.basic_consume(
    queue=queue_name, on_message_callback=callback2, auto_ack=True)

channel.start_consuming()
