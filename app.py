import os
import json
from flask import Flask
from flask_graphql import GraphQLView
import graphene

app = Flask(__name__)

class Item(graphene.ObjectType):
    name = graphene.String()
    price = graphene.Float()
    quantity = graphene.Int()

class Cart(graphene.ObjectType):
    items = graphene.List(Item)
    total = graphene.Float()

    def __init__(self):
        self.filename = 'cart.txt'
        self.items = self.resolve_items()
        self.total = sum(item.price * item.quantity for item in self.items) * 1.05

    def resolve_items(self):
        items = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                items = [json.loads(line.strip()) for line in f]
        return [Item(**item) for item in items]

    def add_item(self, name, price, quantity):
        item = {'name': name, 'price': price, 'quantity': quantity}
        with open(self.filename, 'a') as f:
            f.write(json.dumps(item) + '\n')

    def empty_cart(self):
        open(self.filename, 'w').close()

class AddItemMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        quantity = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, name, price, quantity):
        cart = Cart()
        cart.add_item(name=name, price=price, quantity=quantity)
        return AddItemMutation(success=True)

class EmptyCartMutation(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        cart = Cart()
        cart.empty_cart()
        return EmptyCartMutation(success=True)

class MyMutations(graphene.ObjectType):
    add_item = graphene.Field(AddItemMutation)
    empty_cart = graphene.Field(EmptyCartMutation)

class Query(graphene.ObjectType):
    cart = graphene.Field(Cart)

    def resolve_cart(self, info):
        return Cart()

schema = graphene.Schema(query=Query, mutation=MyMutations)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run()
