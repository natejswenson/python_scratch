"""Weather API integration using WeatherStack and IP-based geolocation."""
import requests
from typing import Optional
from decouple import config

###########################################################################################
# Global variables
###########################################################################################
PAT = config('weather_pat')
WEATHER_URL = config('weather_url')
ZIP_URL = config('zipcode_url')
IP_URL = config('ip_url')

###########################################################################################
# get_temp_based_on_ip
# Use weatherstack API to return the current temperature for a zipcode
###########################################################################################
def get_temp_based_on_ip(zip_code: str) -> Optional[dict]:
    """
    Retrieve current temperature for a given zip code using WeatherStack API.

    Args:
        zip_code: The zip code to query weather for

    Returns:
        Weather data dictionary, or None if request fails
    """
    params = {
        'access_key': PAT,
        'query': zip_code,
        'units': 'f'
    }

    try:
        api_result = requests.get(f"{WEATHER_URL}/current", params=params, timeout=10)

        if api_result.status_code == 200:
            api_response = api_result.json()

            # Check if API returned an error
            if 'error' in api_response:
                print(f"Weather API error: {api_response['error'].get('info', 'Unknown error')}")
                return None

            print('Current temperature in %s is %d°F' %
                  (api_response['location']['name'],
                   api_response['current']['temperature']))
            return api_response
        else:
            print(f"Failed to retrieve weather data. Status code: {api_result.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error retrieving weather data: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing weather data: {e}")
        return None

###########################################################################################
# get_zipcode
# Use ip-api.com to get the current zipcode of a given IP address
###########################################################################################
def get_zipcode() -> Optional[str]:
    """
    Retrieve zip code based on public IP address.

    Returns:
        Zip code string, or None if retrieval fails
    """
    public_ip = get_public_ip()
    if not public_ip:
        return None

    url = f"{ZIP_URL}/{public_ip}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # Check for error status in response
            if data.get('status') == 'fail':
                print(f"IP geolocation error: {data.get('message', 'Unknown error')}")
                return None

            zipcode = data.get('zip')
            if not zipcode:
                print("No zip code found in response")
                return None
            return zipcode
        else:
            print(f"Failed to retrieve ZIP code. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error retrieving ZIP code: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing ZIP code data: {e}")
        return None

###########################################################################################
# get_public_ip
# Use ipinfo.io to get the IP address of computer
###########################################################################################
def get_public_ip() -> Optional[str]:
    """
    Retrieve the public IP address of the current machine.

    Returns:
        IP address string, or None if retrieval fails
    """
    try:
        response = requests.get(f'{IP_URL}', timeout=10)
        if response.status_code == 200:
            data = response.json()
            ip = data.get('ip')
            if not ip:
                print("No IP address found in response")
                return None
            return ip
        else:
            print(f"Failed to retrieve public IP address. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error retrieving public IP: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Error parsing IP data: {e}")
        return None



def main():
    """Main function to get weather based on current IP location."""
    try:
        zipcode = get_zipcode()
        if zipcode:
            get_temp_based_on_ip(zipcode)
        else:
            print("Unable to determine location from IP address.")
    except Exception as e:
        print(f"An error occurred while getting weather data: {e}")

if __name__ == "__main__":
    main()