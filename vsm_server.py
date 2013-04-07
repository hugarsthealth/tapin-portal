#!/usr/bin/env python

import os
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/add_info', methods=['GET', 'POST'])
def add_info():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        return redirect(url_for('submitted'))
    return '''
        <form action="" method="post">
            <p><input type=text name=first_name>
            <p><input type=text name=last_name>
            <p><input type=submit value=Submit>
        </form>
    '''
    
@app.route('/submitted')
def submitted():
    return "Submitted"

if __name__ == '__main__':
    app.run()
