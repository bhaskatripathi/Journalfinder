import openai
import streamlit as st
import pandas as pd
import re

def chat_gpt_request(api_key, messages):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content'].strip()

def journal_finder(api_key, title, abstract, ssci, scie, esci, keywords):
    openai.api_key = api_key

    indexed_in = []
    if ssci:
        indexed_in.append("SSCI")
    if scie:
        indexed_in.append("SCIE")
    if esci:
        indexed_in.append("ESCI")

    indexed_str = ", ".join(indexed_in)
    publishers = "Sciencedirect, MDPI, IEEE, Wiley, Peerj, Emerald, PLOS"

    prompt = f"Find the top 10 best-matching journals for the following paper that are indexed in {indexed_str} and are published by {publishers}. Include information on Impact Factor, Acceptance Rate, and Review Speed.\n\nTitle: {title}\n\nAbstract: {abstract}\n\nKeywords: {keywords}\n\n"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()


st.title("Journal Finder")

with st.sidebar:
    api_key = st.text_input("API Key (masked)", type="password")
    title = st.text_input("Paper Title")
    abstract = st.text_area("Abstract")
    keywords = st.text_input("Keywords (separated by comma)")
    ssci = st.checkbox("SSCI")
    scie = st.checkbox("SCIE")
    esci = st.checkbox("ESCI")

if st.button("Find Journals"):
    if api_key and title and abstract and keywords:
        result = journal_finder(api_key, title, abstract, ssci, scie, esci, keywords)

        # Parse the results to create a dataframe
        journal_data = []

        journal_list = re.split(r"\d{1,2}\.\s", result)[1:]

        for item in journal_list:
            journal_data.append(item.split("\n"))

        df = pd.DataFrame(journal_data, columns=["Journal", "Impact Factor", "Indexed", "Acceptance Rate", "Review Speed", "Link"])

        st.write(df)
    else:
        st.error("Please fill in all required fields.")

