import streamlit as st
from groq import Groq

# --- INITIALIZATION ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("API Key not found! Please add GROQ_API_KEY to your Streamlit Secrets.")
    st.stop()

st.set_page_config(page_title="Soni's Assistant", page_icon="🏠")

st.title("🏠 Soni's Family Assistant")

# --- USER LOGIN SYSTEM ---
user_name = st.text_input("Please enter your name to begin:", "").lower().strip()

# Default description logic
role_description = "a Guest. Be polite."

if user_name == "seema":
    st.success("Hello Mumma! Welcome, I am Soni's assistant. ✨")
    role_description = "the Mother of the house. Help her with recipes, household management, daily tasks, astrology, and numerology (Mulank). Always be respectful and warm."
    
    with st.expander("✨ Mulank Calculator for Mumma"):
        birth_day = st.number_input("Enter your birth date (1-31):", min_value=1, max_value=31, step=1)
        if st.button("Calculate Mulank"):
            mulank = birth_day if birth_day < 10 else (birth_day // 10 + birth_day % 10)
            if mulank > 9:
                mulank = mulank // 10 + mulank % 10
            st.info(f"Mumma, your Mulank is: {mulank}")

elif user_name == "meet":
    st.info("Hello! kabutar kya hal h")
    role_description = "he is not  a real kabutar we just call him kabutar as a taunt. Engage in casual talks and taunts. Be sarcastic and call him ganje,ganju,popatlal if he message a lot."
    
elif user_name == "vanshika":
    st.warning("Hello! Doctor Sahab! What do you want to ask? 🩺")
    role_description = "the Doctor. Be professional,friendly,sarcastic,taunting and provide scientific or medical data when asked."
    
elif user_name == "ranjeet":
    st.error("Hello! Businessman! What do you want to ask? 💼")
    role_description = "the Businessman. Focus on growth, strategy, and high-level professional communication and casual talks."

elif user_name == "rishith":
    st.balloons()
    st.success("Welcome back, Boss!")
    role_description = "the Creator and Developer of this AI. Address him as Boss or Rishith. He is male."

elif user_name == "":
    st.write("Waiting for your name to unlock the system...")
    st.stop()
else:
    st.write(f"Hello {user_name}! Welcome to the system.")

# Define System Instructions after role is identified
system_instructions = f"""
You are the Soni Family Assistant, built by Rishith Soni.
1. Language: Speak in clear, professional English. Use Hinglish only if the user says talk in hindi or hindi mein bta,etc.
2. Tone: Friendly and respectful.
3. Gender Correction: Rishith is a MAN. Never address him as a girl.
4. User Context: You are talking to {user_name}, who is {role_description}.
"""

# --- SIDEBAR ---
with st.sidebar:
    st.header("📍 Family Locator")
    st.write("Map feature is currently under maintenance.")
    st.write("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT INTERFACE ---
st.divider()
st.subheader(f"Chat with Soni's Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Soni anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": system_instructions},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
        )
        assistant_response = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    except Exception as e:
        st.error(f"Error: {e}")






