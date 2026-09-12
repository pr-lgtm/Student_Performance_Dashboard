"""
app.py
======
Class 10 Student Performance Dashboard - Streamlit Application

An interactive chatbot-style analytics portal for teachers to query
student results using natural language. Built with Pandas, NumPy,
and Matplotlib only.
"""

import os
import re
import io
import base64

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATA_FILE = os.path.join("data", "students_data.csv")

SUBJECTS = [
    "Mathematics",
    "Science",
    "Social Science",
    "General Knowledge",
    "Computer Science",
    "Economics",
]

# Aliases for flexible query matching
SUBJECT_ALIASES = {
    "math": "Mathematics",
    "maths": "Mathematics",
    "mathematics": "Mathematics",
    "science": "Science",
    "social science": "Social Science",
    "social": "Social Science",
    "sst": "Social Science",
    "general knowledge": "General Knowledge",
    "gk": "General Knowledge",
    "computer science": "Computer Science",
    "cs": "Computer Science",
    "computer": "Computer Science",
    "economics": "Economics",
    "eco": "Economics",
}

SAMPLE_QUERIES = [
    "Who is the topper of section A?",
    "Show graph for section B mathematics",
    "Compare sections",
    "Who failed in section C?",
    "Show class average",
    "Compare all subjects",
    "Show rank list",
    "Who scored highest in Economics?",
    "Show result summary",
    "Tell me about Aarav Sharma",
]

# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Load CSV dataset; auto-generate if missing or if row count < 160."""
    def generate():
        from data.generate_data import generate_student_dataset
        return generate_student_dataset(DATA_FILE)

    if not os.path.exists(DATA_FILE):
        return generate()
        
    df = pd.read_csv(DATA_FILE)
    if len(df) < 160:
        return generate()
    return df


# ---------------------------------------------------------------------------
# Plotting Helpers  (Matplotlib only)
# ---------------------------------------------------------------------------
def _style_ax(ax, title, xlabel, ylabel):
    """Apply consistent styling to a Matplotlib Axes."""
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.4)


def plot_line_chart(df, subject, section=None):
    """Line chart: Theory, Practical & Total for a subject."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    names = df["Student Name"].tolist()

    ax.plot(x, df[f"{subject} (Total)"], marker="o", lw=2,
            color="#1f77b4", label="Total (Max 100)")
    ax.plot(x, df[f"{subject} (Theory)"], marker="s", ls="--",
            alpha=0.7, color="#ff7f0e", label="Theory (Max 80)")
    ax.plot(x, df[f"{subject} (Practical)"], marker="^", ls=":",
            alpha=0.7, color="#2ca02c", label="Practical (Max 20)")
    ax.axhline(y=33, color="red", ls="-.", lw=1, alpha=0.8,
               label="Pass Line (33)")

    if len(x) <= 40:
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=90, ha="right", fontsize=8)
    else:
        ax.set_xticks([])

    ax.set_ylim(0, 105)
    title = f"Performance in {subject}" + (f" (Section {section})" if section else "")
    _style_ax(ax, title, "Students", "Marks")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    return fig


def plot_bar_chart(df, subject, section=None):
    """Grouped bar chart: Theory vs Practical for a subject."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    width = 0.35
    names = df["Student Name"].tolist()

    ax.bar(x - width / 2, df[f"{subject} (Theory)"], width,
           label="Theory (Max 80)", color="#4c72b0")
    ax.bar(x + width / 2, df[f"{subject} (Practical)"], width,
           label="Practical (Max 20)", color="#55a868")
    ax.axhline(y=33, color="red", ls="-.", lw=1, alpha=0.8,
               label="Pass Line (33)")

    if len(x) <= 40:
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=90, ha="right", fontsize=8)
    else:
        ax.set_xticks([])
        
    title = f"Theory vs Practical in {subject}" + (f" (Section {section})" if section else "")
    _style_ax(ax, title, "Students", "Marks")
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


