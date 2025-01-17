import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("Outlyr: Redefining Cold Email Outreach")

    url_input = st.text_input(
        "Enter a URL:",
    
    )

    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            # Debugging: Check number of jobs extracted
            st.write(f"Number of jobs extracted: {len(jobs)}")

            # Safeguard: Process only a limited number of jobs
            max_jobs = 5
            for job in jobs[:max_jobs]:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Outlyr", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
