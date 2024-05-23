import unittest
import requests


class TestJokesAPI(unittest.TestCase):
    def test_geek_jokes(self):
        url = 'https://insult.mattbas.org/api/insult'
        response = requests.get(url)
        self.assertEqual(200, response.status_code, "Must return 200 status code")
        joke = response.text
        self.assertIsNotNone(joke)
        print(joke)



if __name__ == '__main__':
    unittest.main()
