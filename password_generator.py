
import streamlit as st
import random
import string
import pandas as pd

def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def check_password_strength(password):
    length_criteria = len(password) >= 8
    upper_lower_criteria = any(c.islower() for c in password) and any(c.isupper() for c in password)
    digit_criteria = any(c.isdigit() for c in password)
    special_criteria = any(c in string.punctuation for c in password)
    
    score = sum([length_criteria, upper_lower_criteria, digit_criteria, special_criteria])
    if score == 4:
        return "STRONG 💪", "#008000"
    elif score == 3:
        return "MEDIUM ⚠️", "#FFA500"
    else:
        return "WEAK ❌", "#FF0000"

st.title("🔑 Random Password Generator + Strength Checker")

length = st.slider("Select Password Length", min_value=6, max_value=32, value=12)
use_digits = st.checkbox("Include Numbers (0-9)")
use_special = st.checkbox("Include Special Characters (!@#$%^&*)")

if 'history' not in st.session_state:
    st.session_state.history = []

if st.button("🔐 Generate Password"):
    password = generate_password(length, use_digits, use_special)
    st.session_state.history.append(password)
    strength, color = check_password_strength(password)
    
    st.markdown(f"### 🔑 Generated Password")
    st.code(password, language='text')
    
    st.markdown(f"### Password Strength: <span style='color:{color}'>{strength}</span>", unsafe_allow_html=True)
    
    st.write("✔️ Length is good (8+ characters)." if len(password) >= 8 else "❌ Too short (should be 8+ characters).")
    st.write("✔️ Contains both uppercase & lowercase letters." if any(c.islower() for c in password) and any(c.isupper() for c in password) else "❌ Should contain both uppercase & lowercase letters.")
    st.write("✔️ Contains numbers (0-9)." if any(c.isdigit() for c in password) else "❌ Should include at least one number.")
    st.write("✔️ Contains special characters." if any(c in string.punctuation for c in password) else "❌ Should include at least one special character (!@#$%^&*).")
    
    st.write("---")
    st.write("### 🔍 Password History")
    for i, p in enumerate(st.session_state.history[::-1]):
        st.write(f"{i+1}. {p}")
    
    df = pd.DataFrame(st.session_state.history, columns=["Passwords"])
    st.download_button("📥 Download Passwords", df.to_csv(index=False), "passwords.csv", "text/csv")
    
    st.write("---")
    st.write("Built with ❤️ by [Shabnam Wahid]")


