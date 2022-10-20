import os
import sys
import random
import hashlib
import datetime
import threading
import webbrowser
import signal
import psycopg2
from flask import Flask, render_template, redirect, jsonify, url_for, request, session

app = Flask(__name__)
app.env = "development"

app.secret_key = "School_Teachers_Details_Management_System"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def connector():
    conn = ""

    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="pebotuwa_Maha_vidyalaya",
            user="postgres",
            password="postgres")

    except Exception as e:
        print(str(e))

    return conn


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    # if 'loggedId' not in session:
    #     return redirect('/login')
    today = datetime.date.today()
    current_teachers_count = 10
    retired_teachers_count = 20
    system_users_count = 2

    counts = [current_teachers_count,
              retired_teachers_count, system_users_count]

    return render_template('index.html', today=today, counts=counts)


# Route for login page
@app.route('/login')
def login():
    if 'loggedId' in session:
        return redirect('/index')

    return render_template('login.html')


# Route for add teacher page
@app.route('/add-teacher')
def add_teacher():
    # if 'loggedId' not in session:
    #     return redirect('/login')

    return render_template('add_teacher.html')


# Route for view teacher details page
@app.route('/view-teacher')
def view_teacher():
    # if 'loggedId' not in session:
    #     return redirect('/login')

    return render_template('view_teacher_details.html')


# Route for system users page
@app.route('/system-users')
def system_users():
    # if 'loggedId' not in session:
    #     return redirect('/login')

    return render_template('system_users.html')


# Route for add system user page
@app.route('/add-system-users')
def add_system_users():
    # if 'loggedId' not in session:
    #     return redirect('/login')

    return render_template('add_system_user.html')


# Route for change psw page
@app.route('/change-psw')
def change_psw():
    # if 'loggedId' not in session:
    #     return redirect('/login')

    return render_template('change_psw.html')


# Route for change psw page
@app.route('/logout')
def logout():
    # if 'loggedId' not in session:
    #     return redirect('/login')

    return redirect('/login')


# @app.route("/shutdown", methods=['GET', 'POST'])
# def shutdown():
#     session.clear()
#     sig = getattr(signal, "SIGKILL", signal.SIGTERM)
#     os.kill(os.getpid(), sig)


# Main
if __name__ == '__main__':

    host = "0.0.0.0"
    port = "5001"
    # url = "http://127.0.0.1:{0}".format(port)
    # threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    # app.run(port=port, threaded=True, debug=True)
    app.run(host=host, port=port, threaded=True, debug=True)
