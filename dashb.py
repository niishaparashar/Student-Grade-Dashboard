from flask import Flask, render_template_string, request, redirect, url_for, session
import pandas as pd
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management, 
#in production use environment variable

# Load students data from Excel on app start
def load_student_data():
    try:
        # Read Excel file with student grades
        df = pd.read_excel('students_grades.xlsx', dtype={'role_number': str, 'name': str})
        # Clean column names for consistency
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        print("Loaded columns:", df.columns)  # Debugging output
        return df
    except Exception as e:
        print(f"Error loading student data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

STUDENT_DATA = load_student_data()


LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Student Grade Dashboard - Login</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
    <style>
        /* Modern clean styling consistent with modern design standards */
       @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        * {
            margin: 0; padding: 0; box-sizing: border-box;
        }
        .vt323-title {
  font-family: 'VT323', monospace;
  font-size: 2.5rem;
}
        body {
            font-family: 'Inter', Copperplate;
            background: radial-gradient(circle, rgba(0, 0, 0, 1) 0%, 
            rgba(148, 187, 233, 1) 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            
            padding: 16px;
        }
        .login-container {
            background: rgba(255 255 255 / 0.1);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            padding: 48px 64px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        }
        h1 {
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 24px;
            text-align: center;
            text-shadow: 0 0 8px rgba(0,0,0,0.3);
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 1rem;
            color:#A9A9A9
        }
        input[type="text"] {
            width: 100%;
            padding: 12px 16px;
            border-radius: 12px;
            border: none;
            outline: none;
            font-size: 1rem;
            margin-bottom: 24px;
            color: #333;
        }
        button {
            width: 100%;
            padding: 14px;
            border-radius: 12px;
            border: none;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            background: linear-gradient(135deg, #8B5CF6, #6366F1);
            color: white;
            box-shadow: 0 10px 25px rgba(139,92,246,0.4);
            transition: background-color 0.3s ease;
        }
        button:hover {
            background: linear-gradient(135deg, #6366F1, #8B5CF6);
        }
        .error-msg {
            background: rgba(255 0 0 / 0.8);
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
        }
        @media (max-width: 480px) {
            .login-container {
                padding: 32px 24px;
            }
        }
    </style>
</head>
<body>
    <div class="login-container" role="main" aria-labelledby="loginTitle">
        <h1 id="loginTitle" style="font-family: 'VT323', monospace; font-size: 2.5rem; color: #8A2BE2">
  Student Grade Dashboard Login
</h1>
        {% if error %}
            <div role="alert" class="error-msg">{{ error }}</div>
        {% endif %}
        <form method="POST" action="{{ url_for('login') }}" aria-describedby="loginDesc">
            <label for="role_number">Roll Number</label>
            <input type="text" id="role_number" name="role_number" required autocomplete="off" placeholder="Enter Roll Number" />
            
            <label for="student_name">Student Name</label>
            <input type="text" id="student_name" name="student_name" required autocomplete="off" placeholder="Enter Student Name" />
            
            <button type="submit" aria-label="Login to Student Dashboard">Login</button>
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Student Grade Dashboard - {{ student_name }}</title>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    body {
      font-family: 'Inter', sans-serif;
      margin: 0;
      background: radial-gradient(circle, rgba(0, 0, 0, 1) 0%, 
            rgba(148, 187, 233, 1) 100%);
      color: #374151;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: white;
      padding: 24px 48px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .logo {
      font-weight: 700;
      font-size: 1.75rem;
      color: #6366F1;
      user-select: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .logo .material-icons {
      font-size: 2rem;
    }
    main {
      flex: 1;
      max-width: 1200px;
      margin: 40px auto;
      padding: 0 24px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 48px;
    }
    section {
      background: white;
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.05);
      padding: 32px 40px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    h2 {
      font-weight: 700;
      font-size: 1.5rem;
      color: #4B5563;
      user-select: none;
      border-bottom: 2px solid #6366F1;
      padding-bottom: 8px;
      max-width: max-content;
    }
    .grade-list {
      list-style: none;
      padding: 0;
      margin: 0;
      width: 100%;
    }
    .grade-list li {
      font-weight: 600;
      font-size: 1.1rem;
      padding: 8px 0;
      border-bottom: 1px solid #e5e7eb;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .grade-list li:last-child {
      border-bottom: none;
    }
    .grade-value {
      background: #E0E7FF;
      color: #4338CA;
      border-radius: 8px;
      padding: 4px 12px;
      font-weight: 700;
      min-width: 42px;
      text-align: center;
    }
    .average-grade {
      margin-top: 16px;
      font-size: 1.25rem;
      font-weight: 700;
      color: #2563EB;
      text-align: center;
      user-select: none;
    }
    canvas {
      max-width: 100%;
      height: auto !important;
    }
    .logout-btn {
      background: transparent;
      border: 2px solid #6366F1;
      color: #6366F1;
      font-weight: 600;
      font-size: 1rem;
      border-radius: 12px;
      padding: 10px 20px;
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .highlight-name {
    color: #8B5CF6;              
    font-weight: 900;
    text-shadow: 0 0 6px #C4B5FD;
     }     
    .logout-btn:hover {
      background: #6366F1;
      color: white;
      box-shadow: 0 10px 30px rgba(99,102,241,0.4);
    }
    @media (max-width: 900px) {
      main {
        grid-template-columns: 1fr;
        margin: 24px 16px;
        gap: 32px;
      }
      section {
        padding: 24px 28px;
      }
    }
  </style>
</head>
<body>
  <header role="banner">
    <div class="logo" aria-label="Student Grade Dashboard Logo">
      <span class="material-icons" aria-hidden="true">school</span> Grade Dashboard
    </div>
    <form method="POST" action="{{ url_for('logout') }}">
      <button type="submit" class="logout-btn" aria-label="Logout from Student Dashboard">
        <span class="material-icons" aria-hidden="true">logout</span> Logout
      </button>
    </form>
  </header>
  <main role="main" aria-labelledby="dashboardTitle">
    <h1 id="dashboardTitle" style="display:none;">Student Grade Dashboard for {{ student_name }}</h1>
    <section aria-label="Student Grades List">
      <h2>Grades for <span class="highlight-name">{{ student_name }}</span></h2>
      <ul class="grade-list" aria-live="polite">
        {% for subject, grade in grades.items() %}
          <li><span>{{ subject }}</span><span class="grade-value" aria-label="{{ subject }} grade">{{ grade }}%</span></li>
        {% endfor %}
      </ul>
      <div class="average-grade" aria-label="Average grade for student">
        Average Grade: {{ average_grade }}%
      </div>
    </section>
    <section aria-label="Charts showing student grades">
      <h2>Grade Charts</h2>
      <canvas id="pieChart" role="img" aria-label="Pie chart representing grades distribution"></canvas>
      <canvas id="barChart" role="img" aria-label="Bar chart representing grades per subject" style="margin-top:32px;"></canvas>
    </section>
  </main>
  <script>
    const grades = {{ grades | tojson }};
    const subjects = Object.keys(grades);
    const scores = Object.values(grades);

    // Pie Chart - Grade Distribution
    const ctxPie = document.getElementById('pieChart').getContext('2d');
    const pieChart = new Chart(ctxPie, {
      type: 'pie',
      data: {
        labels: subjects,
        datasets: [{
          label: 'Grades',
          data: scores,
          backgroundColor: [
            '#6366F1',
            '#8B5CF6',
            '#A78BFA',
            '#C4B5FD',
            '#DDD6FE'
          ],
          borderColor: '#F9FAFB',
          borderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {color: '#374151', font: {weight: '600'}}
          },
          tooltip: {
            callbacks: {
              label: context => context.label + ': ' + context.parsed + '%'
            }
          }
        }
      }
    });

    // Bar Chart - Grades per Subject
    const ctxBar = document.getElementById('barChart').getContext('2d');
    const barChart = new Chart(ctxBar, {
      type: 'bar',
      data: {
        labels: subjects,
        datasets: [{
          label: 'Grades (%)',
          data: scores,
          backgroundColor: '#6366F1',
          borderRadius: 8,
          barPercentage: 0.6
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {color: '#4B5563'},
            grid: {color: '#E5E7EB'}
          },
          x: {ticks: {color: '#4B5563'}, grid: {display: false}}
        },
        plugins: {
          legend: {display: false},
          tooltip: {
            callbacks: {
              label: context => context.parsed.y + '%'
            }
          }
        }
      }
    });
  </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        role_number = request.form.get('role_number', '').strip()
        student_name = request.form.get('student_name', '').strip()

        if not role_number or not student_name:
            error = 'Please enter both Role Number and Student Name.'
        else:
            # Use pandas DataFrame to validate
            global STUDENT_DATA
            df = STUDENT_DATA
            # Look for role_number and match name case-insensitive
            print("Available columns:", df.columns)
            matched = df[(df['role_number'] == role_number) & (df['name'].str.lower() == student_name.lower())]
            if not matched.empty:
                session['role_number'] = role_number
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid role number or student name. Please try again.'

    return render_template_string(LOGIN_HTML, error=error)


@app.route('/dashboard')
def dashboard():
    role_number = session.get('role_number')
    if not role_number:
        return redirect(url_for('login'))

    global STUDENT_DATA
    df = STUDENT_DATA

    # Get student row by role_number
    student_rows = df[df['role_number'] == role_number]
    if student_rows.empty:
        return redirect(url_for('login'))

    student_row = student_rows.iloc[0]
    student_name = student_row['name']

    # Subjects expected columns (excluding role_number and name)
    subject_columns = [col for col in df.columns if col not in ('role_number', 'name')]

    # Get grades dictionary
    grades = {}
    for subject in subject_columns:
        grade_val = student_row[subject]
        # Convert to int or float and round to int if possible
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

    # Compute average grade (round to integer)
    average_grade = int(round(np.mean(list(grades.values())))) if grades else 0

    return render_template_string(DASHBOARD_HTML, grades=grades, student_name=student_name, average_grade=average_grade)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

