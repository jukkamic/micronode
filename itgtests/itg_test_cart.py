import unittest
import requests
import json

class CartIntegrationTest(unittest.TestCase):
    def test_cart(self):
        # Define the GraphQL query to retrieve the cart items
        query = """
        query {
          cart {
            name
            price
            quantity
          }
        }
        """

        # Define the GraphQL mutation to add an item to the cart
        mutation = """
        mutation {
  
    addItem(name:"a",price:10.0,quantity:3){
    	cartItem{
        name
        price
        quantity
    
      }
    }
}
        """


        # Make a POST request to the GraphQL endpoint with the query
        response = requests.post('http://localhost:5000/graphql', json={'query': query})

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        response_json = json.loads(response.text)

        # Check that the response contains an empty list of cart items
        self.assertEqual(response_json['data']['cart'], [])

        # Make a POST request to the GraphQL endpoint with the mutation
        response = requests.post('http://localhost:5000/graphql', json={'query': mutation})
        print(response.text)
        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        print(response.text)
        # Parse the JSON response
        response_json = json.loads(response.text)

        # Check that the response contains the expected cart item
        self.assertEqual(response_json['data']['addItem']['cartItem'], {'name': 'a', 'price': 10.0, 'quantity': 3.0})

        # Make a POST request to the GraphQL endpoint with the query again
        response = requests.post('http://localhost:5000/graphql', json={'query': query})

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        response_json = json.loads(response.text)

        # Check that the response contains the expected cart item
        self.assertEqual(response_json['data']['cart'], [{'name': 'a', 'price': 10.0, 'quantity': 3.0}])

if __name__ == '__main__':
    unittest.main()
