
# 📊 Student Grade Dashboard

A web-based dashboard built with Flask and Python that allows students to securely view their subject-wise grades, overall performance, and visual charts — all pulled from a simple Excel file.

---

## 🚀 Features

- 🔐 Login using Roll Number & Student Name
- 📑 Pulls data directly from an Excel sheet (no database needed)
- 📊 Visualizes grades using Pie and Bar charts (Chart.js)
- 📉 Calculates average percentage dynamically
- 💻 Clean, responsive UI with modern design

---

## 🛠️ Tech Stack

- Python 🐍
- Flask 🌐
- Pandas 🧮
- NumPy
- HTML / CSS
- Chart.js 📊

---

## 📂 Project Structure

```
niishaparashar-student-grade-dashboard/
├── dashb.py                  # Main Flask app
├── requirements.txt        # Project dependencies
├── students_grades.xlsx    # Excel file with student data
└── README.md
```

---

## 🧪 How It Works

1. Student enters Roll Number & Name on login page  
2. App checks the Excel file using Pandas  
3. If credentials match:
   - Displays all subject-wise grades
   - Shows interactive pie & bar charts
   - Calculates and displays the average percentage  
4. User can log out securely

---

## 📝 How to Run Locally

1. Clone the repo:
```bash
git clone https://github.com/niishaparashar/student-grade-dashboard.git
cd student-grade-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

---

## 📊 Excel Format Required

Your Excel file should have the following columns:

| role_number | name         | Math | Science | English | History | Art |
|-------------|--------------|------|---------|---------|---------|-----|
| 101         | Vihaan Bansal| 88   | 92      | 79      | 85      | 91  |

---

## 📌 Future Improvements

- Add admin login to upload new Excel sheets
- Allow students to download report cards
- Integrate with a database (optional)
- Add mobile responsiveness and dark mode

---

## 🤝 Credits

Created by [Nisha Parashar](https://github.com/niishaparashar)  
Charts powered by [Chart.js](https://www.chartjs.org/)

---


