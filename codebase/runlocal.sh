#!/bin/bash

# Start tmux session
pip install rsa

tmux new-session -d -s mySession

# Start Python scripts in different windows
tmux new-window -t mySession:1 -n 'weather' 'python3 final.py --port 33021 --network farm1 --name weather'
tmux new-window -t mySession:2 -n 'soil' 'python3 final.py --port 33023 --network farm1 --name soil'
tmux new-window -t mySession:3 -n 'water' 'python3 final.py --port 33025 --network farm1 --name water'
tmux new-window -t mySession:4 -n 'drone' 'python3 final.py --port 33027 --network farm1 --name drone'
tmux new-window -t mySession:5 -n 'health' 'python3 final.py --port 33029  --network farm1 --name health'
# ... similarly start other scripts

# Wait a bit for the script to start
sleep 3

# Send commands to one of the windows
tmux send-keys -t mySession:1 'send' C-m
sleep 1
tmux send-keys -t mySession:1 'farm1/soil/temperature' C-m
tmux send-keys -t mySession:2 'send' C-m
sleep 1
tmux send-keys -t mySession:2 'farm1/drone/speed' C-m



# Attach to session if you want to view it
tmux attach-session -t mySession