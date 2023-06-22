import streamlit as st
from openai.error import OpenAIError
from typing import List, Optional
from knowledge_gpt.components.sidebar import sidebar
from knowledge_gpt.utils import (
    embed_docs,
    get_answer,
    get_sources,
    parse_docx,
    parse_pdf,
    parse_txt,
    search_docs,
    text_to_docs,
    wrap_text_in_html,
    get_readwise_data
)
import datetime
import requests


def clear_submit():
    st.session_state["submit"] = False

st.set_page_config(page_title="RW-GPT", page_icon="📖", layout="centered")
# st.header("Second Brain GPT")

sidebar()

load_readwise_button = None #st.button("Load highlights")
readwise_response = None
if load_readwise_button:
    if not st.session_state.get("READWISE_ACCESS_TOKEN"):
        st.error("Please configure your Readwise API key first!")
    else:
        with st.spinner("Downloading from Readwise"):
            d = st.session_state.get("READWISE_UPDATED_AFTER_DATE")
            readwise_response = get_readwise_data(api_key=st.session_state["READWISE_ACCESS_TOKEN"],
                                                   updated_after=datetime.datetime(d.year, d.month, d.day))
            st.session_state["READWISE_RESPONSE"] = readwise_response

uploaded_file = None

index = None
doc = None

if st.session_state.get("READWISE_RESPONSE") is not None:
    doc = []
    title = []
    author = []
    for book in st.session_state.get("READWISE_RESPONSE"):
        # print("****"+(book["title"] if "title" in book else "uknown") +":"+ "\n\n".join(map(lambda x: x["text"], book["highlights"])))
        highlights = "\n\n".join(map(lambda x: x["text"], book["highlights"]))
        doc.append(highlights)
        title.append(book["title"])
        author.append(book["author"])

    text = text_to_docs(doc, title, author)

    try:
        with st.spinner("Just indexing your highlights. Might take a bit, but no sweat - we only do this once per session."):
            index = embed_docs(text)
        st.session_state["api_key_configured"] = True
    except OpenAIError as e:
        st.error(e._message)

query = st.text_area("Ask a question:", on_change=clear_submit, placeholder="Question about your highlights",)
with st.expander("Advanced Options"):
    show_all_chunks = None#st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = None #st.checkbox("Show parsed contents of the document")

if show_full_doc and doc:
    with st.expander("Document"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_text_in_html(doc)}</p>", unsafe_allow_html=True)

button = st.button("Ask")
if button or st.session_state.get("submit"):
    print(index)
    if not st.session_state.get("OPENAI_API_KEY"):
        st.error("Please set up your OpenAI API key")
    elif not st.session_state.get("READWISE_ACCESS_TOKEN"):
        st.error("Please set up your Readwise Access token")
    elif not query:
        st.error("Please enter a question")
    elif not index:
        print("Index not found")
        d = st.session_state.get("READWISE_UPDATED_AFTER_DATE")
        print("calling get_readwise_data")
        readwise_response = get_readwise_data(api_key=st.session_state["READWISE_ACCESS_TOKEN"],
                                                  updated_after=datetime.datetime(d.year, d.month, d.day))
        print("printing readwise_response"+str(readwise_response))
        st.session_state["READWISE_RESPONSE"] = readwise_response
        print("initiating rerun")
        st.session_state["submit"] = True
        st.experimental_rerun()
    else:
        st.session_state["submit"] = True
        # Output Columns
        answer_col, sources_col = st.columns(2)
        sources = search_docs(index, query)

        try:
            answer = get_answer(sources, query)
            if not show_all_chunks:
                # Get the sources for the answer
                sources = get_sources(answer, sources)

            with answer_col:
                st.markdown("#### Answer")
                st.markdown(answer["output_text"].split("SOURCES: ")[0])

            with sources_col:
                st.markdown("#### Sources")
                for source in sources:
                    st.markdown(source.page_content)
                    st.markdown(source.metadata["source"])
                    st.markdown("---")

        except OpenAIError as e:
            st.error(e._message)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
#st.markdown(hide_streamlit_style, unsafe_allow_html=True)
