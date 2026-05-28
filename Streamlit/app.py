import json
import random
import time
from datetime import date, datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


DATA_FILE = Path("study_data.json")

QUOTES = [
    "One focused session is better than ten distracted hours.",
    "Start small. Stay consistent. Win quietly.",
    "Your future results are being built by today's choices.",
    "Do the next clear thing.",
    "You are not behind. You are in progress.",
    "Focus is a skill. Every session trains it.",
]

BREAK_REMINDERS = [
    "Drink water before your next session.",
    "Stretch your shoulders and neck.",
    "Rest your eyes for 20 seconds.",
    "Take five slow breaths.",
    "Stand up and walk for one minute.",
]

PRIORITIES = ["Low", "Medium", "High", "Critical"]
MOODS = ["Focused", "Calm", "Motivated", "Tired", "Stressed"]
SUBJECT_THEMES = ["Blue", "Pink", "Mint", "Gold", "Lavender", "Coral"]


def load_data():
    """Load saved data and repair older versions of the file."""
    default_data = {
        "subjects": [],
        "tasks": [],
        "notes": "",
        "exam_date": str(date.today()),
        "last_study_date": "",
        "streak": 0,
        "focus_sessions": 0,
        "total_focus_minutes": 0,
        "mood_log": [],
    }

    if not DATA_FILE.exists():
        return default_data

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    for key, value in default_data.items():
        data.setdefault(key, value)

    fixed_subjects = []
    for subject in data["subjects"]:
        if isinstance(subject, str):
            fixed_subjects.append({"name": subject, "theme": "Blue"})
        else:
            fixed_subjects.append({
                "name": subject.get("name", "Unnamed Subject"),
                "theme": subject.get("theme", subject.get("color", subject.get("colour", "Blue"))),
            })

    data["subjects"] = fixed_subjects

    for task in data["tasks"]:
        task.setdefault("priority", "Medium")
        task.setdefault("complete", False)
        task.setdefault("points", 10)

    return data


