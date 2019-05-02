# Kombucha-Monitor
A python script to run on a raspberry pi, record temperature and humidity data, and uplaod it to google drive.

## Usage:
This script is meant to be run on a raspberry pi, with the GrovePi expansion board and the dht sensor. It requires the GrovePi libraries provided at https://www.dexterindustries.com/grovepi-tutorials-documentation/. Also requires Pydrive and all dependancies, found at https://pypi.org/project/PyDrive/.

In addition to having the required libraries installed on the pi, a client_secrets.json is required. This file can be obtained through googles developer console, I am not sharing mine for security reasons. With a valid client_secrets.json from google, the program will open a browser window and ask the user to sign into thier google account and allow the program access to their google drive contents. Finally the settings.yaml file is used to configure pydrive. This file is not required, or can be modified to suit different needs. The one provided in this repository will not require the user to log into google more than once. Using it as provided will create a credentials.json file that is used as a refresh token for the linked google account.
