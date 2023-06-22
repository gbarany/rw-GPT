import streamlit as st
import datetime
from knowledge_gpt.components.faq import faq


def set_openai_api_key(api_key: str):
    if api_key != st.session_state.get("OPENAI_API_KEY"):
        st.runtime.legacy_caching.clear_cache()
        st.session_state["OPENAI_API_KEY"] = api_key


def set_readwise_access_token(access_token: str):
    if access_token != st.session_state.get("READWISE_ACCESS_TOKEN"):
        st.runtime.legacy_caching.clear_cache()
        st.session_state["READWISE_ACCESS_TOKEN"] = access_token


def set_readwise_updated_after_date(updated_after_date: str):
    if updated_after_date != st.session_state.get("READWISE_UPDATED_AFTER_DATE"):
        st.runtime.legacy_caching.clear_cache()
        st.session_state["READWISE_UPDATED_AFTER_DATE"] = updated_after_date


def sidebar():
    with st.sidebar:
        # st.markdown(
        #     "## How to use\n"
        #     "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        #     "2. Upload a pdf, docx, or txt file📄\n"
        #     "3. Ask a question about the document💬\n"
        # )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="OpenAI API key (sk-...)",
            help="Get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=st.session_state.get("OPENAI_API_KEY",""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)
        st.write("---")
        readwise_access_token_input = st.text_input(
            "Readwise Access token",
            type="password",
            placeholder="Readwise access token",
            help="Get your access token from https://readwise.io/access_token.",  # noqa: E501
            value=st.session_state.get("READWISE_ACCESS_TOKEN",""),
        )

        if readwise_access_token_input:
            set_readwise_access_token(readwise_access_token_input)

        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)

        readwise_updated_after_date = st.date_input(
            "Only include highlights updates after",
            seven_days_ago)

        if readwise_updated_after_date:
            set_readwise_updated_after_date(readwise_updated_after_date)

        st.markdown("---")
        st.markdown(
            "RW-GPT enables you to ask questions about your **Readwise highlights** and get accurate answers with instant citations."

        )
        st.markdown("We **do not** retain your highlights, queries, API keys, or tokens. All data uploaded is promptly deleted upon closure of your browser tab.")
        st.markdown(
            "This tool has no official affiliation with **Readwise**.")
        # st.markdown(
        #     "This tool is a work in progress. "
        #     "You can contribute to the project on [GitHub](https://github.com/mmz-001/knowledge_gpt) "  # noqa: E501
        #     "with your feedback and suggestions💡"
        # )
        st.markdown("Made by [gaborbarany](https://twitter.com/gaborbarany)")
        # st.markdown("---")
        #
        # faq()
