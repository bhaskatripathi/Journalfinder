import openai
import streamlit as st
import pandas as pd

def chat_gpt_request(api_key, messages):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content'].strip()

def journal_finder(api_key, title, abstract, ssci, scie, esci, keywords):
    prompt = f"Find the 10 most relevant journals for the following paper based on its title, abstract, and keywords, and provide details including the impact factor, indexing, acceptance rate (if available), review speed, and link to the journal's website:\nTitle: {title}\nAbstract: {abstract}\nKeywords: {keywords}\n"
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

        # Parse the results to create a dataframe
        journals = result.split('\n\n')
        journal_data = []

        for journal in journals:
            j_data = journal.split('\n')
            name = j_data[0].strip()
            impact_factor = j_data[1].split(':')[1].strip()
            indexed = j_data[2].split(':')[1].strip()
            acceptance_rate = j_data[3].split(':')[1].strip()
            review_speed = j_data[4].split(':')[1].strip()
            link = j_data[5].split(':')[1].strip()

            journal_data.append([name, impact_factor, indexed, acceptance_rate, review_speed, link])

        df = pd.DataFrame(journal_data, columns=["Journal", "Impact Factor", "Indexed", "Acceptance Rate", "Review Speed", "Link"])
        
        st.write(df)
    else:
        st.error("Please fill in all required fields.")
