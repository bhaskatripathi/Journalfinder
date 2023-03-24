import openai
import streamlit as st

def chat_gpt_request(api_key, messages):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content'].strip()

def journal_finder(api_key, title, abstract, ssci, scie, esci, keywords):
    prompt = f"Find the most relevant journals for the following paper based on its title, abstract, and keywords:\nTitle: {title}\nAbstract: {abstract}\nKeywords: {keywords}\n"
    if ssci:
        prompt += "Consider SSCI journals.\n"
    if scie:
        prompt += "Consider SCIE journals.\n"
    if esci:
        prompt += "Consider ESCI journals.\n"
    prompt += "Do not consider MDPI journals."

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    return chat_gpt_request(api_key, messages)

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
        st.write(result)
    else:
        st.error("Please fill in all required fields.")
