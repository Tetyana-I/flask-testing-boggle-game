from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle


class FlaskTests(TestCase):
    """ tests for view-functions """
    def setUp(self):
        """ before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_start_game(self):
        """ test rendering start.html """
        with self.client as client: 
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h4 class="h4">GAME RULES:</h4>', html)
             
    def test_game_renderHTML(self):
        """ test rendering a main game-page with game-board and statistics from session"""
        with self.client as client: 
            res = client.get('/game-load')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h4 class="h4">Game Statistics:</h4>', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highest_score'))
            self.assertIsNone(session.get('plays_num'))

    def test_check_guess(self):
        """ test a word-validation """
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["T", "E", "S", "T", "A"], ["A", "B", "C", "D", "E"], ["A", "B", "C", "D", "E"], ["A", "B", "C", "D", "E"], ["A", "B", "C", "D", "E"]] 
            res = self.client.get("/guess?word=test")         
            self.assertEqual(res.json['result'], 'ok')

    def test_if_english_word(self):
        """ test if a word is an English word """
        with self.client as client:
            client.get('/game-load')
            res = client.get('/guess?word=zhopa')
            self.assertEqual(res.json['result'], 'not-word')
            
    def test_highest_score(self):
        """ test if a new record was set """
        with self.client as client:
            client.get('/game-load')
            with client.session_transaction() as change_session:
                change_session['highest_score'] = 10
                change_session['plays_num'] = 2
            res = client.post("/game-over", json={'score': 5})
            self.assertEqual(res.json['newRecord'], False)
            

