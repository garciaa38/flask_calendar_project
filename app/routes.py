from flask import (Blueprint, render_template)
import os
import sqlite3
from datetime import datetime
from app.forms.forms import AppointmentForm

bp = Blueprint('main', __name__, url_prefix='/')
DB_FILE = os.environ.get("DB_FILE")

@bp.before_request
def index():
    with sqlite3.connect(DB_FILE) as conn:
        print("DATABASE", conn)

@bp.route("/", method=["GET", "POST"])
def main():
    form = AppointmentForm()
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute('''
                        SELECT id, name, start_datetime, end_datetime
                        FROM appointments
                        ORDER BY start_datetime;
                        ''')
        results = curs.fetchall()
        print("DATABASE", results)
        print("CHECKING DATE AND TIME", type(results[0][2]))
        datetime_obj = datetime.strptime(results[0][2], '%Y-%m-%d %H:%M:%S')
        print("DATE TIME OBJ", datetime_obj)
        print("JUST TIME", datetime_obj.strftime('%H:%M'))
    return render_template('main.html', rows=results, datetime=datetime, form=form)