import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("API Key not found!")
    st.stop()

# 1. MOVE THE PROMPT HERE (Outside the try/except)
system_instructions = f"""
You are the Soni Family Assistant, built by Rishith Soni (The Boss).
- You are talking to {user_name}.
- Language: Professional English. Use Hinglish ONLY if the user speaks it first. 
- Tone: Friendly and respectful.
- Identity: Rishith is a MALE. Address him as Rishith or Boss. Do not call him 'beti'.
- Specific User Role: {role_description if 'role_description' in locals() else 'a Guest'}
"""

st.set_page_config(page_title="Soni's Assistant", page_icon="🏠")
st.title("🏠 Soni's Family Assistant")

# ... (Keep your User Login System logic here) ...

# --- CHAT INTERFACE ---
# (Inside your response logic, update the messages list like this:)

if prompt := st.chat_input("Ask Soni anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": system_instructions}, # <--- USE THE NEW VARIABLE
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
        )
        # ... rest of your code ...
