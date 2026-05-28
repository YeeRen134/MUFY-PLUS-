import streamlit as st
from datetime import date
import random

# =========================
# SESSION STATE SETUP
# =========================

def initialize_session_state():
    if "tasks" not in st.session_state: #create task list if it doesnt exist
        st.session_state.tasks = []

    if "notes" not in st.session_state: #create notes storage
        st.session_state.notes = ""

    if "streak" not in st.session_state: #create streak counter
        st.session_state.streak = 0

# ===================================
# HEADER SECTION
# ===================================

def display_header():
    st.title("Study Buddy")
    st.subheader("Stay productive one step at a time.")

# ===================================
# QUOTE OF THE DAY
# ===================================

def display_quote():

    quotes = [
        "Small progress is still progress",
        "Discipline beats motivation when motivation disappears",
        "Focus on improving, not being perfect",
        "Success in exams starts with daily habits",
        "The harder you work today, the easier tomorrow becomes"
    ]

    random_quote = random.choice(quotes)

    st.info(f"Quote of the Day: {random_quote}")

# ==================================
# ADD TASK SECTION
# ==================================

def add_task_section():
    st.header("Add Study Task")
    subject = st.selectbox(
        "Choose Subject",
        ["Chemistry", "Physics", "Math", "Fundamental Math", "Advanced Math", "Biology", "Accounting", "Economics", "English", "ICT"]
    )

    task_name = st.text_input("Enter task")
    deadline = st.date_input("Select Deadline")
    add_button = st.button("Add Task")

    if add_button:  #add task when button is clicked
        if task_name != "":
            new_task = {
                "subject": subject,
                "task": task_name,
                "deadline": deadline,
                "completed":False
            }

            st.session_state.tasks.append(new_task)
            st.success("Task added successfully!")
        else:
            st.warning("Please enter a task name.")

# ===============================
# DISPLAY TASKS
# ===============================

def display_tasks():
    st.header("Your Study Tasks")

    if len(st.session_state.tasks) == 0: #if no tasks exist
        st.write("No tasks added yet.")

    for index, task in enumerate(st.session_state.tasks): #loop thru all tasks

        completed = st.checkbox(  #checkbox
            f"{task["subject"]} - {task["task"]} (Due: {task["deadline"]})",
            value=task["completed"],
            key=index
        )

        st.session_state.tasks[index]["completed"] = completed #update completion status

# ===================================
# Exam Countdown
# ===================================

def exam_countdown():
    st.header("Exam Countdown")

    exam_date = st.date_input("Select Exam Date", key="exam")

    days_left = (exam_date - date.today()).days

    st.write(f"{days_left} days left until your exam.")

# ===================================
# NOTES SECTION
# ===================================

def notes_section():
    st.header("Quick Notes")

    notes = st.text_area(
        "Write your notes here",
        value=st.session_state.notes,
        height=200
    )

    st.session_state.notes = notes

# ==================================
# SIDEBAR SECTION
# ==================================

def sidebar_section():

    with st.sidebar:

        st.header("⏱ Focus Corner")

        # ============================================
        # SIMPLE FOCUS TIMER
        # ============================================

        st.subheader("🍅 Focus Timer")

        # Create timer state
        if "timer" not in st.session_state:
            st.session_state.timer = 25 * 60

        # Convert seconds into minutes and seconds
        minutes = st.session_state.timer // 60
        seconds = st.session_state.timer % 60

        # Display timer
        st.write(f"Timer: {minutes:02}:{seconds:02}")

        # Start button
        if st.button("Start Timer"):

            if st.session_state.timer > 0:
                st.session_state.timer -= 1

        # Pause button
        if st.button("Pause Timer"):
            st.write("Timer paused.")

        # Reset button
        if st.button("Reset Timer"):
            st.session_state.timer = 25 * 60

        st.divider()

        # ============================================
        # REMINDERS
        # ============================================

        st.write("💧 Drink water")
        st.write("🧍 Stretch your body")
        st.write("👀 Rest your eyes")

        st.divider()

        # ============================================
        # TASK STATISTICS
        # ============================================

        completed_tasks = 0

        # Count completed tasks
        for task in st.session_state.tasks:

            if task["completed"]:
                completed_tasks += 1

        st.write(f"✅ Completed Tasks: {completed_tasks}")

        st.write(f"📚 Total Tasks: {len(st.session_state.tasks)}")

# ===========================
# MAIN APP
# ===========================

def main():
    initialize_session_state()
    display_header()
    display_quote()
    sidebar_section()
    add_task_section()
    display_tasks()
    exam_countdown()
    notes_section()

if __name__ == "__main__":
    main()
