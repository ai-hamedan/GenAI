import os
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests

import streamlit as st
import langchain_helper as lch
import textwrap

# Configure proxy (replace with your actual proxy)
PROXY = "http://185.255.91.31:8080"  # Format if auth required

# Set environment variables (for libraries that respect them)
os.environ["http_proxy"] = PROXY
os.environ["https_proxy"] = PROXY

# Create a custom requests session with retries
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))
session.proxies = {"http": PROXY, "https": PROXY}

# Now use this session for YouTube loader
from langchain_community.document_loaders import YoutubeLoader
loader = YoutubeLoader.from_youtube_url(
    "https://www.youtube.com/watch?v=wd7TZ4w1mSw&list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&index=3&t=140s"
)




# # Set proxy environment variables before any imports
# os.environ["http_proxy"] = "http://185.255.91.31:8080"
# os.environ["https_proxy"] = "http://185.255.91.31:8080"

st.title("YouTube Assistant")

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.sidebar.text_area(
            label="What is the YouTube video URL?",
            max_chars=200
            )
        query = st.sidebar.text_area(
            label="Ask me about the video?",
            max_chars=50,
            key="query"
            )
        openai_api_key = st.sidebar.text_input(
            label="OpenAI API Key",
            key="langchain_search_api_key_openai",
            max_chars=200,
            type="password"
            )
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/rishabkumar7/pets-name-langchain/tree/main)"
        submit_button = st.form_submit_button(label='Submit')

if query and youtube_url:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    else:
        db = lch.create_db_from_youtube_video_url(youtube_url)
        response, docs = lch.get_response_from_query(db, query)
        st.subheader("Answer:")
        st.text(textwrap.fill(response, width=85))



# import streamlit as st
# import langchain_helper as lch
# import textwrap
# import os

# # Set proxy environment variables before any imports
# os.environ["http_proxy"] = "http://185.255.91.31:8080"
# os.environ["https_proxy"] = "http://185.255.91.31:8080"

# st.title("YouTube Assistant")

# with st.sidebar:
#     with st.form(key='my_form'):
#         youtube_url = st.sidebar.text_area(
#             label="What is the YouTube video URL?",
#             max_chars=200
#             )
#         query = st.sidebar.text_area(
#             label="Ask me about the video?",
#             max_chars=50,
#             key="query"
#             )
#         openai_api_key = st.sidebar.text_input(
#             label="OpenAI API Key",
#             key="langchain_search_api_key_openai",
#             max_chars=200,
#             type="password"
#             )
#         "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#         "[View the source code](https://github.com/rishabkumar7/pets-name-langchain/tree/main)"
#         submit_button = st.form_submit_button(label='Submit')

# if query and youtube_url:
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()
#     else:
#         db = lch.create_db_from_youtube_video_url(youtube_url)
#         response, docs = lch.get_response_from_query(db, query)
#         st.subheader("Answer:")
#         st.text(textwrap.fill(response, width=85))