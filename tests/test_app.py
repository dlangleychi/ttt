# test_app.py

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

    def test_index_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tic Tac Toe', response.get_data(as_text=True))
        self.assertNotIn('X', response.get_data(as_text=True))

    def test_board_alone(self):
        response = self.client.get('/board')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tic Tac Toe', response.get_data(as_text=True))
        self.assertNotIn('X', response.get_data(as_text=True))
        self.assertNotIn(' O ', response.get_data(as_text=True))

    def test_mark_square(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        mark_response = self.client.post('/board/mark/5', follow_redirects=True)
        self.assertEqual(mark_response.status_code, 200)
        self.assertIn('X', mark_response.get_data(as_text=True))

    def test_double_mark(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        mark_response = self.client.post('/board/mark/5', follow_redirects=True)
        self.assertEqual(mark_response.status_code, 200)
        self.assertIn('X', mark_response.get_data(as_text=True))

        mark_response_2 = self.client.post('/board/mark/5', follow_redirects=True)
        self.assertEqual(mark_response_2.status_code, 200)
        self.assertIn('square 5 is already marked', 
                      mark_response_2.get_data(as_text=True))
        
    def test_computer_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        mark_response = self.client.post('/board/mark/5', follow_redirects=True)
        self.assertEqual(mark_response.status_code, 200)
        self.assertIn('X', mark_response.get_data(as_text=True))
        self.assertRegex(mark_response.get_data(as_text=True), r'O(?!C)')

    def test_new_board(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        mark_response = self.client.post('/board/mark/5', follow_redirects=True)
        self.assertEqual(mark_response.status_code, 200)
        
        new_response = self.client.post('/board/new', follow_redirects=True)
        self.assertEqual(new_response.status_code, 200)
        self.assertIn('Tic Tac Toe', new_response.get_data(as_text=True))
        self.assertNotIn('X', new_response.get_data(as_text=True))
        self.assertNotIn(' O ', new_response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()