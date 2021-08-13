from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__) 

app.config['SECRET_KEY'] = "this-is-a-secret"
app.debug = True
toolbar = DebugToolbarExtension(app)


boggle_game = Boggle()
words = boggle_game.read_dict('words.txt')

@app.route('/')
def start_game():
    """ shows a homepage with user's instructions and button to start a game """
    return render_template('start.html')

@app.route('/game-load')
def game():
    """ gets a memory-game-board, sets up a session variables and generates an HTML-game-board"""
    board = boggle_game.make_board()
    session['board'] = board
    highest_score = session.get("highest_score", 0)
    plays_num = session.get("plays_num", 1)
    return render_template('boggle_game.html', board = board, highestscore = highest_score, playsnum = plays_num)

@app.route('/guess')
def check_guess():
    """ word-validation """
    guess = request.args["word"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, guess)
    return jsonify({'result': result})
    
@app.route('/game-over', methods=["POST"])
def best_score():
    """Receive score, update statistics """
    # import pdb
    # pdb.set_trace()
    score = request.json["score"]
    highest_score = session.get("highest_score",0)
    plays_num = session.get("plays_num",1)
    session['plays_num'] = plays_num + 1
    highest_score = max(score, highest_score)
    session['highest_score'] = highest_score
    return jsonify(newRecord = score > highest_score)