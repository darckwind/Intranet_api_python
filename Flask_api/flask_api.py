from flask import Flask
from flask_restful import Resource, Api
from requests_intranet import test
import json
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        test.Requesteo.contructor(self,"rut","clave intranet")
        return test.Requesteo.recover()

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)