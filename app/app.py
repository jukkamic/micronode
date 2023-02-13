from flask import Flask
from flask_graphql import GraphQLView
from graphene import Mutation,ObjectType, String, Int,Float, List, Schema, Field
from cart import Cart, CartItem
import json

app = Flask(__name__)




class Query(ObjectType):
    cart = List(CartItem)
    
    def resolve_cart(self, info):
        cart = Cart()
        cart.load()
        return cart.cart

class AddItemMutation(Mutation):
    class Arguments:
        name = String(required=True)
        price = Float(required=True)
        quantity = Int(required=True)

    cart_item = Field(CartItem)

    def mutate(self, info, **kwargs):
        # Add the item to the cart
        item = CartItem(name=kwargs["name"], price=kwargs["price"], quantity=kwargs["quantity"])
        cart = Cart()
        cart.add_item(item)
         
        return AddItemMutation(cart_item=item)
        #print("k")

class EmptyCartMutation(Mutation):
    empty_cart = Field(String)

    def mutate(self, info):
        cart = Cart()
        cart.empty_cart()
        return 'Cart emptied.'

class MyMutations(ObjectType):
    add_item = AddItemMutation.Field()
    empty_cart = EmptyCartMutation.Field()


def init_app():
    schema = Schema(query=Query, mutation=MyMutations)
    print(schema)
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        )
    )

init_app()

if __name__ == '__main__':
    app.run()

