from flask import Flask
from flask.json import jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
from flask import request
from flask import Response
from flask import send_file
import sys
import os
sys.path.append(os.getcwd())




app = Flask(__name__)
CORS(app)
api = Api(app)

#  

# @app.route('/', methods=["GET"])
# def index():
#     return "Welcome to API v1, try /hello."



if __name__ == "__main__":
    # app.run(host='127.0.0.1', debug=True, port=8010)
    app.run(host='0.0.0.0', debug=True, port=8010)

