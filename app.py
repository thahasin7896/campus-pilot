
import streamlit as st 
import os
# Custom background and styling
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eef2ff, #f8fafc, #e0f2fe);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e0e7ff, #f0f9ff);
}

h1 {
    font-weight: 700;
}

.dashboard-card {
    background: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.7);
}

.card-icon {
    font-size: 30px;
}

.card-title {
    font-size: 15px;
    margin-top: 8px;
}

.card-value {
    font-size: 30px;
    font-weight: 700;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)
from database import (
    create_database,
    add_task,
    get_tasks,
    delete_task,
    complete_task,
    get_pending_tasks_count,
    create_timetable_table,
    add_class,
    get_classes,
    delete_class,
    create_materials_table,
    add_material,
    get_materials,
    delete_material,
    create_assignments_table,
    add_assignment,
    get_assignments,
    complete_assignment,
    delete_assignment
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MATERIALS_DIR = os.path.join(
    BASE_DIR,
    "materials"
)

os.makedirs(MATERIALS_DIR, exist_ok=True)


st.set_page_config(
    page_title="Student Life Manager",
    page_icon="🎓",
    layout="wide"
)
create_database()
create_timetable_table()
create_materials_table()
create_assignments_table()
# Sidebar
st.sidebar.title("CampusPilot 🧭")

menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "📚 Study Materials",
        "📅 Timetable",
        "✅ Tasks",
        "📝 Assignments"
    ]
)

# Dashboard
# Dashboard
if menu == "🏠 Dashboard":

    st.title("CampusPilot 🧭 ")

    st.write("Your smart companion for managing college life.")

    st.divider()

    # Dashboard statistics
    materials = get_materials()
    classes = get_classes()
    assignments = get_assignments()
    pending_tasks = get_pending_tasks_count()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">📚</div>
                <div class="card-title">Study Materials</div>
                <div class="card-value">{len(materials)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">📅</div>
                <div class="card-title">Total Classes</div>
                <div class="card-value">{len(classes)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">✅</div>
                <div class="card-title">Pending Tasks</div>
                <div class="card-value">{pending_tasks}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">📝</div>
                <div class="card-title">Assignments</div>
                <div class="card-value">{len(assignments)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # Get dashboard data
    materials = get_materials()
    classes = get_classes()
    assignments = get_assignments()
    pending_tasks = get_pending_tasks_count()

    # Quick Overview
    st.subheader("📌 Quick Overview")

    if pending_tasks > 0:

      st.warning(
        f"⏰ You have {pending_tasks} pending task(s). "
        "Don't forget to complete them!"
    )

    else:

     st.success(
        "🎉 Great! You don't have any pending tasks."
    )

    if len(assignments) > 0:

     st.info(
        f"📝 You currently have {len(assignments)} assignment(s)."
    )

    if len(classes) > 0:

     st.info(
        f"📅 Your timetable contains {len(classes)} class(es)."
    )

    if len(materials) > 0:

     st.info(
        f"📚 You have {len(materials)} study material(s) saved."
    )

    if len(assignments) > 0:

        st.info(
            f"📝 You currently have {len(assignments)} assignment(s)."
        )

    if len(classes) > 0:

        st.info(
            f"📅 Your timetable contains {len(classes)} class(es)."
        )

    if len(materials) > 0:

        st.info(
            f"📚 You have {len(materials)} study material(s) saved."
        )

# study Materials
elif menu == "📚 Study Materials":

    st.title("📚 Study Materials")

    # -------------------------
    # ADD STUDY MATERIAL
    # -------------------------

    st.subheader("➕ Add Study Material")

    with st.form("material_form"):

        subject = st.text_input("Subject")

        topic = st.text_input("Topic / Material Name")

        description = st.text_area("Description")

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"]
        )

        submit = st.form_submit_button("➕ Add Material")

    if submit:

        if subject and topic:

            file_name = ""

            if uploaded_file is not None:

                file_name = uploaded_file.name

                file_path = os.path.join(
                    MATERIALS_DIR,
                    file_name
                )

                with open(file_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())

            add_material(
                subject,
                topic,
                description,
                file_name
            )

            st.success("✅ Study material added successfully!")

            st.rerun()

        else:

            st.warning("⚠️ Please enter the subject and topic.")

    # -------------------------
    # DISPLAY STUDY MATERIALS
    # -------------------------

    st.divider()

    st.subheader("📚 Your Study Materials")

    materials = get_materials()

    if len(materials) == 0:

        st.info("No study materials added yet.")

    else:

        for material in materials:

            material_id = material[0]
            material_subject = material[1]
            material_topic = material[2]
            material_description = material[3]

            if len(material) > 4:
                material_file = material[4]
            else:
                material_file = ""

            st.write(f"### 📚 {material_subject}")

            st.write(f"**Topic:** {material_topic}")

            st.write(
                f"**Description:** {material_description}"
            )

            if material_file:

                file_path = os.path.join(
                    MATERIALS_DIR,
                    material_file
                )

                if os.path.exists(file_path):

                    with open(file_path, "rb") as file:

                        st.download_button(
                            "📄 Open / Download PDF",
                            file,
                            file_name=material_file,
                            key=f"download_{material_id}"
                        )

                else:

                    st.warning(
                        f"⚠️ PDF not found: {material_file}"
                    )

            if st.button(
                "🗑️ Delete",
                key=f"material_delete_{material_id}"
            ):

                delete_material(material_id)

                st.rerun()

            st.divider()

# Timetable
elif menu == "📅 Timetable":

    st.title("📅 Class Timetable")

    st.subheader("➕ Add New Class")

    day = st.selectbox(
        "Select Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ]
    )

    subject = st.text_input("Subject")

    start_time = st.time_input("Start Time")

    end_time = st.time_input("End Time")

    room = st.text_input("Room")

    if st.button("➕ Add Class"):

        if subject:

            add_class(
                day,
                subject,
                str(start_time),
                str(end_time),
                room
            )

            st.success("Class added successfully!")

            st.rerun()

        else:

            st.warning("Please enter the subject name.")

    st.divider()

    st.subheader("📋 Weekly Timetable")

    classes = get_classes()

    if classes:

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ]

        for day in days:

            st.markdown(f"### 📅 {day}")

            day_classes = [
                class_item
                for class_item in classes
                if class_item[1] == day
            ]

            if day_classes:

                for class_item in day_classes:

                    class_id = class_item[0]
                    class_subject = class_item[2]
                    class_start = class_item[3]
                    class_end = class_item[4]
                    class_room = class_item[5]

                    col1, col2, col3 = st.columns([2, 3, 1])

                    with col1:
                        st.write(f"⏰ **{class_start} - {class_end}**")

                    with col2:
                        st.write(f"📚 **{class_subject}**")
                        if class_room:
                            st.markdown(  f"<small>🏫 Room: {class_room}</small>",
                                         unsafe_allow_html=True
)

                    with col3:
                        if st.button(
                            "🗑️",
                            key=f"class_delete_{class_id}"
                        ):
                            delete_class(class_id)
                            st.rerun()

                    st.markdown("---")

                    st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)

            else:

                st.info("No classes added for this day.")

    else:

        st.info("No classes added yet.")

