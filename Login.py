from flask import Flask, render_template, request, jsonify
from zeep import Client
from zeep.exceptions import Fault
from zeep.helpers import serialize_object

app = Flask(__name__)

# WSDL service URL
wsdl_url = 'https://dev.cpims.net/IPRSServerwcf?wsdl'


def check_wsdl_connection():
    try:
        client = Client(wsdl=wsdl_url)
        return client
    except Exception as e:
        return str(e)  # Return the error as a string to show on the frontend


def create_login_payload(username, password):
    return {
        'log': username,
        'pass': password
    }


def perform_login(client, username, password):
    # Create login payload
    login_payload = create_login_payload(username, password)

    try:
        # login credentials
        response = client.service.Login(**login_payload)

        # Check if response is None
        if response is None:
            return {'success': False, 'message': 'No response from login service.'}

        # Serialize the response
        response_dict = serialize_object(response)

        # Ensure response_dict is a dictionary before calling .get()
        if isinstance(response_dict, dict) and response_dict.get('LoginSuccess', False):

            return {'success': True, 'session_token': response_dict.get('SessionToken')}
        else:
            return {'success': False, 'message': "Invalid credentials. Please try again."}

    except Fault as fault:
        return {'success': False, 'message': f"SOAP Fault during login: {fault}"}

    except Exception as e:
        return {'success': False, 'message': f"An error occurred: {e}"}


def get_data_by_id(client, id_number, token):
    input_payload = {
        'id_number': id_number,
        'session_token': token
    }

    try:
        response = client.service.GetDataByIdCard(**input_payload)

        # Check if response is None
        if response is None:
            return {'success': False, 'message': 'No response from GetDataByIdCard service.'}

        # Serialize the response
        response_dict = serialize_object(response)

        # Ensure response_dict is a dictionary before calling .get()
        if isinstance(response_dict, dict) and not response_dict.get('ErrorOccurred', True):
            return {'success': True, 'data': response_dict}
        else:
            return {'success': False, 'message': response_dict.get('ErrorMessage', 'Unknown error')}

    except Fault as fault:
        return {'success': False, 'message': f"SOAP Fault: {fault}"}

    except Exception as e:
        return {'success': False, 'message': f"An error occurred: {e}"}


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check WSDL connection
    client = check_wsdl_connection()
    if isinstance(client, str):
        return jsonify({'success': False, 'message': f"Failed to connect to WSDL service: {client}"})

    # Perform login
    login_response = perform_login(client, username, password)
    if login_response['success']:
        return jsonify({'success': True, 'session_token': login_response['session_token']})
    else:
        return jsonify(login_response)


@app.route('/get_data', methods=['POST'])
def get_data():
    id_number = request.form.get('id_number')
    session_token = request.form.get('session_token')

    # Check WSDL connection
    client = check_wsdl_connection()
    if isinstance(client, str):
        return jsonify({'success': False, 'message': f"Failed to connect to WSDL service: {client}"})

    # Get data by ID
    data_response = get_data_by_id(client, id_number, session_token)
    return jsonify(data_response)


if __name__ == '__main__':
    app.run(debug=True)
