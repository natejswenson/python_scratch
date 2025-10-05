"""Roku device control and app launching utility."""
import re
from typing import List
from roku import Roku
from decouple import config

# Set roku IP address from environment or use default
roku_ip = config('roku_ip', default='192.168.0.8')
roku = Roku(roku_ip)

def roku_home() -> None:
    """Navigate Roku device to home screen."""
    roku.home()

def select_app(applications: List) -> str:
    """
    Display available applications and get user selection.

    Args:
        applications: List of available Roku applications

    Returns:
        Application ID number as string
    """
    print("Please select an application:")
    for i, app in enumerate(applications, start=1):
        print(f"{i}. {app}")

    # Get user input
    choice = int(input("Enter the number corresponding to the application: "))

    # Set the selected application as a variable
    selected_application = applications[choice - 1]
    selected_application_str = str(selected_application)
    number = re.search(r'\[(\d+)\]', selected_application_str).group(1)
    print(number)
    return number

def launch_app() -> None:
    """Launch a Roku application selected by the user."""
    apps = roku.apps
    number = select_app(apps)
    roku[number].launch()

def get_apps() -> None:
    """Display all available Roku applications."""
    apps = roku.apps
    print(apps)

def main() -> None:
    """Main function to launch Roku app selector."""
    launch_app()

if __name__ == "__main__":
    main()