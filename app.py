from flask import Flask,request
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')


class Cart(Resource):
    def __init__(self):
        self.filename = 'cart.txt'
        self.items = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.items = [eval(line.strip()) for line in f]

    def get(self):
        return {'items': self.items, 'total': self.calculate_total()}

    def post(self):
        item = request.get_json()
        self.items.append(item)
        with open(self.filename, 'a') as f:
            f.write(str(item) + '\n')
        return {'item': item, 'total': self.calculate_total()}, 201

    def delete(self):
        self.items = []
        open(self.filename, 'w').close()
        return {'message': 'Cart is now empty'}

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item['price'] * item['quantity']
        return total * 1.05  # Add 5% tax


api.add_resource(Cart, '/cart')

if __name__ == '__main__':
    app.run(debug=True)
