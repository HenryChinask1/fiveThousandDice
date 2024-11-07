from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def home():
    return 'Hello from Flask'

