import os
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


db_host = "localhost"
db_port = "5432"
db_name = "pebotuwa_maha_vidyalaya"
db_user = "postgres"
db_password = "postgres"


def connector():
    conn = None

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )

    except Exception as e:
        print(f"{str(e)}")

    return conn


# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html'), 404


# 500 page
@app.route('/error')
def error_page():
    return render_template('error-500.html'), 500


# Route for create database
@app.route('/create_db')
def create_db():
    if 'loggedId' in session:
        return redirect('/index')

    checkConn = connector()
    if checkConn is not None:
        return redirect('/index')

    # connection establishment
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database="postgres",
        user=db_user,
        password=db_password
    )

    conn.autocommit = True

    # Create database
    cursor = conn.cursor()
    create_database = '''
            CREATE DATABASE pebotuwa_maha_vidyalaya
            WITH
            OWNER = postgres
            ENCODING = 'UTF8'
            CONNECTION LIMIT = -1
            IS_TEMPLATE = False;
        '''
    cursor.execute(create_database)

    # Create tables and insert data
    queries = []

    queries.append(''' DROP TABLE IF EXISTS public.system_users; ''')

    queries.append('''
             CREATE TABLE IF NOT EXISTS public.system_users
             (
                 first_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
                 last_name character varying(128) COLLATE pg_catalog."default" NOT NULL,
                 username character varying(64) COLLATE pg_catalog."default" NOT NULL,
                 user_type integer NOT NULL,
                 password character varying(255) COLLATE pg_catalog."default" NOT NULL
             )
             TABLESPACE pg_default;
         ''')

    queries.append('''
             ALTER TABLE IF EXISTS public.system_users
                 OWNER to postgres;
         ''')

    queries.append(''' DROP TABLE IF EXISTS public.teachers; ''')

    queries.append('''
             CREATE TABLE IF NOT EXISTS public.teachers
             (
                 full_name character varying COLLATE pg_catalog."default" NOT NULL,
                 full_name_initials character varying COLLATE pg_catalog."default" NOT NULL,
                 dob character varying(16) COLLATE pg_catalog."default" NOT NULL,
                 nic character varying(16) COLLATE pg_catalog."default" NOT NULL,
                 address character varying(255) COLLATE pg_catalog."default" NOT NULL,
                 distance character varying(255) COLLATE pg_catalog."default" NOT NULL,
                 tp_land character varying(16) COLLATE pg_catalog."default",
                 tp_mobile character varying(16) COLLATE pg_catalog."default",
                 email character varying COLLATE pg_catalog."default",
                 married_person_name character varying COLLATE pg_catalog."default",
                 married_person_job character varying COLLATE pg_catalog."default",
                 original_appointment_date character varying(16) COLLATE pg_catalog."default",
                 grade_class character varying COLLATE pg_catalog."default",
                 salary_implement_date character varying COLLATE pg_catalog."default",
                 previous_serviced_schools character varying COLLATE pg_catalog."default",
                 education_qualifications character varying COLLATE pg_catalog."default",
                 id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
                 status integer NOT NULL,
                 CONSTRAINT teachers_pkey PRIMARY KEY (id)
             )
             TABLESPACE pg_default;
         ''')

    queries.append('''
             ALTER TABLE IF EXISTS public.teachers
                 OWNER to postgres;
         ''')

    queries.append('''
             INSERT INTO public.system_users(first_name, last_name, username, user_type, password)
                 VALUES ('Admin', 'Admin', 'admin', '1', '21232f297a57a5a743894a0e4a801fc3');
         ''')

    try:
        conn = connector()
        with conn, conn.cursor() as cur:
            for query in queries:
                cur.execute(query)

            conn.commit()

    finally:
        if conn:
            conn.close()

    return redirect('/index')


# Route for login page
@app.route('/login')
def login():
    if 'loggedId' in session:
        return redirect('/index')

    conn = connector()
    if conn == None:
        if conn:
            conn.close()

        return redirect('/error')

    return render_template('login.html')


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    if 'loggedId' not in session:
        return redirect('/login')

    today = datetime.date.today()
    current_teachers_count = 0
    retired_teachers_count = 0
    system_users_count = 0
    current_teachers = []

    conn = connector()
    query = "SELECT COUNT(*) FROM public.system_users"
    cur = conn.cursor()
    cur.execute(query)
    system_users_count = cur.fetchall()[0][0]

    query = "SELECT * FROM public.teachers WHERE status = 0"
    cur = conn.cursor()
    cur.execute(query)
    current_teachers = cur.fetchall()
    current_teachers_count = len(current_teachers)

    query = "SELECT COUNT(*) FROM public.teachers WHERE status = 1"
    cur = conn.cursor()
    cur.execute(query)
    retired_teachers_count = cur.fetchall()[0][0]

    if conn:
        conn.close()

    counts = [current_teachers_count,
              retired_teachers_count, system_users_count]

    return render_template('index.html', today=today, counts=counts, teachers=current_teachers)


