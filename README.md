# Student_Performance_Dashboard
# Class 10 Student Analytics Portal

An interactive web dashboard built with Streamlit, Pandas, NumPy, and Matplotlib to query and visualize Class 10 student academic performance.

---

## Features

- **Academic Dataset**: 10 student records across 6 subjects:
  - Mathematics, Science, Social Science, General Knowledge, Computer Science, Economics.
  - Evaluation structure: 80 marks Theory + 20 marks Practical (Total: 100 per subject, 600 aggregate).
  - Passing criterion: $\ge 33\%$ in each subject.
- **Natural Language Q&A**:
  - Overall class topper and subject toppers.
  - Pass/Fail student breakdown.
  - Class and subject performance averages.
  - Individual student lookups.
- **Visual Analytics**:
  - Dynamic line charts showing subject-level performance across students using Matplotlib.

---

## Project Structure

```text
student_analytics_app/
│
├── data/
│   ├── generate_data.py       # Script to generate student records
│   └── students_data.csv      # Output CSV dataset
│
├── app.py                     # Streamlit web application
├── requirements.txt           # Project dependencies
├── .gitignore                 # Files excluded from git
└── README.md                  # Project documentation
