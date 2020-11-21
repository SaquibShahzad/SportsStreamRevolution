Analyzing data provided by Rogers, SportsNet and Intel to derive insights and add a fantasy premier league prediction feature to sportsnetNow. The actual solution would have to leverage 5G to work in real time, this is an MVP.

Here's how it would look on SNNOW: 
![SNNOW](https://github.com/SaquibShahzad/SportsStreamRevolution/blob/main/images/web.png?raw=true)


#### To run our demo
First, open up RabbitMQ on 3 different terminals
Then, navigate to the downloaded repo
Go into the PPT folder in the terminal
run our receive_logs, emit_log, and emit_log2 python scripts using the commands:
python receive_logs.py
python emit_log.py
python emit_log2.py

You can see the coordinates of players and the puck being sent to the RabbitMQ database
Please be patient when waiting for an output. There are not many times there is a potential breakaway in the game, so it may take a few minutes before you start to see an output in receive_logs.

#### How the code works
We first open up the game rosters to get player and goalie names and ids, as well as the names of the teams. 
We then open the tracking data, from which we can look at where players are in relation to the goalie and the puck. 
If the player who is closest to the puck is also closest to the goalie from the other team, then we consider this a breakaway.
From this, we output who the player is and which team they play for, who the goalie is and which team they play for, and the positions of this player, the goalie, and the puck. 

#### Next steps
By integrating an API, we could pull stats for the player on the breakaway and the goalie they are up against, and display them to the user
Then we would work on syncing this data with the video feed for the game to produce a "live" interactive stats feed for players on breakaways
Integrating the ability to predict whether a player scores or the goalie saves the shot would be our next task.
