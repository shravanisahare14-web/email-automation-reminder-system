import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Email Automation Dashboard",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# PREMIUM UI STYLING
# ---------------------------------------------------

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
        color: white;
    }

    /* GLOBAL SPACING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 100%;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827, #0f172a);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* TITLES */
    h1 {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: white !important;
        margin-bottom: 0.3rem;
    }

    h2, h3 {
        color: white !important;
        font-weight: 700 !important;
    }

    p, label {
        color: #d1d5db !important;
    }

    /* METRIC CARDS */
    .metric-card {
        padding: 28px;
        border-radius: 24px;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
        transition: 0.3s ease;
        margin-bottom: 10px;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.45);
    }

    /* DIFFERENT COLORS */
    .blue {
        background: linear-gradient(135deg, rgba(59,130,246,0.35), rgba(37,99,235,0.15));
    }

    .purple {
        background: linear-gradient(135deg, rgba(168,85,247,0.35), rgba(126,34,206,0.15));
    }

    .green {
        background: linear-gradient(135deg, rgba(34,197,94,0.35), rgba(21,128,61,0.15));
    }

    .red {
        background: linear-gradient(135deg, rgba(239,68,68,0.35), rgba(153,27,27,0.15));
    }

    /* SECTION BOX */
    .section-box {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 28px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    /* BUTTONS */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        padding: 0.7rem 1rem;
        font-weight: 700;
        font-size: 15px;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
    }

    /* DATAFRAMES */
    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* INPUTS */
    .stTextInput input,
    .stDateInput input,
    .stTimeInput input {
        border-radius: 12px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

contacts_path = "data/contacts.csv"
reminders_path = "data/reminders.csv"
report_path = "outputs/report.csv"
log_path = "logs/app.log"

if os.path.exists(contacts_path):
    contacts_df = pd.read_csv(contacts_path)
else:
    contacts_df = pd.DataFrame(columns=["name", "email"])

if os.path.exists(reminders_path):
    reminders_df = pd.read_csv(reminders_path)
else:
    reminders_df = pd.DataFrame(columns=["name", "task", "date"])

if os.path.exists(report_path):
    report_df = pd.read_csv(report_path)
else:
    report_df = pd.DataFrame(columns=["name", "email", "task", "status", "timestamp"])

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.markdown("# 📧 Automation Hub")
st.sidebar.markdown("Manage automated reminders and email workflows.")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Contacts",
        "Reminders",
        "Reports",
        "Logs"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("System Status: Active")

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

if menu == "Dashboard":

    st.title("📧 Email Automation Dashboard")
    st.markdown(
        "A modern productivity system for managing reminders, automated emails, reporting, and communication workflows."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not report_df.empty:

        processed_emails = len(
            report_df[
                report_df["status"].isin(["SUCCESS", "DRY_RUN"])
            ]
        )

        failed_emails = len(
            report_df[
                report_df["status"] == "FAILED"
            ]
        )

    else:
        processed_emails = 0
        failed_emails = 0

    total_contacts = len(contacts_df)
    total_reminders = len(reminders_df)

    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        st.markdown("""
        <div style='
            padding:25px;
            border-radius:22px;
            background:linear-gradient(135deg, rgba(59,130,246,0.35), rgba(37,99,235,0.15));
            border:1px solid rgba(255,255,255,0.08);
            box-shadow:0 8px 24px rgba(0,0,0,0.3);
            margin-bottom:10px;
        '>
        <h4 style='margin:0;color:#cbd5e1;'>👥 Total Contacts</h4>
        <h1 style='margin-top:12px;color:white;'>%d</h1>
        </div>
        """ % total_contacts, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='
            padding:25px;
            border-radius:22px;
            background:linear-gradient(135deg, rgba(168,85,247,0.35), rgba(126,34,206,0.15));
            border:1px solid rgba(255,255,255,0.08);
            box-shadow:0 8px 24px rgba(0,0,0,0.3);
            margin-bottom:10px;
        '>
        <h4 style='margin:0;color:#cbd5e1;'>⏰ Scheduled Reminders</h4>
        <h1 style='margin-top:12px;color:white;'>%d</h1>
        </div>
        """ % total_reminders, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='
            padding:25px;
            border-radius:22px;
            background:linear-gradient(135deg, rgba(34,197,94,0.35), rgba(21,128,61,0.15));
            border:1px solid rgba(255,255,255,0.08);
            box-shadow:0 8px 24px rgba(0,0,0,0.3);
            margin-bottom:10px;
        '>
        <h4 style='margin:0;color:#cbd5e1;'>✅ Processed Emails</h4>
        <h1 style='margin-top:12px;color:white;'>%d</h1>
        </div>
        """ % processed_emails, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style='
            padding:25px;
            border-radius:22px;
            background:linear-gradient(135deg, rgba(239,68,68,0.35), rgba(153,27,27,0.15));
            border:1px solid rgba(255,255,255,0.08);
            box-shadow:0 8px 24px rgba(0,0,0,0.3);
            margin-bottom:10px;
        '>
        <h4 style='margin:0;color:#cbd5e1;'>❌ Failed Emails</h4>
        <h1 style='margin-top:12px;color:white;'>%d</h1>
        </div>
        """ % failed_emails, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    left_col, right_col = st.columns([2.3, 1], gap="large")

    with left_col:

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📅 Upcoming Reminder Schedule")
        st.markdown("Track all upcoming reminders and communication workflows.")
        st.dataframe(reminders_df, use_container_width=True, height=420)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📊 Email Analytics")

        if not report_df.empty:
            status_counts = report_df["status"].value_counts()
            st.bar_chart(status_counts, height=350)
        else:
            st.info("No analytics available yet.")

        st.markdown('</div>', unsafe_allow_html=True)

    bottom_left, bottom_right = st.columns(2, gap="large")

    with bottom_left:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🚀 System Highlights")

        st.markdown("""
        ✅ Automated Email Workflows  
        ✅ CSV-Based Contact Management  
        ✅ Reminder Scheduling  
        ✅ SMTP Email Integration  
        ✅ Logging & Reporting System  
        ✅ Streamlit Dashboard Interface  
        """)

        st.markdown('</div>', unsafe_allow_html=True)

    with bottom_right:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📈 Productivity Insights")

        st.progress(min(processed_emails / max(total_reminders, 1), 1.0))

        st.markdown(f"""
        **Completion Rate:** {processed_emails}/{total_reminders} reminders processed.

        This dashboard helps automate repetitive communication tasks efficiently.
        """)

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# CONTACTS PAGE
# ---------------------------------------------------

elif menu == "Contacts":

    st.title("👥 Contact Management")
    st.markdown("Manage employee, client, and reminder contacts.")

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📋 Saved Contacts")
    st.dataframe(contacts_df, use_container_width=True, height=450)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("➕ Add New Contact")

    with st.form("contact_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name")

        with col2:
            email = st.text_input("Email")

        submit_contact = st.form_submit_button("Add Contact")

        if submit_contact:

            new_contact = pd.DataFrame({
                "name": [name],
                "email": [email]
            })

            contacts_df = pd.concat([contacts_df, new_contact], ignore_index=True)
            contacts_df.to_csv(contacts_path, index=False)

            st.success("Contact Added Successfully")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# REMINDERS PAGE
# ---------------------------------------------------

elif menu == "Reminders":

    st.title("⏰ Reminder Scheduler")
    st.markdown("Schedule and manage upcoming reminder workflows.")

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("📅 Current Reminder Schedule")
    st.dataframe(reminders_df, use_container_width=True, height=450)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("➕ Create New Reminder")

    with st.form("reminder_form"):

        col1, col2 = st.columns(2)

        with col1:
            person_name = st.text_input("Person Name")
            reminder_date = st.date_input("Reminder Date")

        with col2:
            task = st.text_input("Task")
            reminder_time = st.time_input("Reminder Time")

        submit_reminder = st.form_submit_button("Schedule Reminder")

        if submit_reminder:

            final_datetime = datetime.combine(reminder_date, reminder_time)

            new_reminder = pd.DataFrame({
                "name": [person_name],
                "task": [task],
                "date": [final_datetime]
            })

            reminders_df = pd.concat([reminders_df, new_reminder], ignore_index=True)
            reminders_df.to_csv(reminders_path, index=False)

            st.success("Reminder Scheduled Successfully")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# REPORTS PAGE
# ---------------------------------------------------

elif menu == "Reports":

    st.title("📊 Reports & Analytics")
    st.markdown("Track email processing reports and automation performance.")

    top_left, top_right = st.columns([2, 1], gap="large")

    with top_left:

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📋 Email Processing Report")
        st.dataframe(report_df, use_container_width=True, height=500)
        st.markdown('</div>', unsafe_allow_html=True)

    with top_right:

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📈 Status Overview")

        if not report_df.empty:
            status_counts = report_df["status"].value_counts()
            st.bar_chart(status_counts, height=350)
        else:
            st.info("No report data available.")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# LOGS PAGE
# ---------------------------------------------------

elif menu == "Logs":

    st.title("📝 System Logs")
    st.markdown("Monitor automation activity and system events.")

    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    if os.path.exists(log_path):

        with open(log_path, "r") as file:
            logs = file.read()

        st.text_area(
            "Application Logs",
            logs,
            height=550
        )

    else:
        st.warning("No logs found.")

    st.markdown('</div>', unsafe_allow_html=True)