# Route for deactivate teachers page
@app.route('/')
@app.route('/deactivated-teacher')
def deactivated_teacher():
    if 'loggedId' not in session:
        return redirect('/login')

    teachers = []

    conn = connector()
    query = "SELECT * FROM public.teachers WHERE status = 1"
    cur = conn.cursor()
    cur.execute(query)
    teachers = cur.fetchall()

    if conn:
        conn.close()

    return render_template('deactivated_teachers.html', teachers=teachers)


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

    id = request.args['id']
    conn = connector()
    query = "SELECT * FROM public.teachers WHERE id = %s"
    values = (int(id),)
    cur = conn.cursor()
    cur.execute(query, values)
    details = cur.fetchall()

    if conn:
        conn.close()

    if len(details) > 0:
        return render_template('view_teacher_details.html', details=details[0])

    else:
        return redirect('/index')


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

    if conn:
        conn.close()

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

    if conn:
        conn.close()

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

                if conn:
                    conn.close()

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

                if conn:
                    conn.close()

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
                row_count = 0

                query = ''' INSERT INTO public.system_users (first_name, last_name, username, user_type, password) VALUES (%s, %s, %s, %s, %s) '''
                values = (str(fname), str(lname), str(
                    uname), int(type), str(psw))
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                row_count = cur.rowcount

                if conn:
                    conn.close()

                if row_count > 0:
                    return jsonify({'success': "Account has been created! (ගිණුම නිර්මාණය කර ඇත!)"})

                else:
                    return jsonify({'error': "Account not created. Please try again! (ගිණුම සාදා නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('index')})


# Route for remove system user
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

                if conn:
                    conn.close()

                if row_count > 0:
                    return jsonify({'success': "System user has been removed! (පද්ධති පරිශීලකයා ඉවත් කර ඇත!)"})

                else:
                    return jsonify({'error': "System user not removed. Please try again! (පද්ධති පරිශීලකයා ඉවත් කර නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('index')})


# Route for add new teacher
@app.route('/add_new_teacher', methods=['GET', 'POST'])
def add_new_teacher():

    if request.method == "POST":

        if 'loggedId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:

            fullName = request.form.get('fullName')
            fullNameInitials = request.form.get('fullNameInitials')
            dob = request.form.get('dob')
            nic = request.form.get('nic')
            address = request.form.get('address')
            distance = request.form.get('distance')
            landNumber = request.form.get('landNumber')
            mobileNumber = request.form.get('mobileNumber')
            email = request.form.get('email')
            marriedPersonName = request.form.get('marriedPersonName')
            marriedPersonJob = request.form.get('marriedPersonJob')
            originalAppointment = request.form.get('originalAppointment')
            gradeClass = request.form.get('gradeClass')
            salaryImplementDate = request.form.get('salaryImplementDate')
            servicedSchools = request.form.get('servicedSchools')
            educationQualifications = request.form.get(
                'educationQualifications')

            if (len(fullName) == 0 or len(fullNameInitials) == 0 or len(dob) == 0 or len(nic) == 0 or
                    len(address) == 0 or len(distance) == 0 or len(educationQualifications) == 0):

                return jsonify({'error': "Fields are empty! (ආදාන ක්ෂේත්‍ර හිස්ය!)"})

            else:

                # Insert data
                conn = connector()
                row_count = 0

                query = ''' INSERT INTO public.teachers 
                    (full_name, full_name_initials, dob, nic, address, distance, tp_land, tp_mobile, email, married_person_name, 
                    married_person_job, original_appointment_date, grade_class, salary_implement_date, previous_serviced_schools, 
                    education_qualifications, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
                values = (str(fullName), str(fullNameInitials), str(dob), str(nic), str(address), str(distance), str(landNumber), str(mobileNumber), str(email), str(marriedPersonName),
                          str(marriedPersonJob), str(originalAppointment), str(gradeClass), str(salaryImplementDate), str(servicedSchools), str(educationQualifications), int(0))
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                row_count = cur.rowcount

                if conn:
                    conn.close()

                if row_count > 0:
                    return jsonify({'success': "Teacher details has been inserted! (ගුරු විස්තර ඇතුලත් කර ඇත!)"})

                else:
                    return jsonify({'error': "Teacher details not inserted. Please try again! (ගුරු විස්තර ඇතුලත් කර නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('index')})


# Route for update teacher
@app.route('/update_teacher', methods=['GET', 'POST'])
def update_teacher():

    if request.method == "POST":

        if 'loggedId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:

            id = request.form.get('id')
            fullName = request.form.get('fullName')
            fullNameInitials = request.form.get('fullNameInitials')
            dob = request.form.get('dob')
            nic = request.form.get('nic')
            address = request.form.get('address')
            distance = request.form.get('distance')
            landNumber = request.form.get('landNumber')
            mobileNumber = request.form.get('mobileNumber')
            email = request.form.get('email')
            marriedPersonName = request.form.get('marriedPersonName')
            marriedPersonJob = request.form.get('marriedPersonJob')
            originalAppointment = request.form.get('originalAppointment')
            gradeClass = request.form.get('gradeClass')
            salaryImplementDate = request.form.get('salaryImplementDate')
            servicedSchools = request.form.get('servicedSchools')
            educationQualifications = request.form.get(
                'educationQualifications')

            if (len(id) == 0 or len(fullName) == 0 or len(fullNameInitials) == 0 or len(dob) == 0 or len(nic) == 0 or
                    len(address) == 0 or len(distance) == 0 or len(educationQualifications) == 0):

                return jsonify({'error': "Fields are empty! (ආදාන ක්ෂේත්‍ර හිස්ය!)"})

            else:

                # Insert data
                conn = connector()
                row_count = 0

                query = ''' UPDATE public.teachers SET full_name = %s, full_name_initials = %s, dob = %s, nic = %s, address = %s, distance = %s, tp_land = %s, tp_mobile = %s, email = %s, married_person_name = %s, 
                    married_person_job = %s, original_appointment_date = %s, grade_class = %s, salary_implement_date = %s, previous_serviced_schools = %s, 
                    education_qualifications = %s WHERE id = %s '''
                values = (str(fullName), str(fullNameInitials), str(dob), str(nic), str(address), str(distance), str(landNumber), str(mobileNumber), str(email), str(marriedPersonName),
                          str(marriedPersonJob), str(originalAppointment), str(gradeClass), str(salaryImplementDate), str(servicedSchools), str(educationQualifications), int(id))
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                row_count = cur.rowcount

                if conn:
                    conn.close()

                if row_count > 0:
                    return jsonify({'success': "Teacher details has been updated! (ගුරු විස්තර යාවත්කාලීන කර ඇත!)"})

                else:
                    return jsonify({'error': "Teacher details not updated. Please try again! (ගුරු විස්තර යාවත්කාලීන කර නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('index')})


# Route for change teacher status
@app.route('/change_status', methods=['GET', 'POST'])
def change_status():

    if request.method == "POST":

        if 'loggedId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:

            id = request.form.get('id')
            status = request.form.get('status')

            if (len(id) == 0 or len(status) == 0):

                return jsonify({'error': "Fields are empty! (ආදාන ක්ෂේත්‍ර හිස්ය!)"})

            else:

                # Insert data
                conn = connector()
                row_count = 0

                query = ''' UPDATE public.teachers SET status = %s WHERE id = %s '''
                values = (int(status), int(id))
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                row_count = cur.rowcount

                if conn:
                    conn.close()

                if row_count > 0:
                    return jsonify({'success': "Teacher status has been updated! (ගුරුවරයාගේ තත්ත්වය යාවත්කාලීන කර ඇත!)"})

                else:
                    return jsonify({'error': "Teacher status not updated. Please try again! (ගුරුවරයාගේ තත්ත්වය යාවත්කාලීන කර නැත. කරුණාකර නැවත උත්සාහ කරන්න!)"})

    return jsonify({'redirect': url_for('index')})


# Main
if __name__ == '__main__':

    host = "127.0.0.1"
    port = "5001"
    url = "http://{0}:{1}".format(host, port)
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=port, threaded=True, debug=False)
    # app.run(host=host, port=port, threaded=True, debug=True)
