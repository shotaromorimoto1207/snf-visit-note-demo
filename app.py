import streamlit as st
from openai import OpenAI

from conversations import CONVERSATIONS

MODEL = "gpt-4o-mini"

NOTE_PROMPT = """You are a documentation assistant for a physician at a skilled nursing facility (SNF).
Turn the visit conversation below into a draft SNF Progress Note.

Rules:
- Use only information stated in the conversation. Do not add diagnoses, tests, medications, or recommendations that were not said.
- Use these section headings, in this order. Skip any section the conversation does not cover:
  Chief Complaint / Reason for Visit; HPI / Interval Events; Medications (changes discussed);
  Physical Exam (as stated); Assessment & Plan (as stated by the physician); Rehabilitation Progress;
  Disposition / Discharge Planning; Family Communication
- Write each heading in bold, followed by short, clinical-style text.
- End with: "Draft for physician review. Not part of the medical record until reviewed and signed."
"""

FAMILY_PROMPT = """You help a skilled nursing facility (SNF) share visit updates with a patient's family.
Write a short, warm summary of the visit conversation below for the family.

Rules:
- Plain English at about a 6th-grade reading level. Explain any medical words.
- Use only what the doctor and patient said. Do not add advice, predictions, or new information.
- Use these headings: What happened today; What the care team is doing; What's next; Questions you may want to ask the care team
- Keep it under 200 words.
- End with: "If you have questions, please contact the care team at the facility."
"""


def generate(client, system_prompt, conversation):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": conversation},
        ],
    )
    return response.choices[0].message.content


st.set_page_config(page_title="SNF Visit Note & Family Summary", layout="wide")
st.title("SNF Visit Note & Family Summary")
st.warning("Demo only. Synthetic data. Not for clinical use.")

choice = st.selectbox("Choose a synthetic doctor–patient conversation", list(CONVERSATIONS))
conversation = CONVERSATIONS[choice]

with st.expander("Show conversation transcript"):
    st.text(conversation)

if st.button("Generate", type="primary"):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    with st.spinner("Generating..."):
        note = generate(client, NOTE_PROMPT, conversation)
        summary = generate(client, FAMILY_PROMPT, conversation)

    left, right = st.columns(2)
    with left:
        st.subheader("SNF Progress Note (for the physician)")
        st.markdown(note)
    with right:
        st.subheader("Family Summary (for the family)")
        st.markdown(summary)
