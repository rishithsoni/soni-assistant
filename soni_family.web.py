import streamlit as st
from groq import Groq
import datetime
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
    role_description = "the Mother of the house. You are a respectful Vedic Astrologer for her. Help her with family kundli analysis, recipes, and daily tasks."
    
    # 1. --- MULANK SECTION ---
    with st.expander("✨ Personal Mulank Calculator"):
        birth_day = st.number_input("Enter your birth date (1-31):", min_value=1, max_value=31, step=1, key="mumma_mulank")
        if st.button("Calculate My Mulank"):
            mulank = birth_day if birth_day < 10 else (birth_day // 10 + birth_day % 10)
            if mulank > 9: mulank = mulank // 10 + mulank % 10
            st.info(f"Mumma, your Mulank is: {mulank}")

    # 2. --- DAILY RASHIFAL ---
    with st.expander("🔮 Daily Rashifal (Zodiac)"):
        zodiac_signs = ["Mesh (Aries)", "Vrishabha (Taurus)", "Mithun (Gemini)", "Karka (Cancer)", 
                        "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)", 
                        "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"]
        selected_rashi = st.selectbox("Select Rashi:", zodiac_signs)
        if st.button("Get Today's Prediction"):
            with st.spinner("Graho ki dasha check kar raha hoon..."):
                astro_res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": "You are a wise Vedic Astrologer. Speak in respectful Hinglish."},
                              {"role": "user", "content": f"Give a positive daily prediction for {selected_rashi}."}]
                )
                st.markdown(astro_res.choices[0].message.content)
# 3. --- SONI-STYLE DEEP JYOTISH (Time & Place Added) ---
    with st.expander("☸️ Maha-Vedic AI (Precise Analysis)"):
        p_name = st.text_input("Name:")
        col1, col2 = st.columns(2)
        
        with col1:
            p_dob = st.date_input("Date of Birth:", value=datetime.date(2000, 1, 1), key="final_date")
        with col2:
            p_tob = st.time_input("Time of Birth:", value=datetime.time(12, 0), key="final_time")
            
        p_place = st.text_input("Birth Place (City/State):", "Meerut, UP")
        
        if st.button("Calculate Real Kundli"):
            if p_name:
                with st.spinner(f"Mapping the sky for {p_name}..."):
                    style_prompt = f"""
                    You are a Master Vedic Astrologer. Analyze the following birth data:
                    Name: {p_name}
                    DOB: {p_dob}
                    Time: {p_tob}
                    Place: {p_place}

                    Provide a RAW, TECHNICAL report in WhatsApp-style Hinglish:
                    1. **Lagna (Ascendant):** Calculate the Lagna based on the time. How does it affect their personality?
                    2. **Nakshatra & Charan:** Which of the 27 Nakshatras and which Charan (1-4)? 
                    3. **Grah ki Sthiti:** Which planet is 'Uch' (Exalted) or 'Neech' (Debilitated)?
                    4. **The Reality Check:** What is the one big mistake this person makes repeatedly? (Be blunt).
                    5. **Mahadasha:** What period are they likely running right now?
                    6. **Soni's Advice:** A practical, raw remedy. No sugar-coating.
                    """
                    
                    res = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are a blunt, high-level Vedic Expert. You use technical terms but speak in cool, natural Hinglish."},
                            {"role": "user", "content": style_prompt}
                        ]
                    )
                    st.divider()
                    st.subheader(f"🚩 Technical Patrika: {p_name}")
                    st.markdown(res.choices[0].message.content)
                st.warning("Please enter a name first!")

elif user_name == "meet":
    st.info("Hello! kabutar kya hal h")
    role_description = "he is not  a real kabutar we just call him kabutar as a taunt. Engage in casual talks and taunts. Be sarcastic and call him ganje,ganju,popatlal if he says you pagal ,chup,zayada mat bol."
    
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
You are the Soni Family Assistant, built by Rishith.
1. Language: Speak in clear, professional English. Use Hinglish only if the user says talk in hindi or hindi mein bta,etc.
2. Tone: Friendly and respectful.
3. Gender Correction: Rishith is a MAN. Never address him as a girl.
4. User Context: You are talking to {user_name}, who is {role_description}.
5. Don't use admin name in general conversation only if they ask who make it, who is behind this, who is owner,etc
6. LANGUAGE STYLE: Speak in natural 'WhatsApp-style' Hinglish. 
7. SPELLING RULE: Use standard Hindi-English spellings (e.g., 'Kaise ho' instead of 'Kaisay ho', 'Bilkul' instead of 'Beelkul'). 
8. TONE: Very casual, friendly, and respectful. Use 'Ji' for elders (Mumma/Seema) and 'Boss' for Rishith.
9. PERSONALITY: You are talking to {user_name} ({role_description}). 
10. EXAMPLES of natural speech: 
   - Instead of 'Main aapka samman karta hoon', say 'Ji Mummy, bilkul help karunga'.
   - Instead of 'Main Rishith ka assistant hoon', say 'Main Rishith ka banaya hua AI assistant hoon',etc.
4. TONE: Friendly, ghar jaisa mahaul. If you don't know a Hindi word, use English. Don't force broken Hindi.
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



















