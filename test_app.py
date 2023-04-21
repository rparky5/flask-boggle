from unittest import TestCase

from app import app, games, GAME_ID_JSON_KEY

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
            self.assertIn("<!-- index page test id string -->",
                          html, "id comment string present in HTML")
            self.assertEqual(response.status_code, 200,
                             "status code should be 200")

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            ...
            # make a post request to /api/new-game
            response = client.post('/api/new-game')

            # get the response body as json using .get_json()
            json = response.get_json()

            game_id = json[GAME_ID_JSON_KEY]
            board = json["board"]

            # test that the game_id is a string
            self.assertIsInstance(game_id, str, "game_id is type string")

            # test that the board is a list
            self.assertIsInstance(board, list, "board is type list")
            self.assertIsInstance(board[0], list, "board should contain lists")

            # test that the game_id is in the dictionary of games (imported from app.py above)
            self.assertIn(game_id, games,
                          "key game_id in server games dictionary")

            self.assertEqual(response.status_code, 200,
                             "status code should be 200")

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:
            ...
            # make a post request to /api/new-game
            new_game_response = client.post("/api/new-game")

            # get the response body as json using .get_json()
            new_game_json = new_game_response.get_json()

            # find that game in the dictionary of games (imported from app.py above)
            game_id = new_game_json[GAME_ID_JSON_KEY]
            game = games[game_id]

            # manually change the game board's rows so they are not random
            game.board = ["C", "A", "T"], ["O", "X", "X"], ["X", "G", "X"]
            game.board_size = 3

            def _test_score_word_equals(
                    client,
                    game_id,
                    word,
                    expected_response_json,
                    expected_status_code):
                """Tests if a POST request to '/api/score-word' with the given
                game_id and word as input data returns as json expected_response_json.

                Requires a FlaskClient instance - client, and the 'self' instance from a BoggleAppTestCase
                - tester_self"""

                response = client.post("/api/score-word",
                                       json={GAME_ID_JSON_KEY: game_id, "word": word})

                score_word_json = response.get_json()
                self.assertEqual(
                    expected_response_json,
                    score_word_json,
                    f"{word} is valid word on board")

                self.assertEqual(response.status_code,
                                 expected_status_code,
                                 f"status code should be {expected_status_code}")

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            _test_score_word_equals(client, game_id, "CAT", {
                                    'result': 'ok'}, 200)

            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            _test_score_word_equals(client, game_id, "CATS", {
                                    'result': 'not-on-board'}, 200)

            # test to see that an invalid word returns {'result': 'not-word'}
            _test_score_word_equals(client, game_id, "XGX", {
                                    'result': 'not-word'}, 200)
