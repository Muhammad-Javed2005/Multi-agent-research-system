# Multi-Agent ResearchMind

> An autonomous AI-powered research system that performs live web research, analyzes information from multiple sources, critiques the findings, and generates detailed, structured research content.

## Overview

**Multi-Agent ResearchMind** is a Streamlit-based multi-agent research application designed for deep and up-to-date topic research.

Instead of relying only on an LLM's existing knowledge, the system connects AI agents with live web search to collect current information, analyze relevant sources, evaluate the research, and produce a comprehensive final response.

The project demonstrates how **LLMs, web search, custom tools, and multi-agent workflows** can be combined to build an autonomous research assistant.

## What It Does

Given a research topic or question, the system can:

- Perform live web searches for current information
- Collect and process relevant web content
- Analyze information using specialized AI agents
- Synthesize findings from multiple sources
- Critically review the research for gaps or weaknesses
- Generate a detailed and organized final research response

## How the System Works

The system is organized as a research pipeline rather than a single LLM call.

```text
                    ┌─────────────────────┐
                    │     User Query      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Research Pipeline  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │  Search Agent   │         │  Reader Agent   │
        │                 │         │                 │
        │ Live Web Search │         │ Source Analysis │
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Research Synthesis │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Critic Chain     │
                    │                     │
                    │ Quality Evaluation  │
                    │ Missing Information │
                    │ Weak Evidence       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Writer Chain     │
                    │                     │
                    │    Final Report     │
                    │  Structured Output  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   ResearchMind UI   │
                    │                     │
                    │  Final Deep Report  │
                    └─────────────────────┘
```

## Multi-Agent Architecture

The research process is divided into specialized components.

### Search Agent

Finds relevant and current information from the web using the integrated search tools.

### Reader Agent

Reads and processes retrieved information to identify useful facts, context, and research material.

### Critic Chain

Reviews the collected research, identifies missing information or weak areas, and helps improve the quality of the final result.

### Writer Chain

Organizes the processed research into a clear, detailed, and structured final response.

## Custom Tools

The project includes custom tools that extend the capabilities of the research agents.

These tools allow the system to interact with external information sources and support the research pipeline beyond basic LLM generation.

## Key Features

- Live web research
- Multi-agent AI workflow
- Current information retrieval
- Source analysis and synthesis
- Research quality evaluation
- Detailed content generation
- Custom agent tools
- Streamlit web interface
- Mistral AI integration
- Tavily search integration

## Technology Stack

- Python
- Streamlit
- LangChain
- Mistral AI
- Tavily
- BeautifulSoup
- Requests
- python-dotenv

## Project Structure

```text
multi-agent-research-system/
|
├── app.py
├── agent.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .streamlit/
├── devcontainer/
└── README.md
```

### Main Components

**app.py**  
Main Streamlit application and user interface.

**agent.py**  
Contains the research agents and chains, including the Search Agent, Reader Agent, Critic Chain, and Writer Chain.

**pipeline.py**  
Coordinates the overall research workflow.

**tools.py**  
Contains custom tools used by the research system.

**requirements.txt**  
Contains the project's Python dependencies.

## How It Works in Practice

The system combines two important capabilities.

**Live Information Retrieval**  
Tavily is used to search the web for current and relevant information.

**AI Research and Generation**  
Mistral AI and LangChain components process the retrieved information through the multi-agent pipeline and generate the final research content.

This combination allows the application to research topics using fresh web information rather than depending only on pre-existing model knowledge.

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Muhammad-Javed2005/multi-agent-research-system.git
cd multi-agent-research-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Run the application:

```bash
streamlit run app.py
```

## Deployment

The project is deployed using Streamlit Community Cloud.

**Live Testing / Demo:**  
https://javed-researchmind.streamlit.app/

The deployed application requires the appropriate API credentials to be configured through Streamlit Secrets.

## Security

API keys should never be committed to the repository.

For local development, use `.env`.

For Streamlit deployment, configure the required credentials through Streamlit Secrets.

## Future Improvements

- Improved source verification
- Automatic citation generation
- More specialized research agents
- Research history and memory
- Additional search and data tools
- PDF or DOCX research report export
- Advanced parallel research workflows

## Author

**Engr. Muhammad Javed**

Software Engineering Student | AI & Data Science Enthusiast

Interested in Artificial Intelligence, Machine Learning, Data Science, NLP, Generative AI, Agentic AI, and Software Engineering.

## License

This project is available for educational and research purposes.

---

**Multi-Agent ResearchMind** — an AI-powered system for live web research, multi-agent analysis, and detailed content generation.

