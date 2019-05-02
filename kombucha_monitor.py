#!/usr/bin/env python

import datetime
import time
import os
from shutil import copyfile
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from grovepi import *

SLEEP_TIME = 3

dht_sensor_port = 7
dht_sensor_type = 0

g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)


def upload(file):
    print("uploaded", file)
    #copyfile(file, "uploaded %s" % file)
    with open(file, 'r') as upload_file:
        file_drive = drive.CreateFile({'title:': 'temp'})
        file_drive['title'] = file
        file_drive.SetContentString(upload_file.read())
        file_drive.Upload()
        upload_file.close()

# set loop delay time in seconds, must be less than 1000
loopdelay = 5

# set time at which to upload to google drive
upload_time = datetime.time(12, 0, 0)



# generate two time objects to represent a range of time using the loop delay
# to make sure the current time will only be within the update range once per day
upload_time_begin = datetime.time(upload_time.hour, upload_time.minute, upload_time.second)

minuteoffset = loopdelay/60
secondoffset = loopdelay%60
upload_time_end = datetime.time(upload_time.hour, (upload_time.minute + minuteoffset), (upload_time.second + secondoffset))


# object to hold the currrent time
now = datetime.datetime.now().time()
today = datetime.datetime.now().date()


# check to see if there is an old log file; if there is delete it
if os.path.exists("logdata.tmp"):
    os.remove("logdata.tmp")

#initalize temp file to hold the log data as it is produced
tempfile = open("logdata.tmp", 'w')

# begin file with time program was started
print("Program started at %s on %s\n" % (now.strftime("%H:%M:%S"), today))
tempfile.write("Log started at %s on %s\n" % (now.strftime("%H:%M:%S"), today))

#print(upload_time_begin)
#print(upload_time_end)

[temperature, humidity] = dht(dht_sensor_port, dht_sensor_type)


# Main loop
while True:
    #try block to catch if the user intrupts the script running
    try:

        #update the now time
        now = datetime.datetime.now().time()
        today = datetime.datetime.now().date()

        # if now is between upload time and loopdelay seconds after that time:
        if upload_time_begin < now < upload_time_end:
            #close the file
            tempfile.close()
            # generate logfile final na,e
            logfilename = "%s.dat" % datetime.datetime.now().date()
            #copy contents of temp file to final log file form
            copyfile("logdata.tmp", logfilename)
            # will be uploading logic
            upload(logfilename)

            # delete old files
            os.remove("logdata.tmp")
            os.remove(logfilename)

            # open new tempfile and write the first line
            tempfile = open("logdata.tmp", 'w')
            tempfile.write("Log started at %s on %s\n" % (now, today))

        # get/write data to the file
        [temperature, humidity] = dht(dht_sensor_port, dht_sensor_type)

        tempstring = now.strftime("%H:%M:%S") + "| TEMPERATURE: " + str(temperature) + "   | HUMIDITY: " + str(humidity) + "\n"
        tempfile.write(tempstring)
        print(tempstring)

        # wait for a user difined number of seconds
        time.sleep(loopdelay)

    except KeyboardInterrupt:
        tempfile.close()
        interruptfile = "%s-interrupt.dat" % datetime.datetime.now().date()
        copyfile("logdata.tmp", interruptfile)
        upload(interruptfile)
        os.remove(interruptfile)

        break
