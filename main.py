
from typing import Any, Dict, List
import streamlit as st
from core import run_llm


st.set_page_config(
    page_title="Servicenow AI Assistant",
    page_icon="*",
    layout="centered"
)

st.title(" Servicenow Documentation Assistant")
# st.caption("AI-powered RAG Assistant with Memory")

with st.sidebar:
    st.subheader("Session")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.subheader("Current Chat History")

    if "messages" in st.session_state:
        user_msgs = [
            m["content"]
            for m in st.session_state.messages
            if m["role"] == "user"
        ]

        if user_msgs:
            for msg in user_msgs[::-1]:
                st.caption(f"• {msg[:40]}{'...' if len(msg) > 40 else ''}")
        else:
            st.caption("No questions yet.")



if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi Ambika, Ask me anything about Servicenow documentation.",
        }
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about Servicenow...")

if prompt:
    # Save user message (UI)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Save to memory (Agent)
    st.session_state.chat_history.append(("user", prompt))

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                result: Dict[str, Any] = run_llm(
                    query=prompt,
                    chat_history=st.session_state.chat_history,
                )

                answer = str(result.get("result", "")).strip()
                source_docs = result.get("source_documents", [])

            # Show answer only
            st.markdown(answer)

            # Save assistant message
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

            st.session_state.chat_history.append(("assistant", answer))

            source_keywords = ["source", "reference", "link", "url"]

            if any(keyword in prompt.lower() for keyword in source_keywords):
                if source_docs:
                    unique_sources = list(
                        {doc.metadata.get("source", "Unknown") for doc in source_docs}
                    )

                    st.markdown("### 📎 References")
                    for src in unique_sources:
                        st.markdown(f"- {src}")
                else:
                    st.markdown("No sources available.")

        except Exception as e:
            st.error("Something went wrong.")
            st.exception(e)
