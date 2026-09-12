import os
import numpy as np
import pandas as pd
import random

def generate_student_dataset(output_path="data/students_data.csv"):
    """Create and save the 160-student performance dataset for Ram Lal Anand School."""
    np.random.seed(42)
    random.seed(42)

    first_names = [
        "Aarav", "Diya", "Ishaan", "Ananya", "Rohan", "Meera", "Kabir", "Sneha", 
        "Aditya", "Pooja", "Vihaan", "Zara", "Arjun", "Myra", "Sai", "Fatima", 
        "Krishna", "Priya", "Rahul", "Riya"
    ]
    last_names = [
        "Sharma", "Patel", "Verma", "Iyer", "Gupta", "Nair", "Singh", "Kulkarni", 
        "Joshi", "Reddy", "Das", "Chaudhary", "Malhotra", "Bose", "Menon"
    ]

    # Generate 300 unique names
    all_names = [f"{f} {l}" for f in first_names for l in last_names]
    random.shuffle(all_names)
    students = all_names[:160]

    subjects = [
        "Mathematics",
        "Science",
        "Social Science",
        "General Knowledge",
        "Computer Science",
        "Economics",
    ]

    sections = ["10th A", "10th B", "10th C", "10th D"]
    
    records = []
    
    student_idx = 0
    for section in sections:
        for i in range(1, 41):
            name = students[student_idx]
            student_idx += 1
            
            section_code = section.replace("10th ", "")
            roll_no = f"10{section_code}{i:02d}"
            
            student_dict = {
                "Roll No": roll_no,
                "Student Name": name,
                "Section": section,
                "School Name": "Ram Lal Anand School"
            }

            grand_total = 0
            passed_all = True

            for sub in subjects:
                # Theory out of 80, Practical out of 20
                theory = int(np.random.randint(20, 79))
                practical = int(np.random.randint(5, 20))
                total = theory + practical

                student_dict[f"{sub} (Theory)"] = theory
                student_dict[f"{sub} (Practical)"] = practical
                student_dict[f"{sub} (Total)"] = total

                # 33% passing rule
                if total < 33:
                    passed_all = False

                grand_total += total

            student_dict["Grand Total (600)"] = grand_total
            student_dict["Percentage (%)"] = round((grand_total / 600.0) * 100.0, 2)
            student_dict["Status"] = "PASS" if passed_all else "FAIL"

            records.append(student_dict)

    df = pd.DataFrame(records)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset of 160 students successfully saved to {output_path}")
    return df

if __name__ == "__main__":
    generate_student_dataset()
