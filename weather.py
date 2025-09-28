##########################################################
#imports
##########################################################
import requests
from decouple import config

###########################################################################################
#global_vars
###########################################################################################
PAT = config('weather_pat')
WEATHER_URL = config('weather_url')
ZIP_URL= config('zipcode_url')
IP_URL=config('ip_url')

###########################################################################################
#get_temp_based_on_ip
#use weatherstapck api to return the current temperature for a zipcode
###########################################################################################
def get_temp_based_on_ip(zip):
    params = {
    'access_key':PAT,
    'query': zip,
    'units':'f'
    }

    api_result = requests.get(f"{WEATHER_URL}/current", params)

    api_response = api_result.json()

    print('Current temperature in %s is %d°F' \
        % (api_response['location']['name'], \
        api_response['current']['temperature']))

###########################################################################################
#get_zipcode
#use ip-api.com to get the current the zipcode of a given ip address
###########################################################################################
def get_zipcode():
    public_ip = get_public_ip()
    url = f"{ZIP_URL}/{public_ip}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        zipcode = data['zip']
        return zipcode
    else:
        print(f"Failed to retrieve ZIP code. Status code: {response.status_code}")
        return None
       
###########################################################################################
#get_public_ip
#use ipinfo.io to get the ip address of computer
###########################################################################################
def get_public_ip():
    try:
        response = requests.get(f'{IP_URL}')
        if response.status_code == 200:
            data = response.json()
            return data.get('ip')
        else:
            print(f"Failed to retrieve public IP address. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
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