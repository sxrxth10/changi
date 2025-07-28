# # File: streamlit_app.py

# import streamlit as st
# import requests

# st.set_page_config(page_title="Changi RAG Chatbot", page_icon="🛫")
# st.title("🛫 Changi Airport Assistance")

# st.markdown("Ask anything that you need to know about Changi.")

# query = st.text_input("Your question:")

# if query:
#     with st.spinner("Searching..."):
#         response = requests.post(
#             "http://localhost:8000/chat",  # FastAPI URL
#             json={"query": query}
#         )
#         if response.status_code == 200:
#             data = response.json()
#             st.markdown("### 💬 Answer")
#             st.write(data["response"])
#             st.markdown("---")
#             st.markdown("### 🔗 Sources")
#             for src in data["sources"]:
#                 st.markdown(f"- {src}")
#         else:
#             st.error("Something went wrong with the backend.")


import streamlit as st
import requests

st.set_page_config(page_title="Changi Chatbot", layout="centered")

st.title("🛫 Changi Airport Assistance")

st.markdown("Ask anything that you need to know about Changi.")


# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask me about Changi Airport...")

if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔁 Backend API call
    try:
        response = requests.post(
            "http://localhost:8000/chat",  # or your deployed URL
            json={"query": user_input}
        )
        response.raise_for_status()
        answer = response.json().get("response", "Sorry, I didn't understand that.")
    except Exception as e:
        answer = f"⚠️ Error: {e}"

    # Append assistant message
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
