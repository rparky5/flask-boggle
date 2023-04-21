from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            # test that you're getting a template
            html = response.get_data(as_text=True)
            self.assertIn("<!-- index page test id string -->", html, "id comment string present in HTML")
            self.assertEqual(response.status_code, 200, "status code should be 200")

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            ...
            # make a post request to /api/new-game
            response = client.post('/api/new-game')

            # get the response body as json using .get_json()
            json = response.get_json()

            game_id = json["game_id"]
            # test that the game_id is a string
            self.assertIsInstance(game_id, str, "game_id is type string")
            # test that the board is a list
            self.assertIsInstance(json["board"], list, "board is type list")
            # test that the game_id is in the dictionary of games (imported from app.py above)
            self.assertIn(game_id, games, "key game_id in server games dictionary")

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:
            ...
            # make a post request to /api/new-game
            response = client.post("/api/new-game")

            # get the response body as json using .get_json()
            json = response.get_json()

            # find that game in the dictionary of games (imported from app.py above)
            game_id = json["game_id"]
            game = games[game_id]

            # manually change the game board's rows so they are not random
            game.board = [["H", "E", "L", "L", "O"]]


            # test to see that a valid word on the altered board returns {'result': 'ok'}
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            # test to see that an invalid word returns {'result': 'not-word'}