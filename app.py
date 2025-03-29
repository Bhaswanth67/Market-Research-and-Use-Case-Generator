import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3
import os
import streamlit as st
import datetime
import re
from crewai import Agent, Task, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
SERPER_API_KEY = os.environ.get('SERPER_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Validate API keys
if not GEMINI_API_KEY:
    st.error("Gemini API key is not set. Please set GEMINI_API_KEY in your environment variables.")
    st.stop()
if not SERPER_API_KEY:
    st.error("Serper API key is not set. Please set SERPER_API_KEY in your environment variables.")
    st.stop()

# Initialize Gemini LLM 
llm = LLM(
    model="gemini/gemini-2.0-flash-thinking-exp-01-21",
    temperature=0.5
)

# llm = LLM(
#     model="gemini/gemini-2.0-flash-exp",
#     temperature=0.5
# )

# Initialize Serper tool for web searches
serper_tool = SerperDevTool()

# Define Agents with verbose=False
research_agent = Agent(
    role="Industry and Company Researcher",
    goal="Gather comprehensive information about the specified industry or company using Serper for web searches.",
    backstory="You are an expert researcher skilled in analyzing industries and companies using web tools. Use Serper for all search queries, including simple and complex searches.",
    verbose=False,  # Disable verbose output
    tools=[serper_tool],
    llm=llm
)

use_case_agent = Agent(
    role="AI Use Case Proposer",
    goal="Analyze research data and propose relevant AI, ML, and GenAI use cases based on industry trends and company needs.",
    backstory="You are a creative AI specialist who identifies opportunities for technology to enhance operations and customer experiences.",
    verbose=False,  # Disable verbose output
    llm=llm
)

resource_agent = Agent(
    role="Resource Link Collector",
    goal="Find and collect links to relevant datasets and resources for the proposed use cases using Serper.",
    backstory="You are a data curator adept at sourcing high-quality datasets from platforms like Kaggle, HuggingFace, and GitHub. Use Serper for all searches, including site-specific queries.",
    verbose=False,  # Disable verbose output
    tools=[serper_tool],
    llm=llm
)

report_agent = Agent(
    role="Report Compiler",
    goal="Compile the final proposal with use cases and resource links in markdown format.",
    backstory="You are a skilled writer who creates clear, actionable reports for stakeholders.",
    verbose=False,  # Disable verbose output
    llm=llm
)

# Streamlit App
st.set_page_config(page_title="Market Research & Use Case Generator", page_icon="🤖")
st.title("Market Research & Use Case Generator")

# Create proposals directory if it doesn’t exist
if not os.path.exists("proposals"):
    os.makedirs("proposals")

# List previous proposals
proposal_files = [f for f in os.listdir("proposals") if f.endswith(".md")]
proposal_files.sort(key=lambda x: os.path.getmtime(os.path.join("proposals", x)), reverse=True)

# Previous Proposals Section
st.subheader("Previous Proposals")
if proposal_files:
    selected_proposal = st.selectbox("Select a previous proposal", proposal_files)
    with open(os.path.join("proposals", selected_proposal), "r") as f:
        data = f.read()
    st.download_button(
        label="Download Selected Proposal",
        data=data,
        file_name=selected_proposal,
        mime="text/markdown"
    )
    if st.button("Delete Selected Proposal"):
        os.remove(os.path.join("proposals", selected_proposal))
        st.success(f"Deleted {selected_proposal}")
        st.experimental_rerun()
else:
    st.info("No previous proposals found.")

# Domain Selection
domains_list = [
    "Technology", "Share Price", "Finance", "Operations", "Customer Experience",
    "Supply Chain", "Marketing", "Human Resources", "Research and Development"
]
selected_domains = st.multiselect("Select domains to focus on (optional)", domains_list)
st.write("Select domains to focus the research. If none are selected, the research will be general.")

# User Input
company_or_industry = st.text_input("Enter a company or industry (e.g., Tesla, Automotive):", "")

if st.button("Generate Proposal"):
    if company_or_industry:
        with st.spinner("Generating proposal..."):
            try:
                # Define research task description based on selected domains with enhanced instructions
                if selected_domains:
                    domains_str = ", ".join(selected_domains)
                    research_description = (
                        f"Research the industry or company: {company_or_industry}, focusing on the following domains: {domains_str}. "
                        "Understand the industry segment and the company’s key offerings or strategic focus areas within these domains. "
                        "Summarize key trends or standards relevant to AI, ML, and automation in these domains, including sources. "
                        "Also, search for existing AI and ML use cases in the industry, such as 'AI applications in {company_or_industry}' or 'how {company_or_industry} is leveraging AI'. "
                        "Use Serper for all search queries, adjusting the query complexity as needed."
                    )
                else:
                    research_description = (
                        f"Research the industry or company: {company_or_industry}. "
                        "Understand the industry segment (e.g., Automotive, Finance) and the company’s key offerings or strategic focus areas (e.g., operations, customer experience). "
                        "Summarize key trends or standards relevant to AI, ML, and automation, including sources. "
                        "Also, search for existing AI and ML use cases in the industry, such as 'AI applications in {company_or_industry}' or 'how {company_or_industry} is leveraging AI'. "
                        "Use Serper for all search queries, adjusting the query complexity as needed."
                    )

                # Define Tasks with updated descriptions
                research_task = Task(
                    description=research_description,
                    expected_output="A list of insights with descriptions and source URLs.",
                    agent=research_agent
                )

                use_case_task = Task(
                    description=(
                        "Based on the research insights, analyze industry trends and standards related to AI, ML, and automation. "
                        f"Propose relevant AI, ML, and GenAI use cases for {company_or_industry} to improve processes, enhance customer satisfaction, or boost operational efficiency. "
                        "For each use case, reference the specific insights and include their source URLs from the research output."
                    ),
                    expected_output="A list of proposed use cases with descriptions, referenced insights, and source URLs.",
                    agent=use_case_agent
                )

                resource_task = Task(
                    description=(
                        "For each proposed use case, search for relevant datasets or resources on Kaggle, HuggingFace, and GitHub using Serper. "
                        "Extract key terms or phrases from each use case description to use as keywords in site-specific queries "
                        "(e.g., 'site:kaggle.com [keywords]', 'site:huggingface.co [keywords]', 'site:github.com [keywords]'). "
                        "Collect the top 3 relevant links per use case."
                    ),
                    expected_output="A list of use cases with corresponding resource links.",
                    agent=resource_agent
                )

                report_task = Task(
                    description=(
                        f"Compile a final proposal in markdown format for {company_or_industry}. "
                        f"Focused domains: {', '.join(selected_domains) if selected_domains else 'General'}. "
                        "Include research insights, proposed use cases with references to insights and source URLs, and clickable resource links. "
                        "Format references as markdown links (e.g., [Source](URL)) and ensure resource links are clickable."
                    ),
                    expected_output="A markdown report with the final proposal.",
                    agent=report_agent
                )

                # Manual Task Execution with Custom Messages
                st.write(f"Agent: {research_agent.role} is gathering information on {company_or_industry}.")
                research_output = research_task.execute_sync(agent=research_agent)

                st.write(f"Agent: {use_case_agent.role} is proposing AI use cases for {company_or_industry}.")
                use_case_output = use_case_task.execute_sync(agent=use_case_agent, context=research_output.raw)

                st.write(f"Agent: {resource_agent.role} is collecting resource links for the use cases.")
                resource_output = resource_task.execute_sync(agent=resource_agent, context=use_case_output.raw)

                st.write(f"Agent: {report_agent.role} is compiling the final proposal.")
                report_context = f"{research_output.raw}\n\n{use_case_output.raw}\n\n{resource_output.raw}"
                report_output = report_task.execute_sync(agent=report_agent, context=report_context)

                # Extract the final output
                result = report_output.raw  # Assuming 'raw' is the attribute for the string output

                # Display success message
                st.write("✅ **Proposal generated successfully!**")

                # Display the result
                st.markdown(result)

                # Save to file with unique name
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                sanitized_name = re.sub(r'[^\w]', '_', company_or_industry)
                file_name = f"{sanitized_name}_{timestamp}.md"
                file_path = os.path.join("proposals", file_name)
                with open(file_path, "w") as f:
                    f.write(result)

                # Provide download button for the new proposal
                st.download_button(
                    label="Download Proposal",
                    data=result,
                    file_name=file_name,
                    mime="text/markdown"
                )
            except ValueError as e:
                if "Invalid response from LLM call" in str(e):
                    st.error("The language model failed to generate a response. This might be due to missing information. Try a different company or industry.")
                else:
                    st.error(f"An error occurred: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.error("Please enter a company or industry.")

if __name__ == "__main__":
    pass
