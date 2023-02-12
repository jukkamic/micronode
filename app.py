from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

class Cart(Resource):
    def __init__(self):
        self.items = []

    def get(self):
        return {'items': self.items}

    def post(self):
        item = request.get_json()
        self.items.append(item)
        return {'item': item}, 201

api.add_resource(Cart, '/cart')

if __name__ == '__main__':
    app.run(debug=True)
