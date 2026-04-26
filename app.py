import streamlit as st
import chatbot
import os

# 1. Page Config (Must be the first Streamlit command)
st.set_page_config(page_title="Cardiff SU Assistant", page_icon="🎓")

# 2. Custom CSS to fix the Branding (Cardiff SU Pink)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    div.stButton > button:first-child {
        background-color: #DB126C;
        color: white;
        border: none;
        border-radius: 5px;
    }
    /* Simple styling for the chat input */
    .stChatInput { border-color: #DB126C; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Simplified for Students)
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    
    st.markdown("---")
    st.title("Official SU Assistant")
    st.info("Your 24/7 guide to life at Cardiff University Students' Union.")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 4. Main Chat Interface
st.title("Cardiff Students' Union Assistant")
st.caption("✨ Knowledge base updated every hour with the latest events and news.")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about YOLO, housing advice, or society events..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching latest SU updates..."):
            response = chatbot.ask_chatbot(prompt)
            st.markdown(response)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})