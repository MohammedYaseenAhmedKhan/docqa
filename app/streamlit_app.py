import streamlit as st
from src.retriever import Retriever
from src.generator import generate_answer

st.set_page_config(
    page_title="Enterprise Document QA Assistant",
    layout="wide"
)

st.title("📄 Enterprise Document QA Assistant")
st.caption("Ask questions across company policies using AI-powered search")

# Initialize retriever once
@st.cache_resource
def load_retriever():
    return Retriever()

retriever = load_retriever()

question = st.text_input("Ask a question about company policies")

if st.button("Get Answer") and question:
    with st.spinner("Searching documents..."):
        chunks = retriever.search(question, k=4)

    if not chunks:
        st.warning("No relevant information found.")
    else:
        with st.spinner("Generating answer..."):
            answer = generate_answer(question, chunks)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Sources")
        for c in chunks:
            st.markdown(
                f"- **{c['doc_id']} (Page {c['page']})**"
            )
