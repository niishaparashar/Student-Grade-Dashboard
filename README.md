# Student-Grade-Dashboard
Student Grade Dashboard
A simple Flask web application to manage and display student grades.
Description
This project provides a dashboard where students can log in with their roll number and name to view their grades and average score, loaded from an Excel file (students_grades.xlsx).
Screenshots
Login Page

Dashboard

UI Code
Login Page
The login interface features a centered form with a gradient background and purple accents.
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Grade Dashboard Login</title>
</head>
<body style="background: linear-gradient(135deg, #4B5EAA 0%, #8EA9E8 100%); min-height: 100vh; margin: 0; font-family: Arial, sans-serif;">
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-radius: 16px; padding: 32px; width: 100%; max-width: 400px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2); text-align: center;">
            <h1 style="color: #6B46C1; margin-bottom: 20px;">Student Grade Dashboard Login</h1>
            {% if error %}
                <p style="color: #ff4444; margin-bottom: 15px;">{{ error }}</p>
            {% endif %}
            <form method="POST" style="display: flex; flex-direction: column; gap: 16px;">
                <div>
                    <label for="role_number" style="display: block; color: #fff; margin-bottom: 5px;">Roll Number</label>
                    <input type="text" id="role_number" name="role_number" required style="padding: 8px; width: 100%; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;">
                </div>
                <div>
                    <label for="student_name" style="display: block; color: #fff; margin-bottom: 5px;">Student Name</label>
                    <input type="text" id="student_name" name="student_name" required style="padding: 8px; width: 100%; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; font-size: 14px;">
                </div>
                <button type="submit" style="padding: 10px 20px; background-color: #6B46C1; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px;">Login</button>
            </form>
        </div>
    </div>
</body>
</html>

Dashboard
The dashboard features a header with a logout button, two white cards for grades and charts, and a gradient background.
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Grade Dashboard - {{ student_name }}</title>
</head>
<body style="background: linear-gradient(135deg, #4B5EAA 0%, #8EA9E8 100%); min-height: 100vh; margin: 0; font-family: Arial, sans-serif; padding: 20px 0;">
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">
        <header style="display: flex; justify-content: flex-end; padding: 10px 0;">
            <form action="{{ url_for('logout') }}" method="POST" style="display: inline-block;">
                <button type="submit" style="padding: 10px 20px; background-color: #6B46C1; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px;">Logout</button>
            </form>
        </header>
        <main>
            <h1 style="color: #6B46C1; text-align: center; margin-bottom: 20px;">Grade Dashboard</h1>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                <div style="background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); padding: 20px;">
                    <h2 style="color: #6B46C1; margin-bottom: 16px;">Grades for {{ student_name }}</h2>
                    <ul style="list-style: none; padding: 0;">
                        {% for subject, grade in grades.items() %}
                            <li style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <span>{{ subject }}</span>
                                <span style="color: #6B46C1;">{{ grade }}%</span>
                            </li>
                        {% endfor %}
                    </ul>
                    <p style="margin-top: 10px;"><strong>Average Grade:</strong> <span style="color: #6B46C1;">{{ average_grade }}%</span></p>
                </div>
                <div style="background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); padding: 20px;">
                    <h2 style="color: #6B46C1; margin-bottom: 16px;">Grade Charts</h2>
                    <div id="pie-chart" style="height: 200px; width: 100%;"></div>
                    <div id="bar-chart" style="height: 200px; width: 100%; margin-top: 20px;"></div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>

Prerequisites

Python 3.x
Flask
pandas
numpy
openpyxl (for Excel support)

Installation

Clone the repository:git clone https://github.com/niishaparashar/Student-Grade-Dashboard.git


Navigate to the project directory:cd Student-Grade-Dashboard


Create a virtual environment and activate it:python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate


Install dependencies:pip install -r requirements.txt


Ensure students_grades.xlsx is in the project root.

Usage

Run the application:python dashb.py


Open your browser and go to http://127.0.0.1:5000.
Log in with a valid roll number and name from students_grades.xlsx.
View the dashboard or log out.

Contributing
Feel free to fork and submit pull requests. Issues and suggestions are welcome!
License
This project is open-source. No specific license is defined—consider adding one (e.g., MIT) if you plan to share widely.
Contact
For questions, reach out to niishaparashar.
