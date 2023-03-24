# Scientific Journal Finder

The Scientific Journal Finder is a web application that uses OpenAI's GPT-3 language model to suggest the best matching journals for a given research paper. The application searches for journals published by popular publishers such as Sciencedirect, MDPI, IEEE, Wiley, Peerj, Emerald, and PLOS.

## Getting Started

To use the application, you will need an OpenAI API key. Once you have an API key, you can run the application by:

1. Cloning the repository to your local machine
2. Install the dependencies using `pip install -r requirements.txt`
3. Run the application using `streamlit run app.py`
4. Enter your OpenAI API key, paper title, abstract, and keywords
5. Click the "Find Journals" button to get the results

## How It Works

The Scientific Journal Finder uses OpenAI's GPT-3 language model to generate a prompt that includes the paper's title, abstract, and keywords. The prompt is designed to ask GPT-3 to suggest the best matching journals that are indexed in the selected indexes and are published by the selected publishers. GPT-3 returns a list of the best matching journals, which are displayed to the user.

## Limitations

The Scientific Journal Finder is an experimental application that uses artificial intelligence. 
The application provides suggestions and should not be considered a definitive source of information. 
The application's results should always be verified by the user and cannot be used as a substitute for professional advice.

# UML
```mermaid
classDiagram
    class JournalFinder {
        +chat_gpt_request(api_key: str, messages: List[dict]) : str
        +journal_finder(api_key: str, title: str, abstract: str, ssci: bool, scie: bool, esci: bool, keywords: str) : str
    }
    class StreamlitApp {
        +title: str
        +sidebar: object
        +api_key: str
        +title: str
        +abstract: str
        +keywords: str
        +ssci: bool
```
        +scie: bool
        +esci: bool
    }

    JournalFinder -- StreamlitApp

