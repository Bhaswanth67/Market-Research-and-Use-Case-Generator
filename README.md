# Market Research and Use Case Generator

Welcome to the **Market Research and Use Case Generator**, a powerful Streamlit application designed to automate the creation of detailed market research proposals for companies or industries. This project harnesses the power of Artificial Intelligence (AI), Machine Learning (ML), and Generative AI (GenAI) to deliver actionable insights, propose innovative use cases, and provide valuable resources—all formatted in clean, professional markdown files. Whether you're a business strategist, product manager, or developer, this tool simplifies the process of generating comprehensive proposals tailored to your specific needs.

---

## What Is This Project?

The **Market Research and Use Case Generator** is an open-source tool that enables users to input a company name (e.g., "Tesla") or an industry (e.g., "Automotive") and generate a detailed proposal. The proposal includes:

- **Research Insights**: Key findings about the company or industry, sourced from web searches.
- **Proposed Use Cases**: AI-driven suggestions for applying AI, ML, or GenAI to improve operations, customer experiences, or innovation.
- **Resource Links**: Curated links to datasets and tools from platforms like Kaggle, Hugging Face, and GitHub to support the proposed use cases.

The application is built using Python and leverages cutting-edge libraries such as **CrewAI** for agent-based task execution, **Streamlit** for an intuitive user interface, and APIs like **Gemini** (for language modeling) and **Serper** (for web searches). Generated proposals are saved as markdown files in a `proposals/` directory for easy access and future reference.

---

## What Does It Do?

This project automates the traditionally time-consuming process of market research and proposal creation. Here’s what it delivers:

- **Custom Input**: Users can specify a company or industry and optionally select domains (e.g., Technology, Operations, Marketing) to focus the research.
- **Automated Research**: The tool gathers up-to-date information using web searches and summarizes key trends and insights.
- **AI-Driven Proposals**: It proposes practical use cases for AI, ML, and GenAI, tailored to the input and supported by research data.
- **Resource Collection**: It finds and links relevant datasets and tools to help implement the proposed use cases.
- **Proposal Storage**: Saves each proposal as a markdown file with a unique timestamped filename (e.g., `Tesla_20250327_211020.md`).
- **History Management**: Allows users to view, download, or delete previous proposals directly from the interface.

For example, inputting "Apple" with a focus on "Technology" and "Research and Development" might generate a proposal with use cases like "GenAI-Assisted Product Design" or "Ethical AI Framework Development," complete with supporting insights and resources.

---

## How Does It Work?

The application operates by orchestrating a team of AI agents, each with a specific role, to collaboratively produce the final proposal. Here’s a step-by-step breakdown:

### 1. User Interface (Streamlit)
- Built with **Streamlit**, the app provides a simple web interface where users:
  - Enter a company or industry name.
  - Optionally select domains to refine the research scope (e.g., "Finance," "Customer Experience").
  - Click "Generate Proposal" to start the process.
  - View and manage previous proposals under a "Previous Proposals" section.

### 2. AI Agents (CrewAI)
The app uses the **CrewAI** library to define four specialized agents that work sequentially:

- **Industry and Company Researcher**:
  - **Role**: Gathers comprehensive information using the **SerperDevTool** for web searches.
  - **Task**: Researches the input (e.g., "Tesla") and focuses on selected domains or general trends if none are specified.
  - **Output**: A list of insights with descriptions and source URLs.

- **AI Use Case Proposer**:
  - **Role**: Analyzes research data to propose relevant AI, ML, and GenAI use cases.
  - **Task**: Identifies opportunities based on trends and needs, referencing the researcher’s insights.
  - **Output**: A list of use cases with descriptions, referenced insights, and source URLs.

- **Resource Link Collector**:
  - **Role**: Finds datasets and resources for the proposed use cases using **SerperDevTool**.
  - **Task**: Searches platforms like Kaggle, Hugging Face, and GitHub for relevant links.
  - **Output**: A list of use cases with up to three resource links each.

- **Report Compiler**:
  - **Role**: Compiles the final proposal in markdown format.
  - **Task**: Combines insights, use cases, and resources into a structured report.
  - **Output**: A polished markdown file with sections like Executive Summary, Research Insights, Proposed Use Cases, and Resource Links.

---

## Directory Structure

Here’s how the project is organized:

```
market-research-and-use-case-generator/
├── app.py                  # Main Streamlit application file
├── requirements.txt        # List of Python dependencies
└── proposals/              # Directory for generated markdown proposals
    ├── Apple_20250327_222441.md
    ├── Nvidia_20250327_010622.md
    └── Tesla_20250327_211020.md
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/bhaswanth67/market-research-and-use-case-generator.git
cd market-research-and-use-case-generator
```

### 2. Install Dependencies
Ensure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Obtain API keys for Gemini (language model) and Serper (web search). Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
```
Then load it in `app.py` with `load_dotenv()`.

### 4. Run the Application
Launch the Streamlit app:
```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` to access the interface.

---
