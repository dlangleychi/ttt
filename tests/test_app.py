import unittest

from app import app

class TTTTest(unittest.TestCase):
    
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret"
        app.config["SESSION_COOKIE_NAME"] = "test_session"
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()