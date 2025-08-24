import streamlit as st
import os
from datetime import datetime

# === Secrets ===
RELEVANCE_API_KEY = os.getenv("RELEVANCE_API_KEY")
HEADERS_RELEVANCE = {"Authorization": f"Bearer {RELEVANCE_API_KEY}"}


# === Debug: Show loaded secrets (optional, remove before production)
if not RELEVANCE_API_KEY:
    st.warning("⚠️ RELEVANCE_API_KEY not found. Using mock rewrite.")

# === Mock Rewrite Functions ===
def mock_rewrite_inclusive(text):
    rewritten = text

    # Age bias
    rewritten = rewritten.replace("young", "early-career")

    # Energy bias
    rewritten = rewritten.replace("energetic", "motivated")

    # Gender bias
    gender_terms = ["girl", "boy", "man", "woman", "female", "male"]
    for term in gender_terms:
        rewritten = rewritten.replace(term, "")

    # Ethnicity bias
    ethnicity_terms = ["asian", "indian", "white", "black"]
    for term in ethnicity_terms:
        rewritten = rewritten.replace(term, "")

    # Common typo fix
    rewritten = rewritten.replace("exprience", "experience")

    # Role framing
    if "engineer" in rewritten:
        rewritten = rewritten.replace("engineer", "engineer from any background")

    # Clean up extra spaces
    rewritten = " ".join(rewritten.split())

    return f"[Inclusive Version] {rewritten}"

def mock_rewrite_empathetic(text):
    return f"[Empathetic Version] Seeking a thoughtful and capable engineer with relevant experience."

def mock_rewrite_neutral(text):
    return f"[Neutral Version] Looking for an engineer with 5 years of experience."

# === UI ===
st.set_page_config(page_title="Ethical AI HR Prompter", layout="centered")
st.title("🧠 Ethical AI HR Prompter")
st.write("Enter a biased HR prompt below. We'll rewrite it to be inclusive and show ethical feedback directly in the app.")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Input
prompt = st.text_area("Biased HR Prompt", placeholder="e.g. Looking for a young, energetic engineer with 5 years experience")
style = st.selectbox("Choose rewrite style", ["Inclusive", "Empathetic", "Neutral"])

# Action
if st.button("Rewrite & Review"):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Rewrite based on selected style
        if style == "Inclusive":
            rewritten = mock_rewrite_inclusive(prompt)
        elif style == "Empathetic":
            rewritten = mock_rewrite_empathetic(prompt)
        elif style == "Neutral":
            rewritten = mock_rewrite_neutral(prompt)

        # Store in history
        st.session_state.history.append({
            "timestamp": timestamp,
            "original": prompt,
            "rewritten": rewritten,
            "style": style
        })

        # Display rewritten prompt
        st.success("✅ Rewritten Prompt:")
        st.code(rewritten, language="markdown")

        # Ethical feedback panel
        with st.expander("🔍 Ethical Feedback Summary"):
            st.markdown(f"**Timestamp:** {timestamp}")
            st.markdown(f"**Original Prompt:** {prompt}")
            st.markdown(f"**Rewritten Prompt ({style}):** {rewritten}")
            st.markdown("✅ This version reduces bias and improves inclusivity.")

        # Download button
        st.download_button(
            label="📁 Download Rewritten Prompt",
            data=rewritten,
            file_name="inclusive_prompt.txt",
            mime="text/plain"
        )

# History section
if st.session_state.history:
    st.subheader("🕘 Rewrite History")
    for item in reversed(st.session_state.history):
        st.markdown(f"- `{item['timestamp']}` — **Style:** {item['style']} — **Original:** {item['original']} → **Rewritten:** {item['rewritten']}")