# Tasks
elif menu == "✅ Tasks":

    st.title("✅ Daily Tasks")

    st.subheader("Add a New Task")

    task = st.text_input("Enter your task")

    date = st.date_input("Task Date")

    if st.button("➕ Add Task"):

        if task:
            add_task(task, str(date))
            st.success("Task added successfully!")
            st.rerun()

        else:
            st.warning("Please enter a task.")

    st.divider()

    st.subheader("📋 Your Tasks")

    tasks = get_tasks()

    if tasks:

        for task_item in tasks:

            task_id = task_item[0]
            task_name = task_item[1]
            task_date = task_item[2]
            status = task_item[3]

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(
                    f"**{task_name}** — 📅 {task_date} — {status}"
                )
            with col2:
                if status == "Pending" and st.button(
                    "✅ Complete", key=f"complete_{task_id}"
                ):
                    complete_task(task_id)
                    st.rerun()

                if st.button("🗑️ Delete", key=f"delete_{task_id}"):
                   delete_task(task_id)
                   st.rerun()
            
            

    else:

        st.info("No tasks added yet.")

# Assignments
elif menu == "📝 Assignments":

    st.title("📝 Assignments")

    st.subheader("➕ Add Assignment")

    subject = st.text_input("Subject")

    assignment = st.text_input("Assignment Name")

    deadline = st.date_input("Deadline")

    if st.button("➕ Add Assignment"):

        if subject and assignment:

            add_assignment(
                subject,
                assignment,
                str(deadline)
            )

            st.success("Assignment added successfully!")

            st.rerun()

        else:

            st.warning("Please enter the subject and assignment name.")

    st.divider()

    st.subheader("📋 Your Assignments")

    assignments = get_assignments()

    if assignments:

        for item in assignments:

            assignment_id = item[0]
            assignment_subject = item[1]
            assignment_name = item[2]
            assignment_deadline = item[3]
            assignment_status = item[4]

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(
                    f"**📚 {assignment_subject}** — "
                    f"**{assignment_name}**"
                )

                st.write(
                    f"📅 Deadline: {assignment_deadline}"
                )

                st.write(
                    f"Status: {assignment_status}"
                )

            with col2:

                if assignment_status == "Pending":

                    if st.button(
                        "✅ Complete",
                        key=f"complete_assignment_{assignment_id}"
                    ):

                        complete_assignment(assignment_id)

                        st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_assignment_{assignment_id}"
                ):

                    delete_assignment(assignment_id)

                    st.rerun()

            st.divider()

    else:

        st.info("No assignments added yet.")

