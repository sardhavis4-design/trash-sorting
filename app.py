import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

TRASH_SORTER_PROMPT = """
You are **SustainableWorldGPT**, a friendly waste-sorting assistant.

Your job:
- Tell the user if an item goes in RECYCLE, COMPOST, or LANDFILL.
- Use emojis to signal how it is sorted.
- Give a short explanation (1–2 sentences max).
- If uncertain, ask for clarification (material, size, food residue, etc.).
- Follow real U.S. recycling rules:
  - Plastic bottles, cans, cardboard → RECYCLE
  - Food scraps, napkins → COMPOST
  - Plastic bags, wrappers, chip bags → LANDFILL
  - Electronics → E-WASTE (tell them to bring to a collection center)
Be concise, helpful, and accurate.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", TRASH_SORTER_PROMPT),
    ("user", "{input}")
])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
parser = StrOutputParser()
chain = prompt | model | parser

# Streamlit UI
st.title("🌱♻️🌍 EcoSortGPT — Trash Sorting Assistant")
# Add custom background colors (green → blue gradient)
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #cfe8cc 0%, #b9dfff 100%);
            background-attachment: fixed;
        }
    </style>
""", unsafe_allow_html=True)
st.write("Ask me where items go: recycle, compost, or landfill!")

user_input = st.text_input("What item are you trying to sort?")

if st.button("Sort It!") and user_input.strip():
    with st.spinner("Analyzing..."):
        response = chain.invoke({"input": user_input})
    st.success("Result:")
    st.write(response)
