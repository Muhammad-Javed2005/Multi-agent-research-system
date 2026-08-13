import os
from dotenv import load_dotenv

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

from tools import scrape_url, web_search

load_dotenv()

# Model Setup
LLM = ChatMistralAI(model="mistral-small-2506", temperature=0.2)


# ==========================================
# 1. Tool-Calling Search Agent
# ==========================================
def build_search_agent():
    tools = [web_search]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an elite Intelligence Search Specialist. Your task is to query the web using `web_search`, "
                "extract authoritative insights, accurate statistics, news context, and identify exact source URLs.",
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(LLM, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


# ==========================================
# 2. Tool-Calling Reader Agent
# ==========================================
def build_reader_agent():
    tools = [scrape_url]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Technical Content Extraction Agent. Examine search results, select the most informative URL, "
                "use `scrape_url`, and extract granular data, key facts, timelines, and technical details.",
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(LLM, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)


# ==========================================
# 3. Writer Chain
# ==========================================
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Lead Strategic Research Analyst. Synthesize raw search data and scraped findings into a highly authoritative, structured, and deep research report.",
        ),
        (
            "human",
            """Produce a comprehensive, detailed research report on the prompt below.

### User Research Prompt:
{topic}

### Gathered Intelligence Data:
{research}

---

### Formatting Specifications:
Structure the report cleanly in Markdown:

# Executive Summary
- Brief 3-4 sentence core overview.

# Deep Background & Context
- Historical context, key drivers, and recent developments.

# Key Findings & Impacts (Minimum 4 Detailed Points)
- Detailed analytical points explaining direct/indirect consequences, sector impacts, or economic/technical disruptions.

# Industry / Market Analysis
- Structural, economic, infrastructure, or operational implications.

# Conclusion & Future Outlook
- Strategic takeaways and predictions.

# Verified Sources
- List all extracted URLs clearly with bullet points.

*Ensure maximum detail, objectivity, zero fabrication, and strict adherence to facts.*""",
        ),
    ]
)

writer_chain = writer_prompt | LLM | StrOutputParser()


# ==========================================
# 4. Critic Chain
# ==========================================
critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Senior Editor and Fact Checker. Strictly critique the report for accuracy, depth, logical cohesion, and formatting.",
        ),
        (
            "human",
            """Review and grade the research report below.

### Draft Report:
{report}

---

### Output Format:
**Overall Quality Score:** [X/10]

### Strengths:
- ...

### Areas for Improvement:
- ...

### Final Summary Assessment:
- [One-line professional evaluation]""",
        ),
    ]
)

critic_chain = critic_prompt | LLM | StrOutputParser()