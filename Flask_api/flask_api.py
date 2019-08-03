from flask import Flask,jsonify, request
from flask_restful import Resource, Api
from requests_intranet import test
import json
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']
        return test.Requesteo.recover(self,un,pw)


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)