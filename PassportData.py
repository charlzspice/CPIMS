import json
from zeep import Client
from zeep.exceptions import Fault
from zeep.helpers import serialize_object  # To convert Zeep object to a Python dict

# WSDL service URL
wsdl_url = 'https://dev.cpims.net/IPRSServerwcf?wsdl'

# Create a SOAP client
client = Client(wsdl=wsdl_url)

# Input payload for GetDataByIdCard method
id_number = '39896713'  # Replace with the actual ID number
input_payload = {
    'id_number': id_number,
}

try:
    # Call the GetDataByIdCard method
    response = client.service.GetDataByPassport(**input_payload)
    response_dict = serialize_object(response)

    # Convert response to JSON format
    response_json = json.dumps(response_dict, indent=4)

    # Check for errors in the response
    error_occurred = response_dict.get('ErrorOccurred', True)

    if not error_occurred:
        # Successful retrieval of person's data
        print("Person's Data Retrieved Successfully in JSON Format:")
        print(response_json)
    else:
        # Handle error responses
        error_code = response_dict.get('ErrorCode', 'N/A')
        error_message = response_dict.get('ErrorMessage', 'Unknown error')
        print(f"Error Occurred: {error_message} (Code: {error_code})")

except Fault as fault:
    # Handle SOAP errors
    print(f"SOAP Fault: {fault}")

except Exception as e:
    # Handle other exceptions
    print(f"An error occurred: {e}")
