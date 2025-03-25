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
        # Initialize with a default task
        st.session_state.tasks = [{
            "Task": "<Your task here>",
            "Urgency": False,
            "Importance": False,
            "Estimated Time": 1,
            "Category": classify_task(False, False),
            "Completed": False
        }]

    # Task List Section
    st.subheader("Your Tasks")
    tasks_df = pd.DataFrame(st.session_state.tasks)

    for idx, row in tasks_df.iterrows():
        task_key = f"task_{idx}"
        col1, col2, col3, col4 = st.columns([1, 5, 2, 1])

        # Checkbox for completion
        with col1:
            completed = st.checkbox("", value=row["Completed"], key=f"complete_{idx}")
            st.session_state.tasks[idx]["Completed"] = completed

        # Editable task text
        with col2:
            if completed:
                task_display = f"~~{row['Task']}~~"
            else:
                task_display = row["Task"]
            new_task = st.text_input("", value=row["Task"], key=f"task_text_{idx}")
            if new_task != row["Task"]:
                st.session_state.tasks[idx]["Task"] = new_task

        # Editable actions (estimated time, urgency, importance)
        with col3:
            new_est_time = st.number_input(
                "Time (min)", value=row["Estimated Time"], min_value=1, step=1, key=f"time_{idx}"
            )
            new_urgency = st.checkbox("Urgent", value=row["Urgency"], key=f"urgency_{idx}")
            new_importance = st.checkbox("Important", value=row["Importance"], key=f"importance_{idx}")

            # Update task details
            if (
                new_est_time != row["Estimated Time"]
                or new_urgency != row["Urgency"]
                or new_importance != row["Importance"]
            ):
                st.session_state.tasks[idx]["Estimated Time"] = new_est_time
                st.session_state.tasks[idx]["Urgency"] = new_urgency
                st.session_state.tasks[idx]["Importance"] = new_importance
                st.session_state.tasks[idx]["Category"] = classify_task(new_urgency, new_importance)

        # Delete button with trash can icon
        with col4:
            if st.button("🗑️", key=f"delete_{idx}"):
                del st.session_state.tasks[idx]
                st.rerun()

    # Add Task Button
    if st.button("Add Task"):
        st.session_state.tasks.append({
            "Task": "<Your task here>",
            "Urgency": False,
            "Importance": False,
            "Estimated Time": 1,
            "Category": classify_task(False, False),
            "Completed": False
        })
        st.rerun()

    # Eisenhower Matrix Section
    st.subheader("Eisenhower Matrix")
    if st.session_state.tasks:
        # Filter out completed tasks
        active_tasks = [task for task in st.session_state.tasks if not task["Completed"]]
        sorted_tasks = sort_tasks(pd.DataFrame(active_tasks))

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