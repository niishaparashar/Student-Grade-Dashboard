import pandas as pd

def load_student_data():
    try:
        df = pd.read_excel('students_grades.xlsx', dtype={'role_number': str, 'name': str})
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        print("Loaded columns:", df.columns)
        return df
    except Exception as e:
        print(f"Error loading student data: {e}")
        return pd.DataFrame()