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

    prompt = f"Find the top 10 best-matching journals for the following paper that are indexed in {indexed_str} and are published by {publishers}. Include information on Impact Factor, Acceptance Rate, Review Speed, and URLs.\n\nTitle: {title}\n\nAbstract: {abstract}\n\nKeywords: {keywords}\n\n"

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

def response_to_html_table(response):
    rows = response.split("\n")
    html_table = "<table border='1'>"

    # Add a header row
    html_table += "<tr><th>Journal</th><th>Impact Factor</th><th>Acceptance Rate</th><th>Review Speed</th><th>URL</th></tr>"

    for row in rows:
        if not row:
            continue

        # Extract information from the text
        name = row.split("Impact Factor:")[0].strip()
        impact_factor = row.split("Impact Factor:")[1].split("Acceptance Rate:")[0].strip()
        acceptance_rate = row.split("Acceptance Rate:")[1].split("Review Speed:")[0].strip()
        review_speed = row.split("Review Speed:")[1].split("URL:")[0].strip()
        url = row.split("URL:")[1].strip()

        html_table += f"<tr><td>{name}</td><td>{impact_factor}</td><td>{acceptance_rate}</td><td>{review_speed}</td><td>{url}</td></tr>"

    html_table += "</table>"
    return html_table





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
        
        # Convert the response to an HTML table
        html_table = response_to_html_table(result)
        
        # Display the HTML table in Streamlit
        st.markdown(html_table, unsafe_allow_html=True)
    else:
        st.error("Please fill in all required fields.")



