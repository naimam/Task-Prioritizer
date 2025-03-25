import streamlit as st
import pandas as pd

def classify_task(urgency, importance):
    '''Classify task based on urgency and importance '''
    if importance and urgency:
        return "Do First"
    elif importance and not urgency:
        return "Schedule"
    elif not importance and urgency:
        return "Delegate"
    else:
        return "Eliminate"

# Function to sort tasks based on priority and completion status. completed tasks are sorted to the bottom
def sort_tasks(tasks_df):
    '''Sort tasks based on priority and completion status'''
    priority_order = {
        "Do First": 1,
        "Schedule": 2,
        "Delegate": 3,
        "Eliminate": 4
    }
    tasks_df["Priority"] = tasks_df["Category"].map(priority_order)
    return tasks_df.sort_values(by=["Priority", "Completed"], ascending=[True, True])

def main():
    st.set_page_config(
        page_title="Task Prioritizer",
        page_icon="",
        initial_sidebar_state="auto",
        layout="centered"
    )
    st.title("Task Prioritizer")

    if "tasks" not in st.session_state:
        # Initialize with a default task
        st.session_state.tasks = [{
            "Task": "",
            "Urgency": False,
            "Importance": False,
            "Category": classify_task(False, False),
            "Completed": False
        }]

 

    # Task List Section
    st.subheader("Your Tasks")

     # Add Task Button
    if st.button("Add Task"):
        st.session_state.tasks.insert(0, {  # stack new task on top
            "Task": "",
            "Urgency": False,
            "Importance": False,
            "Category": classify_task(False, False),
            "Completed": False
        })
        st.rerun()

    tasks_df = pd.DataFrame(st.session_state.tasks)

    for idx, row in tasks_df.iterrows():
        task_key = f"task_{idx}"
        # Column layout for task elements
        col1, col2, col3, col4, col5 = st.columns([0.5, 6, 2, 2, 1], vertical_alignment="center", gap="small")

        # Completion Checkbox
        with col1:
            completed = st.checkbox(" ", value=row["Completed"], key=f"complete_{idx}")
            st.session_state.tasks[idx]["Completed"] = completed

        with col2:
            task_display = f"~~{row['Task']}~~" if completed else row["Task"]
            new_task = st.text_input(
               label="Task", value=row["Task"], key=f"task_text_{idx}", placeholder="Enter your task here", label_visibility="collapsed"
            )
            if new_task != row["Task"]:
                st.session_state.tasks[idx]["Task"] = new_task

        # Urgency checkbox
        with col3:
            new_urgency = st.checkbox("Urgent", value=row["Urgency"], key=f"urgency_{idx}")
            if new_urgency != row["Urgency"]:
                st.session_state.tasks[idx]["Urgency"] = new_urgency
                st.session_state.tasks[idx]["Category"] = classify_task(new_urgency, row["Importance"])

        # Importance checkbox
        with col4:
            new_importance = st.checkbox("Important", value=row["Importance"], key=f"importance_{idx}")
            if new_importance != row["Importance"]:
                st.session_state.tasks[idx]["Importance"] = new_importance
                st.session_state.tasks[idx]["Category"] = classify_task(row["Urgency"], new_importance)

        # Delete button 
        with col5:
            if st.button("🗑️", key=f"delete_{idx}"):
                del st.session_state.tasks[idx]
                st.rerun()
                
                
    # Eisenhower Matrix Section
    st.subheader("Eisenhower Matrix")

    # Filter out empty tasks
    active_tasks = [task for task in st.session_state.tasks if task["Task"].strip()]

    if active_tasks:  # Only display the matrix if there is at least one non-empty task
        sorted_tasks = sort_tasks(pd.DataFrame(active_tasks))

        # Create empty lists for each category
        do_first = sorted_tasks[sorted_tasks["Category"] == "Do First"]
        schedule = sorted_tasks[sorted_tasks["Category"] == "Schedule"]
        delegate = sorted_tasks[sorted_tasks["Category"] == "Delegate"]
        eliminate = sorted_tasks[sorted_tasks["Category"] == "Eliminate"]

        # Matrix CSS Style
        st.markdown(
            """
            <style>
            .matrix-section {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 15px;            
            }
            .matrix-section h3 {
                font-size: 18px;
                color: #333;
            }
            .matrix-section p {
                font-size: 15px;
                color: #666;
            }
            .task-item {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
                font-size: 14px;
                color: #333;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

       # Matrix Layout
        col1, col2 = st.columns(2, gap="small", vertical_alignment="top")

        with col1:
            st.markdown(
                f"""
                <div class="matrix-section">
                    <h3>Do First</h3>
                    <p>Important & Urgent</p>
                    {"".join([f'<div class="task-item">{"<s>" + row["Task"] + "</s>" if row["Completed"] else row["Task"]}</div>' for _, row in do_first.iterrows()])}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="matrix-section">
                    <h3>Delegate</h3>
                    <p>Not Important, Urgent</p>
                    {"".join([f'<div class="task-item">{"<s>" + row["Task"] + "</s>" if row["Completed"] else row["Task"]}</div>' for _, row in delegate.iterrows()])}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="matrix-section">
                    <h3>Schedule</h3>
                    <p>Important, Not Urgent</p>
                    {"".join([f'<div class="task-item">{"<s>" + row["Task"] + "</s>" if row["Completed"] else row["Task"]}</div>' for _, row in schedule.iterrows()])}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="matrix-section">
                    <h3>Eliminate</h3>
                    <p>Not Important & Not Urgent</p>
                    {"".join([f'<div class="task-item">{"<s>" + row["Task"] + "</s>" if row["Completed"] else row["Task"]}</div>' for _, row in eliminate.iterrows()])}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.info("Add at least one non-empty task to display the Eisenhower Matrix.")

if __name__ == "__main__":
        main()