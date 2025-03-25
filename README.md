# Task Prioritizer
Feeling overwhelmed by a never-ending to-do list and unsure where to start? This web app helps you take control by using the Eisenhower Matrix to prioritize tasks based on urgency and importance. Simply input your tasks, mark them as urgent or important, and the app will automatically organize them into four actionable categories: "Do First," "Schedule," "Delegate," and "Eliminate."

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://taskprioritizer.streamlit.app/)

## 🛠️ Tools Used

- **Streamlit**: For building the interactive web app and hosting it on Streamlit Cloud.
- **Pandas**: For handling task sorting and data manipulation.
- **HTML/CSS**: For customizing the Eisenhower Matrix layout and task display.

## 🚀 How to Run Locally


1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

## 📄 Features

- **Add and Manage Tasks**: Input your tasks and classify them based on urgency and importance.
- **Edit and Delete Tasks**: Modify task details or remove them from the list.
- **Eisenhower Matrix View**: Automatically organizes tasks into four categories:
   1. **Do First**: Important & Urgent
   2. **Schedule**: Important but Not Urgent
   3. **Delegate**: Not Important but Urgent
   4. **Eliminate**: Not Important & Not Urgent
- **Task Completion Tracking**: Mark tasks as completed and track your progress.
- **Dynamic Sorting**: Automatically reorders tasks based on their priority and completion status.

## 👥 Credits

- **Eisenhower Matrix**: Inspired by the productivity method attributed to Dwight D. Eisenhower.
- **Streamlit**: For providing a simple and efficient framework to build the app.

## 🐝 Support

If you find this app helpful, consider supporting the project by buying a coffee:

[![Buy Me a Coffee](https://storage.ko-fi.com/cdn/kofi5.png?v=6)](https://ko-fi.com/R5R71CFRC2)

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
