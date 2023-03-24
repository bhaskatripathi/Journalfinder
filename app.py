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
        journal_data = []

        journal_list = re.split(r"\d{1,2}\.\s", result)[1:]

        for item in journal_list:
            name_match = re.search(r"^(.*)\s*\(", item)
            if name_match:
                name = name_match.group(1)
            else:
                continue

            impact_factor_match = re.search(r"Impact Factor:\s*([\d.]+)", item)
            if impact_factor_match:
                impact_factor = impact_factor_match.group(1)
            else:
                impact_factor = ""

            indexed_match = re.search(r"Indexed:\s*([\w\s]+)", item)
            if indexed_match:
                indexed = indexed_match.group(1)
            else:
                indexed = ""

            acceptance_rate_match = re.search(r"Acceptance Rate:\s*([A-Za-z\s]+)", item)
            if acceptance_rate_match:
                acceptance_rate = acceptance_rate_match.group(1)
            else:
                acceptance_rate = "Not publicly available"

            review_speed_match = re.search(r"Review Speed:\s*(.*?)\s+from", item)
            if review_speed_match:
                review_speed = review_speed_match.group(1)
            else:
                review_speed = ""

            link_match = re.search(r"Link:\s*(\S+)", item)
            if link_match:
                link = link_match.group(1)
            else:
                link = ""

            journal_data.append([name, impact_factor, indexed, acceptance_rate, review_speed, link])



        df = pd.DataFrame(journal_data, columns=["Journal", "Impact Factor", "Indexed", "Acceptance Rate", "Review Speed", "Link"])

        st.write(df)
    else:
        st.error("Please fill in all required fields.")
