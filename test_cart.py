import os
import json
import unittest
from app import Cart

class CartTestCase(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.cart.empty_cart()

    def test_add_item(self):
        self.cart.add_item('item1', 10, 1)
        self.cart.add_item('item2', 20, 2)

        filename = 'cart.txt'
        with open(filename, 'r') as f:
            items = [json.loads(line.strip()) for line in f]

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'item1')
        self.assertEqual(items[0]['price'], 10)
        self.assertEqual(items[0]['quantity'], 1)
        self.assertEqual(items[1]['name'], 'item2')
        self.assertEqual(items[1]['price'], 20)
        self.assertEqual(items[1]['quantity'], 2)

    def test_empty_cart(self):
        self.cart.add_item('item1', 10, 1)
        self.cart.add_item('item2', 20, 2)
        self.cart.empty_cart()

        filename = 'cart.txt'
        with open(filename, 'r') as f:
            items = [json.loads(line.strip()) for line in f]

        self.assertEqual(len(items), 0)

    def test_calculate_total(self):
        self.cart.add_item('item1', 10, 1)
        self.cart.add_item('item2', 20, 2)

        total = self.cart.total

        self.assertEqual(total, 52.5)

if __name__ == '__main__':
    unittest.main()
