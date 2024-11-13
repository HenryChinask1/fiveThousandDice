from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__, static_url_path='/static')
#app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('main_page.html')

@app.route('/rules')
def rules():
    return render_template('rules_page.html')

@app.route('/nana', methods=['GET', 'POST'])
def nana():
    if request.method == 'GET':
        return render_template('nana_page.html')
    return redirect(url_for('nana'))

@app.route('/game', methods=["GET", "POST"])
def game():
    if request.method == "GET":
        return render_template('game_page.html')
    return redirect(url_for('game'))