def plot_comparison(df, section=None):
    """Bar chart comparing total marks of all subjects side by side."""
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(df))
    n = len(SUBJECTS)
    width = 0.12
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    for i, sub in enumerate(SUBJECTS):
        offset = (i - n / 2) * width + width / 2
        ax.bar(x + offset, df[f"{sub} (Total)"], width,
               label=sub, color=colors[i])

    if len(x) <= 40:
        ax.set_xticks(x)
        ax.set_xticklabels(df["Student Name"].tolist(), rotation=90,
                           ha="right", fontsize=8)
    else:
        ax.set_xticks([])

    title = "Subject-wise Comparison" + (f" (Section {section})" if section else " (All Students)")
    _style_ax(ax, title, "Students", "Total Marks")
    ax.legend(fontsize=8, ncol=3)
    fig.tight_layout()
    return fig


def plot_total_marks(df, section=None):
    """Horizontal bar chart of grand totals."""
    sorted_df = df.sort_values("Grand Total (600)", ascending=True)
    fig, ax = plt.subplots(figsize=(10, max(5, len(df)*0.1)))
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(sorted_df)))
    ax.barh(sorted_df["Student Name"], sorted_df["Grand Total (600)"],
            color=colors)
    
    if len(df) <= 40:
        for i, (val, name) in enumerate(
                zip(sorted_df["Grand Total (600)"], sorted_df["Student Name"])):
            ax.text(val + 3, i, str(val), va="center", fontsize=8)
    
    title = "Grand Total Marks (out of 600)" + (f" (Section {section})" if section else "")
    _style_ax(ax, title, "Marks", "")
    if len(df) > 40:
        ax.set_yticks([])
    fig.tight_layout()
    return fig


