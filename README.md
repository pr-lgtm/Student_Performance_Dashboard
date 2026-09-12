# Student_Performance_Dashboard
---
# Class 10 Student Academic Analytics Portal

An interactive web-based data analytics and query dashboard developed using **Python**, **Streamlit**, **Pandas**, **NumPy**, and **Matplotlib**.

---

## Academic Project Context

- **Institution:** Ram Lal Anand College, University of Delhi  
- **Program/Semester:** Semester III  
- **Course Type:** Skill Enhancement Course (SEC)  
- **Paper Name:** Analytics / Computing using Python  
- **Objective:** Design, implement, and deploy an end-to-end Python application that demonstrates data generation, structured dataset manipulation with Pandas and NumPy, natural language query handling, and data visualization using Matplotlib in a local web interface.

---

## Project Overview

This application manages and evaluates academic performance records for 10 imaginary students in Class 10th. The portal provides:
1. **Academic Records Table:** A tabular overview of theory, practical, aggregate scores, percentages, and pass/fail statuses.
2. **Interactive Natural Language Q&A:** A query interface where users can ask questions about student standings, toppers, averages, and pass/fail statistics.
3. **Visual Analytics:** Line charts generated strictly using Matplotlib to show marks distribution across students for any given subject.

---

## Evaluation & Grading Structure

The dataset models a standard secondary school assessment framework:

| Component | Specification |
| :--- | :--- |
| **Number of Students** | 10 students |
| **Subjects (6)** | Mathematics, Science, Social Science, General Knowledge, Computer Science, Economics |
| **Marking Ratio** | **80 : 20** (80 Marks Theory + 20 Marks Practical) |
| **Total Marks per Subject**| 100 Marks |
| **Grand Total** | 600 Marks (6 subjects × 100) |
| **Passing Criteria** | Minimum **33%** in each individual subject (Total score $\ge 33$) |
| **Result Determination** | **PASS** if all 6 subjects $\ge 33$; otherwise **FAIL** |

---

## Tech Stack & Constraints

- **Python 3.10+**
- **Streamlit:** Web interface, interactive state, and widgets.
- **Pandas:** Data structuring, transformations, aggregations, and CSV exports.
- **NumPy:** Numeric operations and deterministic data synthesis.
- **Matplotlib:** Data visualizations (line charts and trend analysis).
  
*(Note: As per course specifications, visualization is restricted strictly to Matplotlib without external high-level charting wrappers like Plotly or Seaborn).*

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

## Repository Structure

```text
student_analytics_app/
│
├── data/
│   ├── generate_data.py       # Script to generate the 10-student dataset
│   └── students_data.csv      # Generated CSV dataset
│
├── app.py                     # Main Streamlit web application
├── requirements.txt           # Project dependencies
├── .gitignore                 # Files excluded from git tracking
└── README.md                  # Complete project documentation
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
