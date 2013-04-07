#!/usr/bin/env python

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

        f = open("person.csv", 'a')
        f.write(first_name + " " + last_name)
        f.close()

        return redirect(url_for('submitted'))

    return '''
        <form action="/new" method="post">
            <p><input type=text name=first_name>
            <p><input type=text name=last_name>
            <p><input type=submit value=Submit>
        </form>
    '''


@app.route("/new")
def new():
    return request.data


@app.route('/submitted')
def submitted():
    f = open("person.csv", 'r')
    full_name = f.readline()
    f.close()
    return full_name

if __name__ == '__main__':
    app.run(debug=True)