def save_data(data):
    """Save all study data to a local JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def apply_style():
    """Apply the full high-contrast app design."""
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 8% 8%, #fef08a 0, transparent 20%),
                radial-gradient(circle at 92% 10%, #a7f3d0 0, transparent 22%),
                radial-gradient(circle at 50% 100%, #bfdbfe 0, transparent 25%),
                linear-gradient(135deg, #fff7ed 0%, #f8fafc 48%, #ecfeff 100%);
            color: #111827;
        }

        .stApp * {
            color: #111827;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #020617 0%, #172554 48%, #064e3b 100%);
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.14) !important;
            border: 2px solid rgba(255, 255, 255, 0.38) !important;
            border-radius: 14px !important;
            padding: 10px 12px !important;
            margin-bottom: 8px !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.28) !important;
            border-color: #ffffff !important;
        }

        button {
            background: linear-gradient(135deg, #111827, #3730a3) !important;
            color: #ffffff !important;
            border-radius: 14px !important;
            border: 2px solid #ffffff !important;
            font-weight: 900 !important;
            box-shadow: 0 12px 28px rgba(17, 24, 39, 0.28) !important;
        }

        button * {
            color: #ffffff !important;
            font-weight: 900 !important;
        }

        button:hover {
            background: linear-gradient(135deg, #0f766e, #14b8a6) !important;
            transform: translateY(-2px);
        }

        input, textarea {
            background: #ffffff !important;
            color: #111827 !important;
            border: 2px solid #111827 !important;
            border-radius: 12px !important;
        }

        div[data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #111827 !important;
            border: 2px solid #111827 !important;
            border-radius: 12px !important;
        }

        div[data-baseweb="select"] * {
            color: #111827 !important;
            font-weight: 800 !important;
        }

        div[data-baseweb="popover"],
        ul[role="listbox"],
        ul[role="listbox"] li {
            background: #ffffff !important;
            color: #111827 !important;
        }

        ul[role="listbox"] li:hover {
            background: #dbeafe !important;
        }

        details {
            background: #ffffff !important;
            border: 2px solid #111827 !important;
            border-radius: 18px !important;
            padding: 10px !important;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.14) !important;
        }

        summary {
            background: #111827 !important;
            color: #ffffff !important;
            border-radius: 12px !important;
            padding: 12px 14px !important;
            font-weight: 900 !important;
        }

        summary * {
            color: #ffffff !important;
        }

        div[role="radiogroup"] label {
            background: #ffffff !important;
            border: 2px solid #111827 !important;
            border-radius: 12px !important;
            padding: 8px 12px !important;
        }

        div[role="radiogroup"] label * {
            color: #111827 !important;
            font-weight: 800 !important;
        }

        .hero {
            padding: 30px;
            border-radius: 26px;
            background: linear-gradient(135deg, #ffffff 0%, #dbeafe 42%, #fef3c7 100%);
            border: 2px solid #ffffff;
            box-shadow: 0 22px 60px rgba(15, 23, 42, 0.16);
            margin-bottom: 24px;
        }

        .hero-title {
            font-size: 56px;
            font-weight: 1000;
            line-height: 1;
            margin: 0;
            color: #111827 !important;
        }

        .hero-subtitle {
            font-size: 18px;
            font-weight: 700;
            color: #334155 !important;
            margin-top: 10px;
        }

        .metric-card {
            padding: 22px;
            border-radius: 22px;
            min-height: 130px;
            border: 2px solid rgba(255,255,255,0.9);
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.14);
            transition: transform 0.18s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
        }

        .metric-number {
            font-size: 42px;
            font-weight: 1000;
            color: #111827 !important;
        }

        .metric-label {
            font-size: 14px;
            font-weight: 900;
            color: #334155 !important;
            margin-top: 8px;
        }

        .blue { background: linear-gradient(135deg, #bfdbfe, #60a5fa); }
        .pink { background: linear-gradient(135deg, #fbcfe8, #f472b6); }
        .mint { background: linear-gradient(135deg, #ccfbf1, #5eead4); }
        .gold { background: linear-gradient(135deg, #fde68a, #facc15); }
        .lavender { background: linear-gradient(135deg, #e9d5ff, #c084fc); }
        .coral { background: linear-gradient(135deg, #fed7aa, #fb7185); }

        .panel {
            background: #ffffff;
            border-left: 12px solid #3730a3;
            border-radius: 18px;
            padding: 18px 20px;
            margin-bottom: 14px;
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.12);
            transition: margin-left 0.18s ease, transform 0.18s ease;
        }

        .panel:hover {
            margin-left: 12px;
            transform: scale(1.01);
        }

        .exam-box {
            text-align: center;
            padding: 48px;
            border-radius: 30px;
            background: linear-gradient(135deg, #dc2626, #f97316, #facc15);
            box-shadow: 0 24px 60px rgba(220, 38, 38, 0.28);
        }

        .exam-number {
            font-size: 104px;
            font-weight: 1000;
            color: #111827 !important;
            line-height: 1;
        }

        .timer-circle {
            width: 280px;
            height: 280px;
            border-radius: 50%;
            margin: 24px auto;
            background: conic-gradient(#16a34a var(--progress), #e5e7eb 0);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 22px 52px rgba(15, 23, 42, 0.2);
        }

        .timer-inner {
            width: 224px;
            height: 224px;
            border-radius: 50%;
            background: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 46px;
            font-weight: 1000;
            color: #111827 !important;
        }

        .badge {
            display: inline-block;
            padding: 10px 14px;
            border-radius: 999px;
            background: #111827;
            color: #ffffff !important;
            font-weight: 900;
            margin: 5px;
        }

        div[data-testid="stAlert"] * {
            color: #111827 !important;
        }

         section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
            display: none !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            justify-content: center !important;
            text-align: center !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(page_title="Study Spark Ultimate", layout="wide")
    apply_style()


def hero():
    """Show the app header."""
    st.markdown(
        """
        <div class="hero">
            <p class="hero-title">Study Spark Ultimate</p>
            <p class="hero-subtitle">
                Your all-in-one study command center: tasks, subjects, focus, exams, notes, mood, rewards, and progress.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, theme):
    """Show a colorful metric card."""
    st.markdown(
        f"""
        <div class="metric-card {theme}">
            <div class="metric-number">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel(text):
    """Show a hover-pull information panel."""
    st.markdown(f'<div class="panel">{text}</div>', unsafe_allow_html=True)


def subject_names(data):
    """Return subject names only."""
    return [subject["name"] for subject in data["subjects"]]


def update_streak(data):
    """Update streak when a focus session starts."""
    today = str(date.today())

    if data["last_study_date"] == today:
        return

    if data["last_study_date"]:
        last_day = datetime.strptime(data["last_study_date"], "%Y-%m-%d").date()
        gap = (date.today() - last_day).days
        data["streak"] = data["streak"] + 1 if gap == 1 else 1
    else:
        data["streak"] = 1

    data["last_study_date"] = today
    save_data(data)


def play_alarm():
    """Play a browser alarm sound."""
    components.html(
        """
        <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.25, audioCtx.currentTime);
        gain.connect(audioCtx.destination);

        [700, 900, 1100].forEach((freq, index) => {
            const osc = audioCtx.createOscillator();
            osc.type = "triangle";
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime + index * 0.2);
            osc.connect(gain);
            osc.start(audioCtx.currentTime + index * 0.2);
            osc.stop(audioCtx.currentTime + index * 0.2 + 0.18);
        });
        </script>
        """,
        height=0,
    )


def sidebar(data):
    """Create navigation and sidebar stats."""
    st.sidebar.title("Study Menu")

    page = st.sidebar.radio(
        "Choose a page",
        [
            "Dashboard",
            "Mission Board",
            "Subjects",
            "Focus Timer",
            "Exam Countdown",
            "Notes",
            "Mood & Rewards",
        ],
    )

    st.sidebar.divider()
    st.sidebar.metric("Streak", f"{data['streak']} days")
    st.sidebar.metric("Focus minutes", data["total_focus_minutes"])
    st.sidebar.metric("Sessions", data["focus_sessions"])

    return page


def dashboard_page(data):
    """Show the main dashboard."""
    hero()

    total = len(data["tasks"])
    done = sum(1 for task in data["tasks"] if task["complete"])
    progress = done / total if total else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Subjects", len(data["subjects"]), "blue")
    with col2:
        metric_card("Tasks Done", f"{done}/{total}", "green")
    with col3:
        metric_card("Study Streak", f"{data['streak']} days", "gold")
    with col4:
        metric_card("Focus Sessions", data["focus_sessions"], "pink")

    st.subheader("Overall Progress")
    st.progress(progress)

    if total == 0:
        st.info("Add your first task in the Mission Board.")
    elif done == total:
        st.success("All tasks are complete. Excellent work.")
        st.balloons()
    else:
        st.write(f"You still have {total - done} task(s) left.")

    tab1, tab2, tab3 = st.tabs(["Urgent Tasks", "Study Suggestions", "Quick Actions"])

    with tab1:
        show_urgent_tasks(data)

    with tab2:
        panel("Start with the task that has the closest deadline.")
        panel("If you feel stuck, do a 10-minute review before a full focus session.")
        panel("Turn every weak topic into a small mission.")

    with tab3:
        col_a, col_b, col_c = st.columns(3)

        if col_a.button("Random Quote"):
            st.toast(random.choice(QUOTES))

        if col_b.button("Break Reminder"):
            st.toast(random.choice(BREAK_REMINDERS))

        if col_c.button("Celebrate"):
            st.balloons()


def show_urgent_tasks(data):
    """Show unfinished tasks sorted by deadline."""
    tasks = [task for task in data["tasks"] if not task["complete"]]
    tasks.sort(key=lambda task: task["deadline"])

    if not tasks:
        st.success("No urgent unfinished tasks.")
        return

    for task in tasks[:6]:
        deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        days_left = (deadline - date.today()).days

        if days_left < 0:
            st.error(f"{task['name']} | {task['subject']} | overdue")
        elif days_left <= 2:
            st.warning(f"{task['name']} | {task['subject']} | due in {days_left} day(s)")
        else:
            st.info(f"{task['name']} | {task['subject']} | due in {days_left} day(s)")


def mission_board_page(data):
    """Create, edit, complete, filter, and delete tasks."""
    hero()
    st.header("Mission Board")

    options = subject_names(data) or ["No subject"]

    with st.expander("Pull Open: Add New Mission", expanded=True):
        with st.form("add_task"):
            name = st.text_input("Mission name")
            subject = st.selectbox("Subject", options)
            deadline = st.date_input("Deadline")
            priority = st.selectbox("Priority", PRIORITIES, index=1)
            points = st.slider("Reward points", 5, 50, 10, step=5)

            if st.form_submit_button("Add Mission") and name.strip():
                data["tasks"].append({
                    "name": name.strip(),
                    "subject": subject,
                    "deadline": str(deadline),
                    "priority": priority,
                    "points": points,
                    "complete": False,
                })
                save_data(data)
                st.success("Mission added.")
                st.rerun()

    view = st.radio("Board view", ["All", "Active", "Completed", "Critical"], horizontal=True)

    for index, task in enumerate(data["tasks"]):
        if view == "Active" and task["complete"]:
            continue
        if view == "Completed" and not task["complete"]:
            continue
        if view == "Critical" and task["priority"] != "Critical":
            continue

        with st.expander(f"{task['priority']} | {task['name']} | {task['subject']}"):
            new_name = st.text_input("Mission", task["name"], key=f"name_{index}")
            new_subject = st.selectbox(
                "Subject",
                options,
                index=options.index(task["subject"]) if task["subject"] in options else 0,
                key=f"subject_{index}",
            )
            new_deadline = st.date_input(
                "Deadline",
                datetime.strptime(task["deadline"], "%Y-%m-%d").date(),
                key=f"deadline_{index}",
            )
            new_priority = st.selectbox(
                "Priority",
                PRIORITIES,
                index=PRIORITIES.index(task["priority"]),
                key=f"priority_{index}",
            )
            new_points = st.slider("Points", 5, 50, task["points"], step=5, key=f"points_{index}")
            complete = st.checkbox("Mark complete", value=task["complete"], key=f"complete_{index}")

            col1, col2 = st.columns(2)

            if col1.button("Save Mission", key=f"save_task_{index}"):
                task["name"] = new_name.strip()
                task["subject"] = new_subject
                task["deadline"] = str(new_deadline)
                task["priority"] = new_priority
                task["points"] = new_points
                task["complete"] = complete
                save_data(data)
                st.success("Mission saved.")
                st.rerun()

            if col2.button("Delete Mission", key=f"delete_task_{index}"):
                data["tasks"].pop(index)
                save_data(data)
                st.success("Mission deleted.")
                st.rerun()


def subjects_page(data):
    """Create, edit, and delete subjects."""
    hero()
    st.header("Subjects")

    with st.expander("Pull Open: Create Subject", expanded=True):
        with st.form("add_subject"):
            name = st.text_input("Subject name")
            theme = st.selectbox("Subject colour", SUBJECT_THEMES)

            if st.form_submit_button("Create Subject") and name.strip():
                if name.strip() in subject_names(data):
                    st.warning("This subject already exists.")
                else:
                    data["subjects"].append({"name": name.strip(), "theme": theme})
                    save_data(data)
                    st.success("Subject created.")
                    st.rerun()

    if not data["subjects"]:
        st.info("No subjects yet.")
        return

    for index, subject in enumerate(data["subjects"]):
        theme = subject["theme"].lower()
        metric_card(
           subject["name"],
           subject["theme"],
           theme if theme in ["blue", "pink", "mint", "gold", "lavender", "coral"] else "blue"
        )

        with st.expander(f"Edit {subject['name']}"):
            old_name = subject["name"]
            new_name = st.text_input("Subject name", old_name, key=f"subject_name_{index}")
            new_theme = st.selectbox(
                "Subject colour",
                SUBJECT_THEMES,
                index=SUBJECT_THEMES.index(subject["theme"]) if subject["theme"] in SUBJECT_THEMES else 0,
                key=f"subject_theme_{index}",
            )

            col1, col2 = st.columns(2)

            if col1.button("Save Subject", key=f"save_subject_{index}"):
                subject["name"] = new_name.strip()
                subject["theme"] = new_theme

                for task in data["tasks"]:
                    if task["subject"] == old_name:
                        task["subject"] = subject["name"]

                save_data(data)
                st.success("Subject saved.")
                st.rerun()

            if col2.button("Delete Subject", key=f"delete_subject_{index}"):
                removed = data["subjects"].pop(index)["name"]

                for task in data["tasks"]:
                    if task["subject"] == removed:
                        task["subject"] = "No subject"

                save_data(data)
                st.success("Subject deleted.")
                st.rerun()


def focus_timer_page(data):
    """Run the focus timer."""
    hero()
    st.header("Focus Timer")

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None
    if "timer_length" not in st.session_state:
        st.session_state.timer_length = 25
    if "quote" not in st.session_state:
        st.session_state.quote = random.choice(QUOTES)
    if "quote_time" not in st.session_state:
        st.session_state.quote_time = time.time()

    minutes = st.slider("Focus length", 5, 120, 25, step=5)

    col1, col2, col3 = st.columns(3)

    if col1.button("Start Focus"):
        update_streak(data)
        st.session_state.timer_running = True
        st.session_state.timer_length = minutes
        st.session_state.timer_end = time.time() + minutes * 60
        st.session_state.quote = random.choice(QUOTES)
        st.session_state.quote_time = time.time()

    if col2.button("Stop"):
        st.session_state.timer_running = False

    if col3.button("Restart"):
        st.session_state.timer_running = True
        st.session_state.timer_length = minutes
        st.session_state.timer_end = time.time() + minutes * 60

    if st.session_state.timer_running:
        remaining = int(st.session_state.timer_end - time.time())

        if remaining <= 0:
            st.session_state.timer_running = False
            data["focus_sessions"] += 1
            data["total_focus_minutes"] += st.session_state.timer_length
            save_data(data)
            st.success("Focus session complete.")
            st.warning(random.choice(BREAK_REMINDERS))
            st.balloons()
            play_alarm()
        else:
            total_seconds = st.session_state.timer_length * 60
            progress = int(((total_seconds - remaining) / total_seconds) * 100)
            mins = remaining // 60
            secs = remaining % 60

            st.markdown(
                f"""
                <div class="timer-circle" style="--progress:{progress}%;">
                    <div class="timer-inner">{mins:02d}:{secs:02d}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if time.time() - st.session_state.quote_time >= 300:
                st.session_state.quote = random.choice(QUOTES)
                st.session_state.quote_time = time.time()

            st.info(st.session_state.quote)
            time.sleep(1)
            st.rerun()
    else:
        st.info("Choose a length and start your focus session.")

    col4, col5, col6 = st.columns(3)
    with col4:
        metric_card("Sessions", data["focus_sessions"], "green")
    with col5:
        metric_card("Total Minutes", data["total_focus_minutes"], "blue")
    with col6:
        metric_card("Streak", f"{data['streak']} days", "gold")


