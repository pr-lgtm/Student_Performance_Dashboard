<h1 align="center">📊 Class 10 Student Performance Dashboard</h1>

<p align="center">
  <b>An interactive, chatbot-style analytics portal for teachers to analyse Class 10 student results at Ram Lal Anand School.</b><br>
  Built with <b>Python</b> · <b>Streamlit</b> · <b>Pandas</b> · <b>NumPy</b> · <b>Matplotlib</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/streamlit-1.30%2B-FF4B4B?logo=streamlit" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</p>

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Evaluation & Grading Structure](#-evaluation--grading-structure)
- [Repository Structure](#-repository-structure)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Getting Started](#-getting-started)
- [How to Use](#-how-to-use)
- [Sample Queries](#-sample-queries)
- [Screenshots](#-screenshots)
- [Academic Context](#-academic-context)
- [License](#-license)

---

## 🎯 Project Overview

This Streamlit web application manages and evaluates academic performance records for **160 students in Class 10th** across **4 sections (10th A, 10th B, 10th C, and 10th D with 40 students each)** at **Ram Lal Anand School**. Teachers can type natural-language questions into a chatbot-style interface and receive:

- ✅ **Text answers** — topper names, pass/fail lists, averages, rank lists, section-level summaries, individual report cards.
- 📈 **Matplotlib charts** — line charts, bar charts, comparison charts, pie charts, and section-level comparative analysis graphs — all generated on-the-fly.
- 📥 **CSV Downloads** — export result reports and student performance datasets directly for offline reporting and administration.

> **No external AI APIs are used.** The chatbot is a keyword-driven query engine built entirely with Python string matching, Pandas, and NumPy.

---

## 📝 Evaluation & Grading Structure

| Component                 | Specification                                                             |
| :------------------------ | :------------------------------------------------------------------------ |
| **School**                | Ram Lal Anand School                                                      |
| **Number of Students**    | 160                                                                       |
| **Sections (4)**          | 10th A, 10th B, 10th C, 10th D (40 students each)                         |
| **Subjects (6)**          | Mathematics, Science, Social Science, General Knowledge, Computer Science, Economics |
| **Marking Ratio**         | **80 : 20** — 80 marks Theory + 20 marks Practical per subject           |
| **Total Marks per Subject** | 100                                                                     |
| **Grand Total**           | 600 (6 × 100)                                                            |
| **Passing Criteria**      | ≥ 33 marks (33%) in **each** individual subject                          |
| **Result**                | **PASS** if all 6 subjects ≥ 33; otherwise **FAIL**                      |

---

## 🗂 Repository Structure

```text
Student_Performance_Dashboard/
│
├── data/
│   ├── __init__.py              # Makes data/ a Python package
│   ├── generate_data.py         # Script to generate the 160-student dataset (4 sections)
│   └── students_data.csv        # Auto-generated CSV dataset
│
├── app.py                       # Main Streamlit application (UI + query engine)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── README.md                    # This documentation file
```

---

## 🛠 Tech Stack

| Library        | Purpose                                           |
| :------------- | :------------------------------------------------ |
| **Python 3.10+** | Core programming language                       |
| **Streamlit**  | Web interface, interactive widgets, session state, CSV download triggers |
| **Pandas**     | DataFrames, CSV I/O, aggregations, filtering, report generation |
| **NumPy**      | Numeric operations, random seed for reproducible data |
| **Matplotlib** | All visualisations (line, bar, pie, section comparative graphs) |

> ⚠️ As per project specifications, **only Matplotlib** is used for visualisation — no Plotly, Seaborn, or Altair.

---

## ✨ Features

### 💬 Natural-Language Query Engine
- Ask questions in plain English — no coding required.
- Recognises subject aliases (`maths`, `cs`, `gk`, `sst`, `eco`) and section filters (`10th A`, `Section B`, etc.).
- Returns formatted tables, bullet lists, or charts depending on the question.

### 📊 Visualisations (Matplotlib)
| Chart Type                 | What It Shows                                                    |
| :------------------------- | :--------------------------------------------------------------- |
| **Line Chart**             | Theory, Practical & Total marks across students                  |
| **Bar Chart**              | Grouped Theory vs Practical for any subject                      |
| **Comparison**             | All 6 subjects side-by-side for every student                    |
| **Totals Chart**           | Horizontal bar of Grand Totals (sorted)                         |
| **Pie Chart**              | Pass vs Fail ratio                                               |
| **Section Comparative**    | Comparative analysis across sections (10th A, 10th B, 10th C, 10th D) |

### 📋 Data & Analytics
- Full result sheet with sortable columns and section filtering.
- Key metrics panel (total students, pass count, highest total, class average).
- Subject-wise statistical summary (mean, median, max, min, std dev).
- Section-level comparative analysis (average marks, pass percentage, topper per section).
- Individual student report cards.
- Complete rank / merit list.

### 📥 CSV Download Capabilities
- Download complete result datasets as CSV files.
- Export filtered result reports, merit lists, and section summaries with a single click.
- Seamless integration with Streamlit download buttons for offline record-keeping.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10** or higher
- `pip` (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Student_Performance_Dashboard.git
cd Student_Performance_Dashboard

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

> 💡 The dataset (`data/students_data.csv`) is auto-generated on first run if the file is missing. You can also regenerate it manually:
> ```bash
> python -m data.generate_data
> ```

---

## 📖 How to Use

1. **Open the app** — Run `streamlit run app.py` and open the URL shown in your terminal.
2. **Go to the "💬 Ask a Question" tab** — This is the main chatbot interface.
3. **Type a question** in the text input box (or click a quick-query button in the sidebar).
4. **Read the answer** — The dashboard shows text results, tables, or charts depending on your question.
5. **Explore Section Comparisons** — View comparative analysis graphs across 10th A, 10th B, 10th C, and 10th D.
6. **Download Reports** — Export result reports and datasets using the CSV download buttons.
7. **Browse raw data** — Switch to the "📄 Full Dataset" tab to view the complete result sheet.
8. **Need help?** — Check the "❓ Help" tab for a full list of supported queries.

---

## 💡 Sample Queries

| What You Want to Know                  | Type This                              |
| :------------------------------------- | :------------------------------------- |
| Overall class topper                   | `Who is the topper?`                   |
| Subject-specific topper                | `Who scored highest in Science?`       |
| Section-level topper                   | `Who is the topper in Section A?`      |
| Section comparative analysis           | `Compare sections` or `Show section comparison` |
| Weakest student                        | `Who has the lowest marks?`            |
| Pass/Fail breakdown                    | `Who passed?` or `Show fail students`  |
| Merit / rank list                      | `Show rank list`                       |
| Class averages                         | `Show class average`                   |
| Statistical summary                    | `Show subject-wise analysis`           |
| Line chart for a subject               | `Show graph for Mathematics`           |
| Bar chart for a subject                | `Show bar chart for Economics`         |
| Compare all subjects                   | `Compare all subjects`                 |
| Grand total chart                      | `Show total marks chart`               |
| Pass/Fail pie chart                    | `Show pie chart of pass/fail`          |
| Individual student report              | `Tell me about Aarav Sharma`           |

---

## 🖼 Screenshots

<img width="1512" height="856" alt="image" src="https://github.com/user-attachments/assets/0e887ab6-38d0-47bf-8231-812354998fc2" />
<img width="1512" height="860" alt="image" src="https://github.com/user-attachments/assets/48cc948c-504b-4ab5-b540-36bd8dc69de9" />
<img width="1512" height="860" alt="image" src="https://github.com/user-attachments/assets/a4f5fcea-1953-4ae1-972c-7003587f9171" />




---

## 🎓 Academic Context

| Field                 | Detail                                                  |
| :-------------------- | :------------------------------------------------------ |
| **Institution**       | Ram Lal Anand School                                    |
| **Target Group**      | Class 10 (160 students across Sections A, B, C, D)      |
| **Program/Semester**  | Semester III                                            |
| **Course Type**       | Skill Enhancement Course (SEC)                          |
| **Paper Name**        | Analytics / Computing using Python                      |
| **Objective**         | Design, implement and deploy a Python application demonstrating data generation, Pandas/NumPy manipulation, natural-language query handling, section-level comparative analysis, CSV report export, and Matplotlib visualisation in a web interface. |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
