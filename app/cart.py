import json
from graphene import Mutation,ObjectType, String, Int,Float, List, Schema, Field

class CartItem(ObjectType):
    name = String()
    price = Float()
    quantity = Float()
    
class Cart:
    def __init__(self):
        self.cart = []
        self.load()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def add_item(self, item):
        #item = {'name': name, 'price': price, 'quantity': quantity}
        self.cart.append(item)
        self.save()

    def add_item_with_params1(self,name,price,quantity):
        item=CartItem(name=name, price=price, quantity=quantity)
        self.cart.append(item)
        self.save()

    def empty_cart(self):
        self.cart = []
        self.save()

   

    @property
    def total(self):
        return sum(item.price * item.quantity * 1.05 for item in self.cart)

    def save(self):
        filename = 'cart.txt'
        with open(filename, 'w') as f:
            for item in self.cart:
                f.write(str(item.name)+ ','+str(item.quantity)+ ','+str(item.price) + '\n')

    def loadItem(self,line):
        item= CartItem()
        a=line.split(',')
        if len(a)>1:
            item.name=a[0]
            item.quantity=int(a[1])
            item.price=float(a[2])
            return item
        else:   
            return None

    def load(self):
        filename = 'cart.txt'
        try:
            with open(filename, 'r') as f:
                self.cart = [self.loadItem(line.strip()) for line in f]
                self.cart = [i for i in self.cart if i is not None]
        except FileNotFoundError:
            pass
        return self.cart

