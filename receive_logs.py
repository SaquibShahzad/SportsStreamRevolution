#!/usr/bin/env python
import pika
import ast
queue_name = 'puck-tracker'
teams = {}
goalies = {}
players = {}
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
    m = k["Teams"]
    for player in l:
        if player["Position"] == "G":
            goalies[player.get("EntityId")] = [player.get("EntityTeamId"), player.get("FirstName") + " " + player.get("LastName")]
        else:
            players[player.get("EntityId")] = [player.get("EntityTeamId"), player.get("FirstName") + " " + player.get("LastName")]
    for team in m:
        
        temp2 = team["OfficialId"]
        teams[temp2] = team["FullName"]
    if len(goalies) >= 4 and len(teams) == 2:
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
            gpos[player["EntityId"]] = [player["Location"], player["EntityId"]]
        
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
                h = gpos[g][0]
                
                for p in ppos:
                    pyer = ppos[p]
                    
                    if abs(pyer["X"] - h["X"]) + abs(pyer["Y"] - h["Y"]) < cpyer2g[1]:
                        cpyer2g[1] = abs(pyer["X"] - h["X"]) + abs(pyer["Y"] - h["Y"])
                        cpyer2g[0] = p
                        cpyer2g[2] = (int(players[p][0]) == int(goalies[g][0]))
                
                if cpyer2g[0] == cpyer[0] and not cpyer2g[2]:
                    
                    print("Breakaway!")
                    print("Player " +  players[cpyer2g[0]][1] + " of the " + teams[players[cpyer[0]][0]] +" at location: " + str(ppos[cpyer2g[0]]))
                    print("Goalie " +  goalies[g][1] + " of the " + teams[goalies[g][0]] +" at location: " + str(gpos[g][0]))
                    print("Puck's Location: " + str(loc))
                    
            
                
        
        else:
            if player["OnPlayingSurface"]:
                ppos[player["EntityId"]] = player["Location"]
            elif player["EntityId"] in ppos:
                ppos.pop(player["EntityId"])
           


conTag = channel.basic_consume(
    queue=queue_name, on_message_callback=callback2, auto_ack=True)

channel.start_consuming()