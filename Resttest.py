from flask import Flask, request, render_template, send_file
import requests
import json

app = Flask(__name__)

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
        token = response.json().get('access')
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
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=json_data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed: {response.status_code} - {response.text}")


# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure this points to your actual input form template


# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    id_number = request.form.get('id_number')
    serial_number = request.form.get('serial_number')

    try:
        token = get_auth_token(username, password)
        json_data = {
            "id_number": id_number,
            "serial_number": serial_number
        }
        data_response = make_request("/iprs/2/", token, json_data)



        return render_template('Test.html', data=data_response)  # Ensure 'Test.html' is the correct template name

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)
