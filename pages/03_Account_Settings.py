import streamlit as st
from auth import handle_authentication, hash_password, verify_password, handle_logout
from database import get_user, update_user
from database import get_user, update_user

def update_user_details(username, new_name, new_email):
    return update_user(username, {"name": new_name, "email": new_email})

def change_password(username, current_password, new_password):
    user = get_user(username)
    if verify_password(current_password, user['password']):
        # Check if the new password is the same as the current password
        if verify_password(new_password, user['password']):
            return "same_password"
        
        # Hash the new password and update it in the database
        hashed_new_password = hash_password(new_password)
        return update_user(username, {"password": hashed_new_password})
    return False

def update_message_history_limit(username, limit):
    return update_user(username, {"message_history_limit": limit})

def main():
    st.title("Account Settings")

    # Authentication
    username = handle_authentication()
    if not username:
        st.warning("Please log in to access Account Settings.")
        return

    # Get user data
    user = get_user(username)

    # Initialize session state for password change
    if "password_just_changed" not in st.session_state:
        st.session_state.password_just_changed = False

    # Clear password fields if password was just changed
    if st.session_state.password_just_changed:
        st.session_state.current_password = ""
        st.session_state.new_password = ""
        st.session_state.confirm_password = ""
        st.session_state.password_just_changed = False
    # Account Details Section
    st.header("Account Details")
    new_name = st.text_input("Name", value=user['name'])
    new_email = st.text_input("Email", value=user['email'])
    if st.button("Update Details"):
        if update_user_details(username, new_name, new_email):
            st.success("Details updated successfully!")
        else:
            st.error("Failed to update details. Please try again.")

    # Password Change Section
    st.header("Change Password")
    
    current_password = st.text_input("Current Password", type="password", key="current_password")
    new_password = st.text_input("New Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
    
    if st.button("Change Password"):
        if new_password == confirm_password:
            change_result = change_password(username, current_password, new_password)
            if change_result == "same_password":
                st.error("New password cannot be the same as the current password.")
            elif change_result:
                st.success("Password changed successfully!")
                st.session_state.password_just_changed = True
                st.rerun()
            else:
                st.error("Failed to change password. Please check your current password.")
        else:
            st.error("New passwords do not match.")

    # Clear the success message and reset flag after one render
    if st.session_state.password_just_changed:
        st.session_state.password_just_changed = False

    # Assistant Information Section (Placeholder)
    st.header("Assistant Information")
    st.info("Assistant settings will be available in a future update.")

    st.header("Chat Settings")
    user = get_user(username)
    current_limit = user.get('message_history_limit', 10)  # Default to 10 if not set
    new_limit = st.slider("Message History Limit", min_value=1, max_value=20, value=current_limit, 
                          help="Set the number of previous messages to include in the chat history (1-20)")
    if st.button("Update Message History Limit"):
        if update_message_history_limit(username, new_limit):
            st.success(f"Message history limit updated to {new_limit}")
        else:
            st.error("Failed to update message history limit. Please try again.")

    # Logout
    handle_logout()

if __name__ == "__main__":
    main()
