import streamlit as st
import pandas as pd

def classify_task(urgency, importance):
    if importance and urgency:
        return "Do First"
    elif importance and not urgency:
        return "Schedule"
    elif not importance and urgency:
        return "Delegate"
    else:
        return "Eliminate"

# Function to sort tasks based on priority and estimated time
def sort_tasks(tasks_df):
    priority_order = {
        "Do First": 1,
        "Schedule": 2,
        "Delegate": 3,
        "Eliminate": 4
    }
    tasks_df["Priority"] = tasks_df["Category"].map(priority_order)
    return tasks_df.sort_values(by=["Priority", "Estimated Time"], ascending=[True, True])

def main():
    st.set_page_config(
        page_title="Task Prioritizer",
        page_icon="",
        initial_sidebar_state="auto"
    )
    st.title("Task Prioritizer")

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # Task Input Form
    with st.form("task_form"):
        task_name = st.text_input("Task Name", "")
        urgency = st.checkbox("Is it urgent?")
        importance = st.checkbox("Is it important?")
        estimated_time = st.number_input("Estimated time to complete (in minutes)", min_value=1, step=1)

        submit = st.form_submit_button("Add Task")

        if submit and task_name:
            category = classify_task(urgency, importance)
            st.session_state.tasks.append({
                "Task": task_name,
                "Urgency": urgency,
                "Importance": importance,
                "Estimated Time": estimated_time,
                "Category": category,
                "Completed": False  # New field to track completion status
            })
            st.success("Task added successfully!")
            st.rerun()

    # Task List Section
    st.subheader("Your Tasks")
    if st.session_state.tasks:
        tasks_df = pd.DataFrame(st.session_state.tasks)

        for idx, row in tasks_df.iterrows():
            task_key = f"task_{idx}"
            col1, col2, col3 = st.columns([6, 2, 2])

            with col1:
                task_display = f"~~{row['Task']}~~" if row["Completed"] else row["Task"]
                st.markdown(task_display)

            with col2:
                if st.button("Edit", key=f"edit_{idx}"):
                    edited_task = st.text_input("Edit Task", value=row["Task"], key=f"edit_task_{idx}")
                    edited_est_time = st.number_input("Estimated time (min)", value=row["Estimated Time"], min_value=1, step=1, key=f"edit_time_{idx}")
                    urgency_edit = st.checkbox("Is it urgent?", value=row["Urgency"], key=f"edit_urgency_{idx}")
                    importance_edit = st.checkbox("Is it important?", value=row["Importance"], key=f"edit_importance_{idx}")
                    if st.button("Save Edit", key=f"save_{idx}"):
                        st.session_state.tasks[idx]["Task"] = edited_task
                        st.session_state.tasks[idx]["Urgency"] = urgency_edit
                        st.session_state.tasks[idx]["Importance"] = importance_edit
                        st.session_state.tasks[idx]["Estimated Time"] = edited_est_time
                        st.session_state.tasks[idx]["Category"] = classify_task(urgency_edit, importance_edit)
                        st.session_state.tasks[idx]["Completed"] = False  # Reset completion status after edit
                        st.rerun()

            with col3:
                if st.button("Delete", key=f"delete_{idx}"):
                    del st.session_state.tasks[idx]
                    st.rerun()

        if st.button("Clear All Tasks"):
            st.session_state.tasks = []
            st.rerun()
    else:
        st.info("No tasks added yet. Use the form above to add tasks.")

    # Eisenhower Matrix Section
    st.subheader("Eisenhower Matrix")
    if st.session_state.tasks:
        sorted_tasks = sort_tasks(pd.DataFrame(st.session_state.tasks))

        # Create empty lists for each category
        do_first = sorted_tasks[sorted_tasks["Category"] == "Do First"]
        schedule = sorted_tasks[sorted_tasks["Category"] == "Schedule"]
        delegate = sorted_tasks[sorted_tasks["Category"] == "Delegate"]
        eliminate = sorted_tasks[sorted_tasks["Category"] == "Eliminate"]

        # Layout of the matrix
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Do First (Important & Urgent)")
            for _, row in do_first.iterrows():
                st.markdown(f"- {row['Task']} ({row['Estimated Time']} min)")

        with col2:
            st.subheader("Schedule (Important, Not Urgent)")
            for _, row in schedule.iterrows():
                st.markdown(f"- {row['Task']} ({row['Estimated Time']} min)")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Delegate (Not Important, Urgent)")
            for _, row in delegate.iterrows():
                st.markdown(f"- {row['Task']} ({row['Estimated Time']} min)")

        with col4:
            st.subheader("Eliminate (Not Important & Not Urgent)")
            for _, row in eliminate.iterrows():
                st.markdown(f"- {row['Task']} ({row['Estimated Time']} min)")

if __name__ == "__main__":
    main()
