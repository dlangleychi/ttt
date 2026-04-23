from flask import(
    flash,
    Flask,
    render_template,
    redirect,
    session,

    url_for,
)

import oo_ttt

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
    session['board'] = {square: '' for square in range(1, 10)}
    return redirect(url_for('get_board'))

@app.route('/board')
def get_board():
    return render_template('board.html', board=session['board'])

@app.route('/board/mark/<square>')
def add_marker(square):
    if session['board'][square]:
        flash(f'square {square} is already marked')
    else:
        session['board'][square] = 'X'
        session.modified = True
    return redirect(url_for('get_board'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)