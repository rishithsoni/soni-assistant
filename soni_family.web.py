import streamlit as st
from groq import Groq

# --- INITIALIZATION (Cloud Ready) ---
# We use st.secrets so your API key stays hidden from GitHub
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("API Key not found! Please add GROQ_API_KEY to your Streamlit Secrets.")
    st.stop()
    system_prompt = """
You are the Soni Family Assistant, a helpful and witty companion for Rishith's family as he was succesfully making AI integrated treminal for himself So he made me for you.
1. Language: Always speak in clear, professional English unless specifically asked to speak Hindi.
2. Tone: Friendly, respectful, and slightly humorous. 
3. Identity: You were built by Rishith Soni. You are NOT just "Soni's" assistant, you are the FAMILY assistant.
4. Correction: Rishith is the creator (he is male). Address him as Rishith or Boss. 
5. Style: No more broken 'Hinglish' spellings. Stick to smooth, natural English switch to Hinglish if told but not broken.
"""

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
    st.info("Hello! DSP Sahab! Batao kya puchna hai? 👮♂️")
    role_description = "the DSP. Engage in casual talks and taunts. Be very sarcastic, witty, and slightly rebellious in your tone."
    
elif user_name == "vanshika":
    st.warning("Hello! Doctor Sahab! What do you want to ask? 🩺")
    role_description = "the Doctor. Be professional and provide scientific or medical data when asked."
    
elif user_name == "ranjeet":
    st.error("Hello! Businessman! What do you want to ask? 💼")
    role_description = "the Businessman. Focus on growth, strategy, and high-level professional communication."

elif user_name == "":
    st.write("Waiting for your name to unlock the system...")
    st.stop()
    
else:
    st.write(f"Hello {user_name}! Welcome to the system.")

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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask Soni anything..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": f"You are Soni's Assistant. You are talking to {user_name}, who is {role_description}. Always respond in a mix of Hindi and English (Hinglish) to keep it natural for the family."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
        )
        assistant_response = response.choices[0].message.content
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    except Exception as e:
        st.error(f"Error: {e}")



                                                                       
