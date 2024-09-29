from flask import Flask, render_template, request, jsonify
from zeep import Client
from zeep.exceptions import Fault
from zeep.helpers import serialize_object  # To convert Zeep object to a Python dict
import json

app = Flask(__name__)

# WSDL service URL
wsdl_url = 'https://dev.cpims.net/IPRSServerwcf?wsdl'

# Create a SOAP client
client = Client(wsdl=wsdl_url)


@app.route('/')
def index():
    return render_template('verifyId.html')


@app.route('/get_data', methods=['POST'])
def get_data():
    id_number = request.form.get('id_number')  # Get ID number from form
    serial_number = request.form.get('serial_number')  # Get ID number from form
    input_payload = {
        'id_number': id_number,
        'serial_number': serial_number,
    }

    try:
        # Call the GetDataByPassport method
        response = client.service.VerificationByIdCard(**input_payload)
        response_dict = serialize_object(response)

        # Check for errors in the response
        error_occurred = response_dict.get('ErrorOccurred', True)

        if not error_occurred:
            # Convert response to JSON format
            response_json = json.dumps(response_dict, indent=4)
            return jsonify({'success': True, 'data': response_json})
        else:
            # Handle error responses
            error_code = response_dict.get('ErrorCode', 'N/A')
            error_message = response_dict.get('ErrorMessage', 'Unknown error')
            return jsonify({'success': False, 'message': f"Error: {error_message} (Code: {error_code})"})

    except Fault as fault:
        return jsonify({'success': False, 'message': f"SOAP Fault: {fault}"})

    except Exception as e:
        return jsonify({'success': False, 'message': f"An error occurred: {e}"})


if __name__ == '__main__':
    app.run(debug=True)
