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
# 3. --- MAHA-JYOTISH AI (Technical Vedic Analysis) ---
    with st.expander("☸️ Maha-Vedic AI (Nakshatra & Grah Analysis)"):
        p_name = st.text_input("Name for deep analysis:")
        p_dob = st.date_input("Date of Birth:", value=datetime.date(2000, 1, 1), key="deep_astro")
        
        if st.button("Calculate Maha-Kundli"):
            if p_name:
                with st.spinner(f"Calculating Nakshatras for {p_name}..."):
                    maha_prompt = f"""
                    You are an expert Vedic Astrologer specializing in Nakshatras and planetary degrees.
                    Analyze the birth date {p_dob} for {p_name}. 
                    Provide a RAW and REAL technical report in Hinglish:
                    
                    1. **Nakshatra & Pada:** Identify the likely Nakshatra and its 1-4 Pada based on the date.
                    2. **Rashi Lord (Lagan):** Who is the ruling planet and how is it behaving?
                    3. **Grah Dasha:** Mention the current likely Mahadasha influence (e.g., Rahu-Kaal or Shani-Dhaiya).
                    4. **The Shadow (Dosha):** Mention any Mangal, Kaal Sarp, or Pitra Dosha vibes.
                    5. **Career & Money:** Real talk—will they be rich or struggle? Leader or worker?
                    6. **Upay (Remedy):** A specific ritual or stone based on their Nakshatra.
                    """
                    
                    res = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are a professional Maha-Jyotish. You use technical Vedic terms like Ashwini, Rohini, Revati, etc. You tell the raw truth."},
                            {"role": "user", "content": maha_prompt}
                        ]
                    )
                    st.divider()
                    st.subheader(f"🚩 Maha-Analysis: {p_name}")
                    st.markdown(res.choices[0].message.content)
        
            else:
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


















