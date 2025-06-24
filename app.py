import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, session
from models.models import load_student_data
import numpy as np
import pandas as pd


app = Flask(__name__, template_folder='dashboard/template')
# Explicitly set secret_key with a fallback
app.secret_key = os.environ.get('SECRET_KEY', 'a_very_secure_key_2025')

# Load configuration (optional, for other settings)
app.config.from_object('config')

# Load student data at app startup
STUDENT_DATA = load_student_data()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        role_number = request.form.get('role_number', '').strip()
        student_name = request.form.get('student_name', '').strip()

        if not role_number or not student_name:
            error = 'Please enter both Role Number and Student Name.'
        else:
            df = STUDENT_DATA
            matched = df[(df['role_number'] == role_number) & (df['name'].str.lower() == student_name.lower())]
            if not matched.empty:
                session['role_number'] = role_number
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid role number or student name. Please try again.'

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    role_number = session.get('role_number')
    if not role_number:
        return redirect(url_for('login'))

    df = STUDENT_DATA
    student_rows = df[df['role_number'] == role_number]
    if student_rows.empty:
        return redirect(url_for('login'))

    student_row = student_rows.iloc[0]
    student_name = student_row['name']

    subject_columns = [col for col in df.columns if col not in ('role_number', 'name')]
    grades = {}
    for subject in subject_columns:
        grade_val = student_row[subject]
        if pd.isnull(grade_val):
            grade_val = 0
        else:
            try:
                grade_val = int(round(grade_val))
            except Exception:
                try:
                    grade_val = float(grade_val)
                except Exception:
                    grade_val = 0
        grades[subject] = grade_val

    average_grade = int(round(np.mean(list(grades.values())))) if grades else 0

    return render_template('dashboard.html', grades=grades, student_name=student_name, average_grade=average_grade)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)