def exam_page(data):
    """Show exam countdown and revision guidance."""
    hero()
    st.header("Exam Countdown")

    saved = datetime.strptime(data["exam_date"], "%Y-%m-%d").date()
    exam_day = st.date_input("Exam date", saved)

    if str(exam_day) != data["exam_date"]:
        data["exam_date"] = str(exam_day)
        save_data(data)

    days_left = (exam_day - date.today()).days

    st.markdown(
        f"""
        <div class="exam-box">
            <div class="exam-number">{days_left}</div>
            <h2>DAYS LEFT UNTIL EXAM</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if days_left < 0:
        st.success("This exam date has passed.")
    elif days_left <= 3:
        st.error("Emergency mode: past papers, mistakes, sleep, and high-value topics only.")
    elif days_left <= 14:
        st.warning("Serious revision window: focus on weak topics and timed practice.")
    else:
        st.info("You have time. Build a steady revision rhythm now.")

    with st.expander("Pull Open: Revision Strategy", expanded=True):
        panel("Step 1: List your weakest topics.")
        panel("Step 2: Create one mission for each weak topic.")
        panel("Step 3: Practise exam-style questions.")
        panel("Step 4: Review every mistake the same day.")
        panel("Step 5: Keep the final day light and calm.")


def notes_page(data):
    """Save quick study notes."""
    hero()
    st.header("Notes")

    prompt = random.choice([
        "What confused me today?",
        "What should I revise tomorrow?",
        "What mistake do I keep repeating?",
        "What topic finally made sense?",
    ])

    panel(f"<b>Writing prompt:</b> {prompt}")

    notes = st.text_area("Study notes", value=data["notes"], height=420)

    if st.button("Save Notes"):
        data["notes"] = notes
        save_data(data)
        st.success("Notes saved.")


def mood_rewards_page(data):
    """Track mood and show rewards."""
    hero()
    st.header("Mood & Rewards")

    mood = st.select_slider("How do you feel today?", options=MOODS)

    if st.button("Save Mood"):
        data["mood_log"].append({"date": str(date.today()), "mood": mood})
        save_data(data)
        st.success("Mood saved.")

    st.subheader("Badges")

    badges = []
    points = sum(task["points"] for task in data["tasks"] if task["complete"])

    if data["streak"] >= 3:
        badges.append("3-Day Streak")
    if data["streak"] >= 7:
        badges.append("7-Day Streak")
    if data["focus_sessions"] >= 5:
        badges.append("Focus Starter")
    if data["total_focus_minutes"] >= 120:
        badges.append("120-Minute Club")
    if points >= 100:
        badges.append("100 Mission Points")

    if badges:
        st.markdown("".join([f'<span class="badge">{badge}</span>' for badge in badges]), unsafe_allow_html=True)
    else:
        st.info("No badges yet. Complete missions or start focus sessions to earn them.")

    st.subheader("Mood History")

    if not data["mood_log"]:
        st.write("No mood check-ins yet.")
    else:
        for entry in data["mood_log"][-7:]:
            panel(f"{entry['date']} | {entry['mood']}")


def main():
    """Run the full app."""
    setup_page()
    data = load_data()
    page = sidebar(data)

    if page == "Dashboard":
        dashboard_page(data)
    elif page == "Mission Board":
        mission_board_page(data)
    elif page == "Subjects":
        subjects_page(data)
    elif page == "Focus Timer":
        focus_timer_page(data)
    elif page == "Exam Countdown":
        exam_page(data)
    elif page == "Notes":
        notes_page(data)
    elif page == "Mood & Rewards":
        mood_rewards_page(data)


main()