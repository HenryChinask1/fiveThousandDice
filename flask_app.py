from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True

@app.route('/')
def home():
    return render_template('main_page.html')

