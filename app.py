from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api,Resource
import hashlib



app=Flask(__name__)
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'aavani'
app.config['MYSQL_PASSWORD'] = 'aavani123'
app.config['MYSQL_DB'] = 'TwoFactor'

mysql = MySQL(app)


@app.route('/api/v1/twofactor/create_delivery_method', methods=['POST'])
def create_delivery_method():
    try:
        # Get delivery method data from the request
        data = request.json

        if 'name' in data and 'target' in data:
            name = data['name']
            target = data['target']

            # Create a cursor to interact with the MySQL database
            cursor = mysql.connection.cursor()

            # Insert the new delivery method into the database, without specifying user_id
            cursor.execute("INSERT INTO delivery_methods (name, target) VALUES (%s, %s)", (name, target))

            # Commit the changes to the database
            mysql.connection.commit()

            # Close the cursor
            cursor.close()

            return jsonify({"message": "Delivery method created successfully."})
        else:
            return jsonify({"error": "Invalid data provided for creating a delivery method."})
    except Exception as e:
        return jsonify({"error": "An error occurred while creating the delivery method.", "details": str(e)})
    


@app.route('/api/v1/twofactor/get_delivery_methods', methods=['GET'])
def get_delivery_methods():
    try:
        # Create a cursor within a context manager to interact with the MySQL database
        with mysql.connection.cursor() as cursor:
            # Execute an SQL query to fetch delivery methods
            cursor.execute("SELECT name, target FROM delivery_methods")
            delivery_methods = cursor.fetchall()

        # Convert the results to a list of dictionaries for JSON serialization
        delivery_methods_list = [{'name': method[0], 'target': method[1]} for method in delivery_methods]

        return jsonify(delivery_methods_list)
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching delivery methods.", "details": str(e)})
    
import datetime
# import random
# def generate_otp():
#     return ''.join([str(random.randint(0,9))for _ in range(6)])
# @app.route('/api/v1/twofactor/requests_otp', methods=['POST'])
# def request_otp():
#     try:
#         # Get JSON data from the request
#         data = request.json

#         # Extract the necessary fields from the JSON data
#         delivery_method = data['deliveryMethod']['name']
#         target = data['deliveryMethod']['target']
#         request_time = data['requestTime'] / 1000
#         token_live_time = data['tokenLiveTimeInSec']
#         extended_access_token = data['extendedAccessToken']
#         request_time = datetime.datetime.fromtimestamp(request_time)
#         otp=generate_otp()

#         # Create a cursor within a context manager to interact with the MySQL database
#         with mysql.connection.cursor() as cursor:
#             # Insert the data into the database
#             cursor.execute(
#                  "INSERT INTO otp_requests (delivery_method, target, request_time, token_live_time, extended_access_token, otp) VALUES (%s, %s, %s, %s, %s, %s)",
#                 (delivery_method, target, request_time, token_live_time, extended_access_token, otp)
#             )

#             # Commit the changes to the database
#             mysql.connection.commit()

#         # return jsonify({"message": "OTP request successfully stored in the database."})
#         return jsonify({"otp":otp})
#     except Exception as e:
#         return jsonify({"error": "An error occurred while processing the OTP request.", "details": str(e)})




import datetime
import random

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

@app.route('/api/v1/twofactor/requests_otp', methods=['POST'])
def request_otp():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract the necessary fields from the JSON data
        delivery_method = data['deliveryMethod']['name']
        target = data['deliveryMethod']['target']
        request_time = data['requestTime'] / 1000
        token_live_time = data['tokenLiveTimeInSec']
        extended_access_token = data['extendedAccessToken']
        request_time = datetime.datetime.fromtimestamp(request_time)
        otp = generate_otp()

        # Create a cursor within a context manager to interact with the MySQL database
        with mysql.connection.cursor() as cursor:
            # Insert the data into the database, including the generated 'otp'
            cursor.execute(
                "INSERT INTO otp_requests (delivery_method, target, request_time, token_live_time, extended_access_token, otp) VALUES (%s, %s, %s, %s, %s, %s)",
                (delivery_method, target, request_time, token_live_time, extended_access_token, otp)
            )

            # Commit the changes to the database
            mysql.connection.commit()

        # Return the generated OTP in the response
        return jsonify({"otp": otp})
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the OTP request.", "details": str(e)})

import string
@app.route('/api/v1/twofactor/validate_otp', methods=['POST'])
# def validate_otp(otp_to_validate):
#     try:
#         data = request.json

#         # Extract the OTP from the request data
#         provided_otp = data.get('otp')

#         # Perform OTP validation (replace this with your validation logic)
#         is_valid = validate_otp(provided_otp)

#         if is_valid:
#             # If the OTP is valid, generate a response with token, validFrom, and validTo
#             current_time = int(datetime.datetime.now().timestamp())
#             valid_from = current_time
#             valid_to = valid_from + 3600  # Valid for 1 hour (adjust as needed)

#             response_data = {
#                 "token": generate_token(),  # Implement your token generation logic
#                 "validFrom": valid_from,
#                 "validTo": valid_to
#             }

#             return jsonify(response_data), 200
#         else:
#             return jsonify({"error": "Invalid OTP"}), 400

#     except Exception as e:
#         return jsonify({"error": "An error occurred while validating OTP.", "details": str(e)})



