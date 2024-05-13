Project 3 – Readme 



This guide provides instructions for executing the code. By adhering to the outlined steps, you will replicate the results showcased during the interview.



Step 1: File Setup and installing required libraries

In total, there will be three files that you deal with:

final.py

runlocal.sh

runglobal.sh (optional – to check Inter Pi communication)



Install the below package in all the Pis - pip install rsa



Step 2: File Allocation Among Two Raspberry Pis

Ensure that both Raspberry Pis have a copy of final.py.

For intraPi connection -Transfer runlocal1.sh to the first Raspberry Pi. 

Optional for inter Pi connections - Move runGlobal.sh to the second Raspberry Pi. 



Step 3: Run runlocal.sh to simulate Intra Pi communication



# runlocal.sh-  This script is used to automate the process of running multiple Python scripts concurrently using Tmux. To use this script, you need to have Tmux installed on your system. 

./runlocal.sh -> to run the file.

The script will do the following:



# Simulating Itra Pi Networking

1. Create a new Tmux session named 'mySession'.

2. Start multiple Devices (Python scripts) in different Tmux windows.







How to navigate between devices [Terminals]- 
You can hop between sessions or terminal by [cmd + b] for Mac or [ cntrl +c ] for windows and then clicking the desired session. example - type "2" for soil 

   1 - mySession:1 -n 'weather' 

   2- mySession:2 -n 'soil' 

   3 - mySession:3 -n 'water'

   4 - mySession:4 -n 'drone' 

   5 - mySession:5 -n 'health'





4. The runlocal.sh already runs two scenarios 

The devices in this network are part of farm1

    # Scenario 1

    4.1 Where device 1- weather request temperature from device 2 - soil, which most of the time would process the sensor data and return Optimal temperature.

    # Scenario 2

    4.2 Where device 2- soil request speed from device 3 - drone, which most of the time would process the sensor data and return Dangerous speed.



    # Custom Scenario

    4.3 To check send custom Interest Packages between Devices in intra PI network go to the desired Session for the particular device and type send and click on enter. This allows you to send an interest package to the network . The interest package should be of the form network_name/device_type/sensor_data. egs- farm1/soil/temperature





Optional Step 4: Run runglobal on second Pi to check Inter Pi communication, Interest forwarding 

# Simulating Inter Pi networking 



    1 run runglobal.sh on the second Pi.

    2 The runglobal.sh already runs three scenarios 

	The devices in this network are part of farm2

    # Scenario 1

    2.1 Where device 1- weather request temperature from device 2 – soil of the farm2 itself ( same network), which would process the sensor data and return Optimal temperature.

    # Scenario 2

    2.2 Where device 2- soil from farm2 request speed from device 3 – drone from farm1, which would process the sensor data and return Dangerous speed. (shows inter Pi communication and interest forwarding as both these devices are not connected directly)

To simulate Forwarding request - data of a different kind from a different network is requestd . egs- farm1/drone/speed from farm2/weather.

    The interest package goes from farm2/weather to farm1/weather and then farm1/weather forwards it to farm1/drone. The Response also travels back in the same path.



    # Scenario 3

    2.3 To check node failure ,FIB updation, dynamic routing while forwarding interest package the bash file terminates health terminal i.e. session5 in 15 seconds. We can check in 5 seconds that the FIB is updated, and u can place a custom request from any device on either of the network to fetch data from both networks .

2.4 Then from farm1/health network ( Pi1) – 

2.5 Type send and click enter 

2.6 Then type “farm2/soil/temperature” to send the interest package. 

Node failure would be handled even though the link between farm1/health an farm2/health is cut off.



Optional

# Custom Scenario

    2.4 To check send custom Interest Packages between Devices in Inter PI network go to the desired Session for the particular device and type send and click on enter. This allows you to send an interest package to the network . The interest package should be of the form network_name/device_type/sensor_data. egs- farm1/weather/temperature.



