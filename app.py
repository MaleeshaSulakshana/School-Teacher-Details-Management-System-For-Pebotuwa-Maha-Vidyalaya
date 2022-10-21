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
            database="pebotuwa_maha_vidyalaya",
            user="postgres",
            password="postgres")

    except Exception as e:
        print(str(e))

    return conn


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    if 'loggedId' not in session:
        return redirect('/login')

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
    if 'loggedId' not in session:
        return redirect('/login')

    return render_template('add_teacher.html')


# Route for view teacher details page
@app.route('/view-teacher')
def view_teacher():
    if 'loggedId' not in session:
        return redirect('/login')

    return render_template('view_teacher_details.html')


# Route for system users page
@app.route('/system-users')
def system_users():
    if 'loggedId' not in session:
        return redirect('/login')

    conn = connector()
    query = "SELECT first_name, last_name, username, user_type FROM public.system_users WHERE username != %s"
    values = (str(session['loggedId']),)
    cur = conn.cursor()
    cur.execute(query, values)
    details = cur.fetchall()

    return render_template('system_users.html', details=details)


# Route for add system user page
@app.route('/add-system-users')
def add_system_users():
    if 'loggedId' not in session:
        return redirect('/login')

    return render_template('add_system_user.html')


# Route for change psw page
@app.route('/change-psw')
def change_psw():
    if 'loggedId' not in session:
        return redirect('/login')

    conn = connector()
    query = "SELECT first_name, last_name, username, user_type FROM public.system_users WHERE username = %s"
    values = (str(session['loggedId']),)
    cur = conn.cursor()
    cur.execute(query, values)
    details = cur.fetchall()

    return render_template('change_psw.html', details=details)


# Route for change psw page
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route("/shutdown", methods=['GET', 'POST'])
def shutdown():
    session.clear()
    sig = getattr(signal, "SIGKILL", signal.SIGTERM)
    os.kill(os.getpid(), sig)


# Route for system login
@app.route('/system_login', methods=['GET', 'POST'])
def system_login():

    if request.method == "POST":

        if 'loggedId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            username = request.form.get('username')
            psw = request.form.get('psw')

            if (len(username) == 0 or len(psw) == 0):
                return jsonify({'error': "Fields are empty! (ආදාන ක්ෂේත්‍ර හිස්ය!)"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()

                # Check user is exist
                conn = connector()
                query = "SELECT username, user_type FROM public.system_users WHERE username = %s AND password = %s"
                values = (str(username), str(psw))
                cur = conn.cursor()
                cur.execute(query, values)
                details = cur.fetchall()

                if len(details) > 0:
                    session['loggedId'] = str(details[0][0])
                    session['type'] = str(details[0][1])
                    return jsonify({'redirect': url_for('index')})

                return jsonify({'error': "Sign in failed. Please try again! (පුරනය වීම අසාර්ථක විය. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('login')})


# Route for change psw
@app.route('/psw_change', methods=['GET', 'POST'])
def psw_change():

    if request.method == "POST":

        if 'loggedId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(psw) == 0 or len(cpsw) == 0):
                return jsonify({'error': "Fields are empty! (ආදාන ක්ෂේත්‍ර හිස්ය!)"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()

                # Check user is exist
                conn = connector()
                row_count = 0
                query = " UPDATE public.system_users SET password = %s WHERE username = %s"
                values = (str(psw), str(session['loggedId']))
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                row_count = cur.rowcount

                if row_count > 0:
                    return jsonify({'success': "Password has been updated! (මුරපදය යාවත්කාලීන කර ඇත!)"})

                else:
                    return jsonify({'error': "Password not updated. Please try again! (මුරපදය යාවත්කාලීන කර නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('login')})


# Route for add system user
@app.route('/add_new_system_user', methods=['GET', 'POST'])
def add_new_system_user():

    if request.method == "POST":

        if 'loggedId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            uname = request.form.get('uname')
            type = request.form.get('type')
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(fname) == 0 or len(lname) == 0 or len(uname) == 0 or len(type) == 0 or len(psw) == 0 or len(cpsw) == 0):

                return jsonify({'error': "Fields are empty! (ආදාන ක්ෂේත්‍ර හිස්ය!)"})

            elif psw != cpsw:
                return jsonify({'error': "Password are not matched (මුරපද තහවුරු කරන්න!)"})

            else:

                # Check username is exist
                conn = connector()
                query = "SELECT COUNT(*) FROM public.system_users WHERE username = %s"
                values = (str(uname),)
                cur = conn.cursor()
                cur.execute(query, values)

                if cur.fetchall()[0][0] > 0:
                    return jsonify({'error': "Username already exist! (පරිශීලක නාමය දැනටමත් පවතී!)"})

                psw = hashlib.md5(psw.encode()).hexdigest()

                # Insert data
                conn = connector()
                row_count = 0

                query = ''' INSERT INTO public.system_users (first_name, last_name, username, user_type, password) VALUES (%s, %s, %s, %s, %s) '''
                values = (str(fname), str(lname), str(
                    uname), int(type), str(psw))
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                row_count = cur.rowcount

                if row_count > 0:
                    return jsonify({'success': "Account has been created! (ගිණුම නිර්මාණය කර ඇත!)"})

                else:
                    return jsonify({'error': "Account not created. Please try again! (ගිණුම සාදා නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('index')})


# Route for add system user
@app.route('/remove_system_user', methods=['GET', 'POST'])
def remove_system_user():

    if request.method == "POST":

        if 'loggedId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            username = request.form.get('username')

            if (len(username) == 0):
                return jsonify({'error': "Fields are empty! (ආදාන ක්ෂේත්‍ර හිස්ය!)"})

            else:

                # Delete data
                conn = connector()
                row_count = 0

                query = ''' DELETE FROM public.system_users WHERE username = %s '''
                values = (str(username), )
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                row_count = cur.rowcount

                if row_count > 0:
                    return jsonify({'success': "System user has been removed! (පද්ධති පරිශීලකයා ඉවත් කර ඇත!)"})

                else:
                    return jsonify({'error': "System user not removed. Please try again! (පද්ධති පරිශීලකයා ඉවත් කර නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('index')})


# Main
if __name__ == '__main__':

    host = "0.0.0.0"
    port = "5001"
    # url = "http://127.0.0.1:{0}".format(port)
    # threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    # app.run(port=port, threaded=True, debug=True)
    app.run(host=host, port=port, threaded=True, debug=True)
