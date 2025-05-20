import streamlit as st
import requests
import os
import time

# API endpoint URLs
API_URL = "http://localhost:8000"
UPLOAD_URL = f"{API_URL}/upload"
TRAIN_URL = f"{API_URL}/train"
QUERY_URL = f"{API_URL}/query"
CLEAR_URL = f"{API_URL}/clear"
STATUS_URL = f"{API_URL}/status"

def check_system_status():
    """Check if the RAG system is ready"""
    try:
        response = requests.get(STATUS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": "Failed to connect to API"}
    except Exception as e:
        return {"status": "error", "message": f"Error connecting to API: {str(e)}"}

def main():
    st.set_page_config(
        page_title="RAG Document Query System",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Document Query System")
    st.info("Make sure the backend service is running. Start it with: `python app.py`")
    
    st.markdown("""
    This application allows you to:
    1. Upload text documents
    2. Train the system on these documents
    3. Query information from the documents
    """)
    
    # Check system status
    system_status = check_system_status()
    
    # Sidebar
    with st.sidebar:
        st.header("System Controls")
        
        # Display system status
        status_color = "green" if system_status.get("status") == "ready" else "red"
        status_message = system_status.get('message', 'Unknown')
        if system_status.get("status") == "error":
            st.error(f"Backend connection error: {status_message}")
        else:
            st.markdown(f"**System Status:** <span style='color:{status_color}'>{status_message}</span>", unsafe_allow_html=True)
        
        # Upload section
        st.subheader("1. Upload Documents")
        uploaded_files = st.file_uploader("Upload text files", type=["txt"], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("Process Uploads"):
                with st.spinner("Uploading files..."):
                    for uploaded_file in uploaded_files:
                        file_content = uploaded_file.read()
                        files = {"file": (uploaded_file.name, file_content, "text/plain")}
                        response = requests.post(UPLOAD_URL, files=files)
                        if response.status_code == 200:
                            st.success(f"Uploaded: {uploaded_file.name}")
                        else:
                            st.error(f"Failed to upload {uploaded_file.name}: {response.text}")
        
        # Training section
        st.subheader("2. Train System")
        if st.button("Train on Uploaded Documents"):
            with st.spinner("Training system... This may take a moment."):
                try:
                    response = requests.post(TRAIN_URL)
                    if response.status_code == 200:
                        st.success("Training completed successfully!")
                        # Refresh status
                        time.sleep(1)
                        system_status = check_system_status()
                        status_color = "green" if system_status.get("status") == "ready" else "red"
                        st.markdown(f"**System Status:** <span style='color:{status_color}'>{system_status.get('message', 'Unknown')}</span>", unsafe_allow_html=True)
                    else:
                        st.error(f"Training failed: {response.text}")
                except Exception as e:
                    st.error(f"Error during training: {str(e)}")
        
        # Clear data section
        st.subheader("System Maintenance")
        if st.button("Clear All Data"):
            if st.checkbox("Confirm data deletion"):
                with st.spinner("Clearing all data..."):
                    try:
                        response = requests.post(CLEAR_URL)
                        if response.status_code == 200:
                            st.success("All data cleared successfully!")
                            # Refresh status
                            time.sleep(1)
                            system_status = check_system_status()
                            status_color = "green" if system_status.get("status") == "ready" else "red"
                            st.markdown(f"**System Status:** <span style='color:{status_color}'>{system_status.get('message', 'Unknown')}</span>", unsafe_allow_html=True)
                        else:
                            st.error(f"Failed to clear data: {response.text}")
                    except Exception as e:
                        st.error(f"Error clearing data: {str(e)}")
    
    # Main area for querying
    st.header("3. Query Your Documents")
    
    if system_status.get("status") != "ready":
        st.warning("⚠️ Please upload documents and train the system before querying.")
    else:
        query = st.text_input("Enter your question:", placeholder="What information are you looking for?")
        
        if st.button("Submit Query") and query:
            with st.spinner("Processing query..."):
                try:
                    response = requests.post(
                        QUERY_URL,
                        json={"query": query}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display the answer
                        st.subheader("Answer")
                        st.write(result.get("response", "No response generated"))
                        
                        # Display sources
                        st.subheader("Sources")
                        sources = result.get("sources", [])
                        if sources:
                            for i, source in enumerate(sources):
                                if source:
                                    st.text(f"{i+1}. {source}")
                        else:
                            st.text("No sources found")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()