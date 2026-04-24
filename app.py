from flask import(
    flash,
    Flask,
    render_template,
    redirect,
    session,
    url_for,
)

import random

app = Flask(__name__)
app.secret_key = 'secret'

POSSIBLE_WINNING_ROWS = (
        ('1', '2', '3'),  # top row of board
        ('4', '5', '6'),  # center row of board
        ('7', '8', '9'),  # bottom row of board
        ('1', '4', '7'),  # left column of board
        ('2', '5', '8'),  # middle column of board
        ('3', '6', '9'),  # right column of board
        ('1', '5', '9'),  # diagonal: top-left to bottom-right
        ('3', '5', '7'),  # diagonal: top-right to bottom-left
    )

CENTER_SQUARE = '5'

HUMAN_MARKER = 'X'
COMPUTER_MARKER = 'O'

def get_board_handle():
    if 'board' not in session:
        session['board'] = {str(square): '' for square in range(1, 10)}
    return session['board']

def unused_squares(board):
    return [square for square, mark in board.items() if mark == '']

def is_full(board):
    return len(unused_squares(board)) == 0

def three_in_a_row(marker, row, board):
    return all(board[square] == marker for square in row)

def is_winner(marker, board):
    for row in POSSIBLE_WINNING_ROWS:
        if three_in_a_row(marker, row, board):
            return True
        
    return False

def someone_won(board):
    return is_winner(HUMAN_MARKER, board) or is_winner(COMPUTER_MARKER, board)

def is_game_over(board):
    return is_full(board) or someone_won(board)

def count_markers_for(marker, row, board):
    return sum(board[square] == marker for square in row)

def critical_square(marker, board):
    for row in POSSIBLE_WINNING_ROWS:
        if count_markers_for(marker, row, board) == 2:
            for square in row:
                if square in unused_squares(board):
                    return square
    return None

def pick_center_square(board):
    if CENTER_SQUARE in unused_squares(board):
        return CENTER_SQUARE
    return None

def pick_random_square(board):
    return random.choice(unused_squares(board))

def computer_move(board):
    choice = critical_square(COMPUTER_MARKER, board)
    if choice is None:
        choice = critical_square(HUMAN_MARKER, board)
    if choice is None:
        choice = pick_center_square(board)
    if choice is None:
        choice = pick_random_square(board)
    return choice

@app.route('/')
def index():
    get_board_handle()
    return redirect(url_for('get_board'))

@app.route('/board/new', methods=['POST'])
def new_board():
    session['board'] = {str(square): '' for square in range(1, 10)}
    return redirect(url_for('get_board'))

@app.route('/board')
def get_board():
    board = get_board_handle()
    return render_template('board.html', board=board)

@app.route('/board/mark/<square>', methods=['POST'])
def add_marker(square):
    board = get_board_handle()
    if board[square]:
        flash(f'square {square} is already marked')
    else:
        board[square] = HUMAN_MARKER
        if is_game_over(board):
            if someone_won(board):
                if is_winner(HUMAN_MARKER, board):
                    flash('player won')
                else:
                    flash('computer won')
            else:
                flash('board is full')
            session.modified = True
            return redirect(url_for('get_board'))

        else:
            board[computer_move(board)] = COMPUTER_MARKER            
            if is_game_over(board):
                if someone_won(board):
                    if is_winner(HUMAN_MARKER, board):
                        flash('player won')
                    else:
                        flash('computer won')
                else:
                    flash('board is full')
                session.modified = True
                return redirect(url_for('get_board'))

        session.modified = True
        
    return redirect(url_for('get_board'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)