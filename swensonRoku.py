#imports
from roku import Roku
import re

#set roku ip address
roku=Roku('192.168.0.8')

#home method
def rokuHome():
   roku.home()

#select application
def selectApp(applications):
    print("Please select an application:")
    for i, app in enumerate(applications, start=1):
        print(f"{i}. {app}")
    # Get user input
    choice = int(input("Enter the number corresponding to the application: "))
    # Set the selected application as a variable
    selected_application = applications[choice - 1]
    selected_application_str=str(selected_application)
    number = re.search(r'\[(\d+)\]', selected_application_str).group(1)
    print(number)
    return number

def launchApp():
    apps=roku.apps
    number=selectApp(apps)
    app=roku[number].launch()
    

def getApps():
    apps=roku.apps
    print(apps)
    
#rokuHome()

launchApp()