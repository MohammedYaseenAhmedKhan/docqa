import streamlit as st
from src.retriever import retrieve
from src.generator import generate_answer

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Enterprise Document QA",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Enterprise Document QA Assistant")
st.write(
    "Ask questions over internal company documents. "
    "Answers are generated using retrieved source content."
)

# -------------------------------
# Session state
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Input
# -------------------------------
query = st.text_input("Ask a question:", placeholder="e.g. What is the leave policy?")

# -------------------------------
# Button action
# -------------------------------
if st.button("Get Answer") and query.strip():
    with st.spinner("Retrieving documents and generating answer..."):
        chunks = retrieve(query, k=5)
        answer = generate_answer(query, chunks)

    st.session_state.history.append({
        "question": query,
        "answer": answer,
        "sources": chunks
    })

# -------------------------------
# Display results
# -------------------------------
for item in reversed(st.session_state.history):
    st.markdown("### ❓ Question")
    st.write(item["question"])

    st.markdown("### ✅ Answer")
    st.write(item["answer"])

    with st.expander("📚 View Source Documents"):
        for i, src in enumerate(item["sources"], start=1):
            st.markdown(
                f"""
                **Source {i}**  
                **Document:** `{src['doc_id']}`  
                **Page:** {src['page']}  
                **Score:** {src['score']:.3f}
                """
            )
            st.write(src["text"])
