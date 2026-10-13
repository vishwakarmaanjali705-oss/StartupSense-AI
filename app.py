import streamlit as st
import re

from ai_analysis import analyze_startup

from database import (
    create_account,
    check_login,
    get_user,
    update_username,
    change_password,
    create_tables
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StartupSense AI",
    page_icon="🚀",
    layout="wide"
)

from style import apply_style, hero, card
apply_style()

# ============================================================
# CREATE DATABASE
# ============================================================

create_tables()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "new_idea"

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "username" not in st.session_state:
    st.session_state.username = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "analysis_name" not in st.session_state:
    st.session_state.analysis_name = ""

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

if "view_history_id" not in st.session_state:
    st.session_state.view_history_id = None

# ============================================================
# LOGIN / CREATE ACCOUNT
# ============================================================

if not st.session_state.logged_in:

    # ========================================================
    # LOGIN
    # ========================================================

    if st.session_state.auth_page == "login":

        st.title("🚀 StartupSense AI")

        st.write(
            "AI-powered startup decision support"
        )

        st.divider()

        st.subheader("Welcome back 👋")

        st.write(
            "Sign in to continue to your dashboard."
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button(
            "🚀 Login",
            use_container_width=True,
            type="primary"
        ):

            if not email or not password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                user = check_login(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = user[0]
                    st.session_state.email = email
                    st.session_state.page = "new_idea"

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid email or password."
                    )

        st.write("")

        st.caption(
            "Don't have an account?"
        )

        if st.button(
            "✨ Create a new account",
            use_container_width=True
        ):

            st.session_state.auth_page = "register"

            st.rerun()


    # ========================================================
    # CREATE ACCOUNT
    # ========================================================

    else:

        st.title("🚀 StartupSense AI")

        st.subheader("Create your account")

        st.write(
            "Create an account to start analyzing "
            "your startup ideas."
        )

        st.divider()

        username = st.text_input(
            "Name",
            placeholder="Enter your name"
        )

        new_email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        if st.button(
            "✨ Create Account",
            use_container_width=True,
            type="primary"
        ):

            if (
                not username
                or not new_email
                or not new_password
                or not confirm_password
            ):

                st.error(
                    "Please fill in all fields."
                )

            elif "@" not in new_email:

                st.error(
                    "Please enter a valid email address."
                )

            elif len(new_password) < 6:

                st.error(
                    "Password must be at least 6 characters."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success = create_account(
                    username,
                    new_email,
                    new_password
                )

                if success:

                    st.success(
                        "🎉 Account created successfully!"
                    )

                    st.session_state.auth_page = "login"

                    st.rerun()

                else:

                    st.error(
                        "❌ An account with this email "
                        "already exists."
                    )

        st.write("")

        if st.button(
            "← Back to Login",
            use_container_width=True
        ):

            st.session_state.auth_page = "login"

            st.rerun()


# ============================================================
# MAIN APPLICATION
# ============================================================

else:

    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.title("🚀 StartupSense")

        st.caption(
            f"Welcome, {st.session_state.username}"
        )

        st.divider()

        # ----------------------------------------------------
        # NEW IDEA
        # ----------------------------------------------------

        if st.button(
            "➕ New Idea",
            use_container_width=True
        ):

            st.session_state.page = "new_idea"

            st.rerun()

        # ----------------------------------------------------
        # ANALYSIS
        # ----------------------------------------------------

        if st.button(
            "📊 Analysis",
            use_container_width=True
        ):

            st.session_state.page = "analysis"

            st.rerun()

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        if st.button(
            "📜 History",
            use_container_width=True
        ):

            st.session_state.page = "history"

            st.rerun()

        # ----------------------------------------------------
        # SETTINGS
        # ----------------------------------------------------

        if st.button(
            "⚙️ Settings",
            use_container_width=True
        ):

            st.session_state.page = "settings"

            st.rerun()

        st.divider()

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.email = ""
            st.session_state.page = "new_idea"
            st.session_state.analysis_result = None
            st.session_state.analysis_name = ""

            st.rerun()


    # ========================================================
    # NEW IDEA PAGE
    # ========================================================

    if st.session_state.page == "new_idea":

        st.title("💡 New Startup Idea")

        st.write(
            "Enter your startup information to receive "
            "an AI-powered startup analysis."
        )

        st.divider()

        st.subheader("🚀 Startup Information")

        startup_name = st.text_input(
            "Startup Name",
            placeholder="Example: EcoCart"
        )

        description = st.text_area(
            "Describe your startup idea",
            placeholder=(
                "What problem does your startup solve? "
                "How does your solution work?"
            ),
            height=150
        )

        col1, col2 = st.columns(2)

        with col1:

            industry = st.selectbox(
                "Industry",
                [
                    "Technology",
                    "Healthcare",
                    "FinTech",
                    "Education",
                    "E-Commerce",
                    "Food & Beverage",
                    "Sustainability",
                    "Social Impact",
                    "Other"
                ]
            )

        with col2:

            business_model = st.selectbox(
                "Business Model",
                [
                    "Subscription",
                    "Freemium",
                    "Marketplace",
                    "Direct Sales",
                    "Advertising",
                    "Commission",
                    "Other"
                ]
            )

        target_market = st.text_input(
            "Target Customers",
            placeholder="Example: College students"
        )

        col1, col2 = st.columns(2)

        with col1:

            budget = st.number_input(
                "Estimated Initial Budget (₹)",
                min_value=0,
                value=100000,
                step=10000
            )

        with col2:

            competition = st.slider(
                "Competition Level",
                min_value=1,
                max_value=10,
                value=5
            )

        st.caption(
            "1 = Very Low Competition | "
            "10 = Very High Competition"
        )

        st.write("")

        # ====================================================
        # AI ANALYSIS BUTTON
        # ====================================================

        if st.button(
            "🔍 Analyze My Startup",
            use_container_width=True,
            type="primary"
        ):

            if not startup_name.strip():

                st.error(
                    "Please enter your startup name."
                )

            elif not description.strip():

                st.error(
                    "Please describe your startup idea."
                )

            elif not target_market.strip():

                st.error(
                    "Please enter your target customers."
                )

            else:

                with st.spinner(
                    "🤖 StartupSense AI is analyzing your idea..."
                ):

                    try:

                        result = analyze_startup(
                            startup_name=startup_name,
                            description=description,
                            industry=industry,
                            business_model=business_model,
                            target_market=target_market,
                            budget=budget,
                            competition=competition
                        )

                        # ------------------------------------
                        # SAVE RESULT IN SESSION
                        # ------------------------------------

                        st.session_state.analysis_result = result

                        st.session_state.analysis_name = (
                            startup_name
                        )

                        # ------------------------------------
                        # SAVE RESULT IN ANALYSIS HISTORY
                        # ------------------------------------

                        from datetime import datetime
                        import uuid

                        if "analysis_history" not in st.session_state:
                            st.session_state.analysis_history = []

                        history_entry = {
                            "id": str(uuid.uuid4()),
                            "startup_name": startup_name,
                            "date": datetime.now().strftime(
                                "%d %b %Y, %I:%M %p"
                            ),
                            "result": result,
                        }

                        st.session_state.analysis_history.insert(
                            0, history_entry
                        )
                        
                        # ------------------------------------
                        # MOVE TO ANALYSIS PAGE
                        # ------------------------------------

                        st.session_state.page = "analysis"

                        st.rerun()

                    except Exception as e:

                        st.error(
                            "❌ Something went wrong while "
                            "analyzing your startup."
                        )

                        st.caption(
                            f"Error: {e}"
                        )


    # ========================================================
    # ANALYSIS PAGE
    # ========================================================

    elif st.session_state.page == "analysis":

        st.title("📊 Startup Analysis")

        st.write(
            "AI-powered analysis of your startup idea."
        )

        st.divider()

        # ----------------------------------------------------
        # CHECK WHETHER ANALYSIS EXISTS
        # ----------------------------------------------------

        if st.session_state.analysis_result:

            st.subheader(
                f"🚀 {st.session_state.analysis_name}"
            )

            st.divider()

            # ------------------------------------------------
            # DISPLAY AI RESULT
            # ------------------------------------------------


            cleaned_result = re.sub(
    r"<br\s*/?>",
    "\n\n",
    st.session_state.analysis_result,
    flags=re.IGNORECASE
)

            st.markdown(cleaned_result)

            # ------------------------------------------------
            # ACTION BUTTONS
            # ------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "← Analyze Another Idea",
                    use_container_width=True
                ):

                    st.session_state.analysis_result = None
                    st.session_state.analysis_name = ""
                    st.session_state.page = "new_idea"

                    st.rerun()

            with col2:

                if st.button(
                    "➕ New Analysis",
                    use_container_width=True
                ):

                    st.session_state.analysis_result = None
                    st.session_state.analysis_name = ""
                    st.session_state.page = "new_idea"

                    st.rerun()

        else:

            st.info(
                "No startup analysis is available yet."
            )

            if st.button(
                "➕ Create New Analysis",
                use_container_width=True,
                type="primary"
            ):

                st.session_state.page = "new_idea"

                st.rerun()


 # ========================================================
    # HISTORY PAGE
    # ========================================================

    elif st.session_state.page == "history":

        st.title("📜 Analysis History")

        # Initialize history if it does not exist
        if "analysis_history" not in st.session_state:
            st.session_state.analysis_history = []

        if "view_history_id" not in st.session_state:
            st.session_state.view_history_id = None

        history = st.session_state.analysis_history

        st.divider()

        if not history:
            st.info(
                "📭 No previous analyses yet. "
                "Generate a startup analysis to see it here."
            )

        else:
            st.caption(f"Total analyses: {len(history)}")

            # Show selected previous analysis
            selected_id = st.session_state.view_history_id

            if selected_id is not None:

                selected = next(
                    (
                        item for item in history
                        if item["id"] == selected_id
                    ),
                    None,
                )

                if selected:
                    st.subheader(
                        f"📊 {selected['startup_name']}"
                    )

                    st.caption(selected["date"])

                    if st.button("⬅️ Back to History"):
                        st.session_state.view_history_id = None
                        st.rerun()

                    st.markdown(selected["result"])

                else:
                    st.session_state.view_history_id = None
                    st.rerun()

            else:
                # Display saved analyses
                for item in history:

                    with st.container(border=True):

                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.markdown(
                                f"**🚀 {item['startup_name']}**"
                            )
                            st.caption(item["date"])

                        with col2:
                            if st.button(
                                "View",
                                key=f"view_{item['id']}",
                                use_container_width=True,
                            ):
                                st.session_state.view_history_id = (
                                    item["id"]
                                )
                                st.rerun()

    # ========================================================
    # SETTINGS PAGE
    # ========================================================

    elif st.session_state.page == "settings":

        st.title("⚙️ Settings")

        st.write("Manage your StartupSense account.")

        st.divider()

        user = get_user(st.session_state.email)

        if user:

            current_username = user[0]
            current_email = user[1]

        
            # =================================================
            # PROFILE
            # =================================================

            st.subheader("👤 Profile")

            st.write(
                f"Email: **{current_email}**"
            )

            new_username = st.text_input(
                "Name",
                value=current_username
            )

            if st.button(
                "Save Profile",
                use_container_width=True
            ):

                if new_username.strip():

                    update_username(
                        current_email,
                        new_username.strip()
                    )

                    st.session_state.username = (
                        new_username.strip()
                    )

                    st.success(
                        "✅ Profile updated!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Name cannot be empty."
                    )

            st.divider()

            # =================================================
            # CHANGE PASSWORD
            # =================================================

            st.subheader("🔐 Change Password")

            old_password = st.text_input(
                "Current Password",
                type="password"
            )

            new_password = st.text_input(
                "New Password",
                type="password"
            )

            confirm_new_password = st.text_input(
                "Confirm New Password",
                type="password"
            )

            if st.button(
                "Change Password",
                use_container_width=True
            ):

                if not old_password:

                    st.error(
                        "Enter your current password."
                    )

                elif not new_password:

                    st.error(
                        "Enter a new password."
                    )

                elif len(new_password) < 6:

                    st.error(
                        "Password must be at least 6 characters."
                    )

                elif new_password != confirm_new_password:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    changed = change_password(
                        current_email,
                        old_password,
                        new_password
                    )

                    if changed:

                        st.success(
                            "✅ Password changed successfully!"
                        )

                    else:

                        st.error(
                            "❌ Current password is incorrect."
                        )
