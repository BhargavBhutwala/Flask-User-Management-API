from flask import Flask, request, jsonify, make_response
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS globally for all routes, with specific origin
CORS(
   app,
   resources={r"/user/*": {"origins": "http://localhost:4200"}},
   supports_credentials=True
)

ma = Marshmallow(app)

# Global OPTIONS request handler
@app.after_request
def after_request(response):
   response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
   response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
   response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
   response.headers.add("Access-Control-Allow-Credentials", "true")  # Allow cookies if needed
   return response

@app.route("/<path:path>", methods=["OPTIONS"])
def handle_options(path):
   response = make_response()
   response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
   response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
   response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
   response.headers.add("Access-Control-Allow-Credentials", "true")
   return response

# Import controller after CORS and OPTIONS handler setup
from controller import *
