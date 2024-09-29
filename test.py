import requests
import json
##Rest  Framework
# Base URL for the IPRS API
base_url = "https://ovc.childprotection.uonbi.ac.ke/api"

# Authentication credentials
username = "testhealthit"
password = "T3st@987654321"

# Authentication endpoint
auth_url = f"{base_url}/token/"

# Function to get the authentication token
def get_auth_token(username, password):
    auth_data = {
        "username": username,
        "password": password
    }
    response = requests.post(auth_url, data=auth_data)

    if response.status_code == 200:
        print("Auth response:", response.json())
        token = response.json().get('access')  # Get 'access' token

        if token:
            return token
        else:
            raise Exception("Access token not found in the response")
    else:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

# Function to make API requests with the token
def make_request(endpoint, token, json_data=None):
    url = f"{base_url}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"  # Set content type to JSON
    }

    print("Request URL:", url)
    print("Headers:", headers)
    print("JSON Data:", json_data)  # Print JSON data being sent

    # If json_data is provided, use POST; otherwise, use GET
    if json_data:
        response = requests.get(url, headers=headers, json=json_data)   # Use json parameter for sending data
    else:
        response = requests.get(url, headers=headers)  # Use GET request

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed: {response.status_code} - {response.text}")

# Main function to run the different endpoints
def main():
    try:
        # Get the authentication token
        token = get_auth_token(username, password)
        print("Authentication successful. Token obtained.")

        # 1. /iprs/2/ - GetDataByIdCard
        id_number = '39896713'  # Use an actual ID number
        serial_number = " "  # Use a valid serial number or a placeholder

        # Prepare JSON data for the request
        json_data = {
            "id_number": id_number,
            "serial_number": serial_number
        }

        # Make the API request
        data_by_id_card = make_request("/iprs/2/", token, json_data)

        print("Data by ID Card:", json.dumps(data_by_id_card, indent=4))  # Pretty print the JSON response

    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the script
if __name__ == "__main__":
    main()