def plot_pie_pass_fail(df, section=None):
    """Pie chart of pass vs fail ratio."""
    counts = df["Status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%",
           colors=["#2ca02c", "#d62728"][:len(counts)],
           startangle=90, textprops={"fontsize": 12})
    title = "Pass / Fail Distribution" + (f" (Section {section})" if section else "")
    ax.set_title(title, fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig

def plot_section_comparison(df):
    """Compare average marks and pass percentages across sections."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    sec_avg = df.groupby("Section")["Grand Total (600)"].mean().reset_index()
    axes[0].bar(sec_avg["Section"], sec_avg["Grand Total (600)"], color="#1f77b4")
    axes[0].set_title("Average Grand Total by Section", fontsize=14, fontweight="bold", pad=12)
    axes[0].set_xlabel("Section", fontsize=11)
    axes[0].set_ylabel("Avg Marks", fontsize=11)
    for i, val in enumerate(sec_avg["Grand Total (600)"]):
        axes[0].text(i, val + 2, f"{val:.1f}", ha="center", fontsize=10)

    pass_pct = df.groupby("Section").apply(lambda x: (x["Status"] == "PASS").mean() * 100).reset_index(name="Pass %")
    axes[1].bar(pass_pct["Section"], pass_pct["Pass %"], color="#2ca02c")
    axes[1].set_title("Pass Percentage by Section", fontsize=14, fontweight="bold", pad=12)
    axes[1].set_xlabel("Section", fontsize=11)
    axes[1].set_ylabel("Pass %", fontsize=11)
    for i, val in enumerate(pass_pct["Pass %"]):
        axes[1].text(i, val + 1, f"{val:.1f}%", ha="center", fontsize=10)

    fig.tight_layout()
    return fig

# ---------------------------------------------------------------------------
# Query Matchers
# ---------------------------------------------------------------------------
def _match_subject(text):
    """Return the matched subject name from query text, or None."""
    text = text.lower()
    for alias in sorted(SUBJECT_ALIASES, key=len, reverse=True):
        if alias in text:
            return SUBJECT_ALIASES[alias]
    return None

def _match_section(text):
    """Return the matched section from query text, or None."""
    match = re.search(r"section\s+([a-z])", text.lower())
    if match:
        return f"10th {match.group(1).upper()}"
    return None


# ---------------------------------------------------------------------------
# Query Engine
# ---------------------------------------------------------------------------
def answer_query(query, full_df):
    """
    Parse a natural-language query and return (msg, fig_or_none, df_to_download, csv_filename).
    """
    q = query.lower().strip()
    
    # Filter by section if specified in the query
    section = _match_section(q)
    df = full_df[full_df["Section"] == section] if section else full_df.copy()
    sec_text = f" in Section {section}" if section else ""

    # ---- Section Comparison request ----
    if any(w in q for w in ["compare section", "section comparison"]):
        fig = plot_section_comparison(full_df)
        return "Here is the **section-wise comparison** chart:", fig, None, None

    # ---- Chart / Graph requests ----
    want_bar = any(w in q for w in ["bar chart", "bar graph", "bar "])
    want_line = any(w in q for w in ["line chart", "line graph", "line "])
    want_graph = any(w in q for w in ["graph", "chart", "plot", "show marks", "visuali"])
    want_compare = any(w in q for w in ["compare", "comparison", "all subject", "every subject"])
    want_total_chart = any(w in q for w in ["total marks chart", "grand total chart", "total chart", "overall chart"])
    want_pie = any(w in q for w in ["pie chart", "pie graph", "pass fail chart", "pass.*fail.*chart"])

    if want_compare and not any(w in q for w in ["section"]):
        fig = plot_comparison(df, section)
        return f"Here is the **subject-wise comparison** chart{sec_text}:", fig, None, None

    if want_total_chart:
        fig = plot_total_marks(df, section)
        return f"Here is the **grand total marks** chart{sec_text}:", fig, None, None

    if want_pie:
        fig = plot_pie_pass_fail(df, section)
        return f"Here is the **Pass / Fail distribution** pie chart{sec_text}:", fig, None, None

    if want_graph or want_bar or want_line:
        subject = _match_subject(q) or "Mathematics"
        if want_bar:
            fig = plot_bar_chart(df, subject, section)
            return f"Here is the **bar chart** for **{subject}**{sec_text}:", fig, None, None
        else:
            fig = plot_line_chart(df, subject, section)
            return f"Here is the **line chart** for **{subject}**{sec_text}:", fig, None, None

    # ---- Topper queries ----
    if any(w in q for w in ["topper", "highest", "rank 1", "first rank", "best student", "top scorer"]):
        subject = _match_subject(q)
        if subject:
            col = f"{subject} (Total)"
            top = df.loc[df[col].idxmax()]
            msg = (f"**Subject Topper — {subject}{sec_text}**\n\n"
                   f"| Field | Value |\n|---|---|\n"
                   f"| Name | {top['Student Name']} |\n"
                   f"| Section | {top.get('Section', 'N/A')} |\n"
                   f"| Roll No | {top['Roll No']} |\n"
                   f"| Total | {top[col]} / 100 |\n"
                   f"| Theory | {top[f'{subject} (Theory)']} / 80 |\n"
                   f"| Practical | {top[f'{subject} (Practical)']} / 20 |")
            return msg, None, pd.DataFrame([top]), "topper_subject.csv"
        else:
            top = df.loc[df["Grand Total (600)"].idxmax()]
            msg = (f"**Overall Class 10 Topper{sec_text}**\n\n"
                   f"| Field | Value |\n|---|---|\n"
                   f"| Name | {top['Student Name']} |\n"
                   f"| Section | {top.get('Section', 'N/A')} |\n"
                   f"| Roll No | {top['Roll No']} |\n"
                   f"| Grand Total | {top['Grand Total (600)']} / 600 |\n"
                   f"| Percentage | {top['Percentage (%)']}% |\n"
                   f"| Status | {top['Status']} |")
            return msg, None, pd.DataFrame([top]), "topper_overall.csv"

    # ---- Lowest / weakest ----
    if any(w in q for w in ["lowest", "weakest", "least", "bottom", "worst", "last rank"]):
        subject = _match_subject(q)
        if subject:
            col = f"{subject} (Total)"
            low = df.loc[df[col].idxmin()]
            msg = (f"**Lowest Scorer — {subject}{sec_text}**\n\n"
                   f"| Field | Value |\n|---|---|\n"
                   f"| Name | {low['Student Name']} |\n"
                   f"| Section | {low.get('Section', 'N/A')} |\n"
                   f"| Marks | {low[col]} / 100 |")
            return msg, None, pd.DataFrame([low]), "lowest_subject.csv"
        else:
            low = df.loc[df["Grand Total (600)"].idxmin()]
            msg = (f"**Lowest Overall Scorer{sec_text}**\n\n"
                   f"| Field | Value |\n|---|---|\n"
                   f"| Name | {low['Student Name']} |\n"
                   f"| Section | {low.get('Section', 'N/A')} |\n"
                   f"| Grand Total | {low['Grand Total (600)']} / 600 |\n"
                   f"| Percentage | {low['Percentage (%)']}% |")
            return msg, None, pd.DataFrame([low]), "lowest_overall.csv"

    # ---- Rank list ----
    if any(w in q for w in ["rank", "ranking", "merit", "position", "leaderboard", "rank list"]):
        ranked = df.sort_values("Grand Total (600)", ascending=False).reset_index(drop=True)
        ranked.index += 1
        ranked.index.name = "Rank"
        cols = ["Student Name", "Section", "Grand Total (600)", "Percentage (%)", "Status"]
        # In case 'Section' is missing due to some mismatch
        if "Section" not in ranked.columns:
            cols.remove("Section")
            
        table = ranked[cols].to_markdown()
        filename = f"rank_list{'_sec_'+section if section else ''}.csv"
        return f"**Rank List{sec_text}**\n\n{table}", None, ranked, filename

    # ---- Pass / Fail ----
    if any(w in q for w in ["pass", "fail", "result"]):
        passed_df = df[df["Status"] == "PASS"]
        failed_df = df[df["Status"] == "FAIL"]
        
        passed = passed_df["Student Name"].tolist()
        failed = failed_df["Student Name"].tolist()
        
        msg = (f"**Result Summary{sec_text} (Pass threshold: 33% per subject)**\n\n"
               f"- **Passed ({len(passed)}/{len(df)}):** "
               f"{', '.join(passed) if passed else 'None'}\n"
               f"- **Failed ({len(failed)}/{len(df)}):** "
               f"{', '.join(failed) if failed else 'None'}")
        
        fig = plot_pie_pass_fail(df, section)
        
        # Determine what to download
        dl_df = passed_df if "pass" in q and "fail" not in q else (failed_df if "fail" in q and "pass" not in q else df)
        dl_name = f"results{'_sec_'+section if section else ''}.csv"
        
        return msg, fig, dl_df, dl_name

    # ---- Average / Mean ----
    if any(w in q for w in ["average", "mean", "class average"]):
        avg_total = df["Grand Total (600)"].mean()
        avg_pct = df["Percentage (%)"].mean()
        lines = [f"**Averages{sec_text}**\n",
                 f"| Metric | Value |",
                 f"|---|---|",
                 f"| Grand Total | {avg_total:.2f} / 600 |",
                 f"| Percentage | {avg_pct:.2f}% |\n",
                 f"**Subject-wise Averages (out of 100)**\n",
                 f"| Subject | Average |\n|---|---|"]
        
        stats_data = [{"Metric": "Grand Total", "Value": avg_total}, {"Metric": "Percentage", "Value": avg_pct}]
        
        for sub in SUBJECTS:
            sub_avg = df[f"{sub} (Total)"].mean()
            lines.append(f"| {sub} | {sub_avg:.2f} |")
            stats_data.append({"Metric": f"{sub} Average", "Value": sub_avg})
            
        dl_df = pd.DataFrame(stats_data)
        
        return "\n".join(lines), None, dl_df, f"averages{'_sec_'+section if section else ''}.csv"

    # ---- Subject-wise analysis (median, max, min) ----
    if any(w in q for w in ["analysis", "summary", "statistics", "stats", "overview"]):
        lines = [f"**Statistical Summary{sec_text}**\n",
                 "| Subject | Mean | Median | Max | Min | Std Dev |",
                 "|---|---|---|---|---|---|"]
        
        stats_list = []
        for sub in SUBJECTS:
            col = f"{sub} (Total)"
            mean, med, mmax, mmin, std = df[col].mean(), df[col].median(), df[col].max(), df[col].min(), df[col].std()
            lines.append(f"| {sub} | {mean:.1f} | {med:.1f} | {mmax} | {mmin} | {std:.1f} |")
            stats_list.append({"Subject": sub, "Mean": mean, "Median": med, "Max": mmax, "Min": mmin, "Std": std})
            
        gt = df["Grand Total (600)"]
        mean, med, mmax, mmin, std = gt.mean(), gt.median(), gt.max(), gt.min(), gt.std()
        lines.append(f"\n| **Grand Total** | {mean:.1f} | {med:.1f} | {mmax} | {mmin} | {std:.1f} |")
        stats_list.append({"Subject": "Grand Total", "Mean": mean, "Median": med, "Max": mmax, "Min": mmin, "Std": std})
        
        dl_df = pd.DataFrame(stats_list)
        return "\n".join(lines), None, dl_df, f"statistics{'_sec_'+section if section else ''}.csv"

    # ---- Individual student lookup ----
    for name in df["Student Name"]:
        if name.lower() in q:
            row = df[df["Student Name"] == name].iloc[0]
            lines = [f"**Student Report Card: {row['Student Name']}** "
                     f"(Roll No: {row['Roll No']}, Section: {row.get('Section', 'N/A')})\n",
                     f"| Subject | Theory (/80) | Practical (/20) | Total (/100) |",
                     f"|---|---|---|---|"]
            for sub in SUBJECTS:
                lines.append(f"| {sub} | {row[f'{sub} (Theory)']} | {row[f'{sub} (Practical)']} | {row[f'{sub} (Total)']} |")
            lines.append(f"\n| **Grand Total** | | | **{row['Grand Total (600)']} / 600** |")
            lines.append(f"\n- **Percentage:** {row['Percentage (%)']}%")
            lines.append(f"- **Status:** {row['Status']}")
            return "\n".join(lines), None, pd.DataFrame([row]), f"{name.replace(' ', '_')}_report.csv"

    # ---- Fallback: help ----
    help_lines = [
        "I'm sorry, I couldn't understand that query. Here are some things you can ask:\n",
        "**General Queries:**",
        "- *Who is the topper of section A?*",
        "- *Who scored highest in Science?*",
        "- *Who has the lowest marks in section B?*",
        "- *Show pass and fail students*",
        "- *Show the rank list for section C*",
        "- *What is the class average?*",
        "- *Show subject-wise analysis*\n",
        "**Graph & Chart Queries:**",
        "- *Show graph for section B Mathematics*",
        "- *Compare sections*",
        "- *Show bar chart for Economics*",
        "- *Compare all subjects*",
        "- *Show total marks chart*",
        "- *Show pie chart of pass/fail*\n",
        "**Student Lookup:**",
        "- *Tell me about Aarav Sharma*",
        "- *Diya Patel*",
    ]
    return "\n".join(help_lines), None, None, None


def get_csv_download_link(df, filename="data.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    return csv


# ===========================================================================
# Streamlit UI
# ===========================================================================
st.set_page_config(
    page_title="Class 10 Student Analytics",
    page_icon="📊",
    layout="wide",
)

# ---- Background Image ----
try:
    bg_path = "/home/codespace/.gemini/antigravity/brain/3f404156-ef0c-429d-8d1f-37c424075eb0/.user_uploaded/media_1789231795953.png"
    with open(bg_path, "rb") as f:
        data = f.read()
    b64_str = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        }}
        /* Main Container Glassmorphism & Font Visibility */
        .block-container {{
            background-color: rgba(0, 0, 0, 0.65) !important;
            border-radius: 20px !important;
            padding: 2.5rem !important;
            margin-top: 3rem !important;
            margin-bottom: 3rem !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        /* Global Text Enhancements */
        h1, h2, h3, h4, h5, h6, p, span, label, div {{
            text-shadow: 0px 2px 4px rgba(0,0,0,0.8) !important;
            color: #ffffff !important;
        }}
        /* Table / DataFrame Tweaks */
        table {{
            background-color: rgba(255, 255, 255, 0.1) !important;
        }}
        th, td {{
            color: #ffffff !important;
            text-shadow: none !important;
        }}
        /* Button Enhancements */
        .stButton>button {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: #ffffff !important;
            backdrop-filter: blur(5px) !important;
            border-radius: 8px !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        }}
        .stButton>button:hover {{
            background-color: rgba(255, 255, 255, 0.4) !important;
            border-color: rgba(255, 255, 255, 0.5) !important;
        }}
        /* TextInput Tweaks */
        .stTextInput input {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            color: #000000 !important;
            text-shadow: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except Exception:
    pass

# ---- Header ----
st.markdown(
    "<h1 style='text-align:center;'>📊 Class 10 Student Performance Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#e0e0e0;'>"
    "Marking: 80 Theory + 20 Practical = 100 per subject &nbsp;|&nbsp; "
    "Total: 600 &nbsp;|&nbsp; Pass: ≥ 33% per subject</p>",
    unsafe_allow_html=True,
)
st.divider()

df = load_data()

# ---- Sidebar ----
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown(
        "This dashboard lets teachers interactively analyse "
        "Class 10 results by typing natural-language questions."
    )
    st.divider()
    st.subheader("📋 Quick Queries")
    st.markdown("Click any button below to auto-fill and run the query.")
    
    if "selected_query" not in st.session_state:
        st.session_state.selected_query = ""
    if "trigger_query" not in st.session_state:
        st.session_state.trigger_query = False

    for sq in SAMPLE_QUERIES:
        if st.button(sq, use_container_width=True):
            st.session_state.selected_query = sq
            st.session_state.trigger_query = True

# ---- Tabs ----
tab_chat, tab_data, tab_help = st.tabs(
    ["💬 Ask a Question", "📄 Full Dataset", "❓ Help"]
)

with tab_chat:
    st.subheader("Ask anything about the student results")

    user_query = st.text_input(
        "Type your question (or click a quick query from the sidebar):",
        value=st.session_state.get("selected_query", ""),
        placeholder="e.g. Who is the topper of section A? / Compare sections",
    )
    
    # Determine the query to run
    active_query = user_query
    if st.session_state.get("trigger_query"):
        active_query = st.session_state.selected_query
        st.session_state.trigger_query = False

    if active_query:
        st.markdown("---")
        with st.spinner("Analysing..."):
            msg, fig, dl_df, dl_name = answer_query(active_query, df)
        st.markdown(msg)
        if fig is not None:
            st.pyplot(fig)
        if dl_df is not None:
            st.download_button(
                label="📥 Download Result Data as CSV",
                data=get_csv_download_link(dl_df),
                file_name=dl_name,
                mime="text/csv"
            )

with tab_data:
    st.subheader("📄 Complete Class 10 Result Sheet")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.download_button(
        label="📥 Download Full Dataset (CSV)",
        data=get_csv_download_link(df),
        file_name="students_full_data.csv",
        mime="text/csv"
    )

    st.markdown("### Key Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", len(df))
    
    # Sections count
    sections = df.get("Section", pd.Series(dtype=str)).nunique()
    c2.metric("Sections", sections)
    
    c3.metric("Highest Total", f"{df['Grand Total (600)'].max()} / 600")
    c4.metric("Class Avg %", f"{df['Percentage (%)'].mean():.1f}%")

with tab_help:
    st.subheader("❓ What can I ask?")
    st.markdown(
        """
| Category | Example Queries |
|---|---|
| **Topper** | *Who is the topper of section A?*, *Who scored highest in Science?* |
| **Lowest** | *Who has the lowest marks in section B?*, *Weakest student in Maths?* |
| **Pass/Fail** | *Who passed in section C?*, *Show fail students*, *Result summary* |
| **Rankings** | *Show rank list*, *Merit list for section A* |
| **Averages** | *Class average*, *Mean marks for section D* |
| **Statistics** | *Show analysis*, *Subject-wise stats* |
| **Line Chart** | *Show graph for section B Mathematics*, *Line chart for GK* |
| **Bar Chart** | *Show bar chart for Economics* |
| **Comparison** | *Compare all subjects*, *Compare sections* |
| **Totals Chart** | *Show total marks chart* |
| **Pie Chart** | *Show pie chart of pass/fail* |
| **Student** | *Tell me about Aarav Sharma*, *Diya Patel* |
"""
    )