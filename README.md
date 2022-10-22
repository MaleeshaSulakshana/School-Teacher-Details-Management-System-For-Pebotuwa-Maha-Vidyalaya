# School-Teacher-Details-Management-System-For-Pebotuwa-Maha-Vidyalaya
School Teacher Details Management System For Pebotuwa Maha Vidyalaya (ර/පෑබොටුව මහා විද්‍යාලය)

# Requirements
* Install Python (https://www.python.org/downloads/)
* Install Postgresql (https://www.postgresql.org/download/)
* Install pip (https://pip.pypa.io/en/stable/installation/)
* Install pipenv (https://pipenv.pypa.io/en/latest/install/)

# Steps to run
* Create virtual environment<br/>
**python -m pipenv shell**<br/>

* Install required pip packages <br/>
**pip install flask**<br/>
**pip install psycopg2**<br/>
**pip install pyinstaller** - for generate .exe file

## Do you need to generate .exe file use below command
* pyinstaller -w -F -i "icon\logo.ico" --name "School Teachers Details Management System" --add-data "templates;templates" --add-data "static;static" app.py