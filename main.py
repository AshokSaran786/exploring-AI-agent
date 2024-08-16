from crewai import Crew
from textwrap import dedent
import streamlit as st
import sys

from stock_analysis_agents import StockAnalysisAgents, StreamToExpander
from stock_analysis_tasks import StockAnalysisTasks

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_icon="✈️", layout="wide")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

class FinancialCrew:
  def __init__(self, company):
    self.company = company

  def run(self):
    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()

    research_task = tasks.research(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent)
    filings_task = tasks.filings_analysis(financial_analyst_agent)
    recommend_task = tasks.recommend(investment_advisor_agent)

    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent
      ],
      tasks=[
        research_task,
        financial_task,
        filings_task,
        recommend_task
      ],
      verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
    icon("📉 Stock Analysis 📈")

    st.subheader("Let AI agents earn money for you!",
                 divider="rainbow", anchor=False)

    with st.sidebar:
        st.header("👇 Enter Details of the Company:")
        with st.form("my_form"):
            Company = st.text_input("Which company stock do you want to analyze?", placeholder="Tesla, Apple, etc.")
            submitted = st.form_submit_button("Submit")

        st.divider()


if submitted:
    with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
        with st.container(height=500, border=False):
            sys.stdout = StreamToExpander(st)
            trip_crew = FinancialCrew(Company)
            result = trip_crew.run()
        status.update(label="✅ Analysis Completed!",
                      state="complete", expanded=False)

    st.subheader(f"Your Detailed Analysis for {Company}:", anchor=False, divider="rainbow")
    st.markdown(result)
