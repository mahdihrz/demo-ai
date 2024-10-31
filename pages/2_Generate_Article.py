from io import BytesIO

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser


from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if "articles" not in st.session_state:
    st.session_state.articles = []

st.title("Generate Article")
st.write("Enter a topic to generate an article.")
topic = st.text_input("Topic", "")

if st.button("Generate Article"):
    if topic:
        with st.spinner("Generating article..."):
            try:
                # Initialize the chat model
                model = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k")  # Update model as needed

                messages = [
                    SystemMessage(content="Act like an expert in blog writing and produce an article"),
                    HumanMessage(content="Write an article about " + topic),
                ]

                parser = StrOutputParser()
                chain = model | parser

                article = chain.invoke(messages)

                st.success("Article generated successfully!")
                st.write("Generated Article:")
                st.write(article)

                if article:
                    article_data = BytesIO(article.encode("utf-8"))
                    st.download_button(
                        label="Download Article",
                        data=article_data,
                        file_name="generated_article.txt",
                        mime="text/plain"
                    )

                st.session_state.articles.append(article)
            except Exception as e:
                st.error(f"Error generating article: {e}")
    else:
        st.error("Please enter a topic.")

if st.session_state.articles:
    st.write("Previously generated articles:")
    for i, art in enumerate(st.session_state.articles):
        with st.expander(f"Article {i + 1}:"):
            st.write()
            st.write(art)