import unittest
import app

class CartTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.client = self.app.test_client()
        

    def tearDown(self):
        response = self.client.delete('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {'message': 'Cart is now empty'})
        self.app = None
        self.client = None

    def test_get_empty_cart(self):
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {'items': [], 'total': 0})

    def test_post_to_cart(self):
        item = {'name': 'item1', 'price': 10, 'quantity': 2}
        response = self.client.post('/cart', json=item)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.get_json(), {'item': item, 'total': 21})

    def test_calculate_total(self):
        item1 = {'name': 'item1', 'price': 10, 'quantity': 2}
        item2 = {'name': 'item2', 'price': 5, 'quantity': 3}
        response = self.client.post('/cart', json=item1)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/cart')
        response = self.client.post('/cart', json=item2)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {'items': [item1, item2], 'total': 36.75})

if __name__ == '__main__':
    unittest.main()
