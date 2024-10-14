import streamlit as st
import os

@st.fragment
def file_management_content(assistant):
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0

    uploader_container = st.empty()
    
    with uploader_container:
        uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "pdf"], key=f"uploader_{st.session_state.uploader_key}")
    
    if uploaded_file is not None and not st.session_state.file_uploaded:
        if upload_file(assistant, uploaded_file):
            st.session_state.file_uploaded = True
            st.session_state.uploader_key += 1  # Increment the key to reset the uploader
            uploader_container.empty()  # Clear the uploader
            st.rerun(scope="fragment")
    
    if st.session_state.file_uploaded:
        st.success("File uploaded successfully!")
        st.session_state.file_uploaded = False  # Reset for next upload
    
    st.subheader("Uploaded Files")
    files = list_files(assistant)
    if isinstance(files, list):
        for file in files:
            col1, col2 = st.columns([3, 1])
            col1.write(f"{file.get('name', 'Unknown')}")
            if col2.button("🗑️ Delete", key=file.get('id')):
                if delete_file(assistant, file.get('id')):
                    st.success(f"Deleted {file.get('name', 'Unknown')}")
                    st.rerun(scope="fragment")
    else:
        st.error(files)  # This will be the error message if listing failed

def file_management_sidebar(assistant):
    if assistant:
        file_management_content(assistant)
    else:
        st.error("Assistant not initialized. Unable to manage files.")

def list_files(assistant):
    try:
        return assistant.list_files()
    except Exception as e:
        return f"Error listing files: {str(e)}"

def upload_file(assistant, file):
    try:
        max_size = 200 * 1024 * 1024
        if file.size > max_size:
            st.error(f"File is too large. Maximum size is {max_size/1024/1024:.2f}MB. Your file is {file.size/1024/1024:.2f}MB.")
            return False

        with st.spinner("Uploading file..."):
            temp_file_path = f"{file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(file.getbuffer())
            response = assistant.upload_file(file_path=temp_file_path)
            os.remove(temp_file_path)
        return True
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return False

def delete_file(assistant, file_id):
    try:
        assistant.delete_file(file_id=file_id)
        return True
    except Exception as e:
        st.error(f"Error deleting file: {str(e)}")
        return False
