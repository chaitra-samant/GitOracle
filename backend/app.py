import streamlit as st
import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"

def call_api(endpoint: str, method: str = "GET", data: Dict[Any, Any] = None) -> Dict[Any, Any]:
    """Make API calls to FastAPI backend"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            st.error(f"Unsupported HTTP method: {method}")
            return {}
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
            return {}
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Make sure FastAPI is running on localhost:8000")
        return {}
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return {}

def main():
    st.set_page_config(
        page_title="GitHub RAG System",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 GitHub RAG System")
    st.markdown("Ingest GitHub repositories and query their contents using RAG")
    
    # Sidebar for system status
    with st.sidebar:
        st.header("System Status")
        
        if st.button("🔄 Refresh Status"):
            st.rerun()
        
        status = call_api("/status")
        if status:
            st.success("✅ API Connected") if status else st.error("❌ API Disconnected")
            
            if status.get("database_exists"):
                st.success("✅ Database Ready")
            else:
                st.warning("⚠️ No Database Found")
            
            repos = status.get("ingested_repositories", [])
            if repos:
                st.info(f"📚 {len(repos)} Repository(ies) Ingested")
                with st.expander("View Repositories"):
                    for repo in repos:
                        st.text(f"• {repo}")
            else:
                st.info("📚 No Repositories Ingested")
        
        st.markdown("---")
        if st.button("🗑️ Reset Database", type="secondary"):
            if st.session_state.get("confirm_reset"):
                result = call_api("/reset", method="DELETE")
                if result:
                    st.success("Database reset successfully!")
                    st.session_state.confirm_reset = False
                    st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("Click again to confirm reset")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📥 Ingest Repository")
        
        github_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository",
            help="Enter the full GitHub repository URL"
        )
        
        if st.button("🚀 Ingest Repository", type="primary"):
            if not github_url:
                st.error("Please enter a GitHub URL")
            else:
                with st.spinner("Ingesting repository... This may take a few minutes."):
                    result = call_api("/ingest", method="POST", data={"github_url": github_url})
                    
                    if result:
                        if result.get("success"):
                            st.success(result.get("message", "Success!"))
                            if result.get("files_created"):
                                with st.expander("Files Created"):
                                    for file in result["files_created"]:
                                        st.text(f"• {file}")
                        else:
                            st.error(result.get("message", "Ingestion failed"))
        
        # Example URLs
        with st.expander("📋 Example URLs"):
            examples = [
                "https://github.com/octocat/Hello-World",
                "https://github.com/microsoft/vscode",
                "https://github.com/facebook/react"
            ]
            for example in examples:
                if st.button(f"Use: {example}", key=f"example_{example}"):
                    st.session_state.github_url = example
                    st.rerun()
    
    with col2:
        st.header("💬 Query Repository")
        
        # Check if database exists
        status = call_api("/status")
        if not status.get("database_exists"):
            st.warning("⚠️ No knowledge base found. Please ingest a repository first.")
            st.stop()
        
        query = st.text_area(
            "Your Question",
            placeholder="What does this repository do? How do I use the main function? What are the key components?",
            height=100
        )
        
        col_query, col_clear = st.columns([3, 1])
        with col_query:
            ask_button = st.button("🔍 Ask Question", type="primary")
        with col_clear:
            if st.button("🗑️ Clear"):
                st.session_state.query_history = []
                st.rerun()
        
        if ask_button and query:
            with st.spinner("Searching knowledge base..."):
                result = call_api("/query", method="POST", data={"query": query, "k": 5})
                
                if result:
                    st.markdown("### 📝 Answer")
                    st.markdown(result.get("response", "No response received"))
                    
                    sources = result.get("sources", [])
                    if sources:
                        st.markdown("### 📚 Sources")
                        for i, source in enumerate(sources, 1):
                            st.text(f"{i}. {source}")
                    
                    # Store in session state for history
                    if "query_history" not in st.session_state:
                        st.session_state.query_history = []
                    
                    st.session_state.query_history.append({
                        "query": query,
                        "response": result.get("response", ""),
                        "sources": sources
                    })
        
        # Query History
        if hasattr(st.session_state, "query_history") and st.session_state.query_history:
            st.markdown("---")
            st.markdown("### 📜 Query History")
            
            for i, item in enumerate(reversed(st.session_state.query_history[-5:]), 1):
                with st.expander(f"Q{i}: {item['query'][:50]}..."):
                    st.markdown(f"**Question:** {item['query']}")
                    st.markdown(f"**Answer:** {item['response']}")
                    if item['sources']:
                        st.markdown("**Sources:**")
                        for source in item['sources']:
                            st.text(f"• {source}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        💡 Tip: Try asking about specific functions, file structures, or implementation details
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()