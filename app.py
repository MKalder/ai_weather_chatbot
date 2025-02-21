from flask import Flask, request, make_response, render_template_string, jsonify #type: ignore
from flask_cors import CORS,cross_origin #type: ignore
import json

from weather_condition.weather import Weather
from html.web_application import html_content

app = Flask(__name__)
CORS(app)

weather = Weather()

@app.route('/')
def index():
    """Endpoint to indicate that the webhook server is running"""

    return render_template_string(html_content)

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
    
    # Return the response
    return jsonify(response)

if __name__ == "__main__":
    """
    This is the application’s entry point. 
    It starts the Flask development server on port 5050 with debug mode enabled. 
    
    This setup is used with ngrok for local hosting and is only executed when the script runs directly, 
    not when imported as a module for cloud hosting. 
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

