from flask import Flask, request, make_response 
from flask_cors import CORS,cross_origin 
import json

from weather_condition.weather import Weather

app = Flask(__name__)
CORS(app)

weather = Weather()

@app.route('/')
def index():
    """Endpoint to indicate that the webhook server is running"""

    return 'Webhook is running!'

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    """
    Endpoint to handle Dialogflow fulfillment requests

    This endpoint receives a POST request from Google Dialogflow ES with a JSON payload
    containing the request data. The function processes the request and returns
    a JSON response according to the Google Dialogflow ES fulfillment response format.

    Returns:
        A JSON response containing the response from the fulfillment code.
    """

    # Get the request data from Google Dialogflow ES request
    request_json = request.get_json(silent=True, force=True)

    # Process the request using the Weather class
    response = weather.process_request(request_json)

    # Convert the response to a JSON string
    response_json = json.dumps(response)

    # Set the Content-Type header to application/json
    response_headers = {
        'Content-Type': 'application/json'
    }

    # Return the response
    return make_response(response_json, response_headers)

if __name__ == "__main__":
    """
    This is the entry point of the application. It starts the Flask
    development server on port 5050 and enables debug mode.

    This is only executed when the script is run directly, not when it is
    imported as a module, such as when hosted on PythonAnywhere. 
    """
    # Start the Flask development server
    app.run(
        # The host IP address to bind to
        host="0.0.0.0",
        # The port number to listen on
        port=5050,
        # Enable debug mode
        debug=True
    )

