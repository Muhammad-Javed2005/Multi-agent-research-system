from agent import build_reader_agent, build_search_agent, critic_chain, writer_chain


def run_research_pipeline(user_prompt: str) -> dict:
    state = {}

    print("\n" + "=" * 65)
    print(f"  STARTING AGENTIC RESEARCH PIPELINE")
    print(f"  Prompt: {user_prompt}")
    print("=" * 65)

    # ----------------------------------------------------
    # STEP 1: Search Agent
    # ----------------------------------------------------
    print("\n[AGENT 1/4]  Search Agent: Querying Web & Collecting Intelligence...")
    search_agent = build_search_agent()
    
    search_response = search_agent.invoke({
        "input": f"Perform deep, comprehensive research on: {user_prompt}"
    })
    
    state["search_results"] = search_response["output"]
    print("\n✓ Search Phase Complete. Extracted snippets and links.")

    # ----------------------------------------------------
    # STEP 2: Reader Agent
    # ----------------------------------------------------
    print("\n[AGENT 2/4]  Reader Agent: Selecting Best Source & Extracting Deep Data...")
    reader_agent = build_reader_agent()
    
    reader_response = reader_agent.invoke({
        "input": (
            f"Review these search results for query: '{user_prompt}'. "
            f"Select the single most authoritative article URL and scrape it using `scrape_url`.\n\n"
            f"Search Data:\n{state['search_results']}"
        )
    })
    
    state["scraped_content"] = reader_response["output"]
    print("\n✓ Scraping Phase Complete. Deep content extracted.")

    # ----------------------------------------------------
    # STEP 3: Writer Chain
    # ----------------------------------------------------
    print("\n[AGENT 3/4]   Writer Chain: Synthesizing & Drafting Structured Report...")
    
    combined_research = (
        f"=== SEARCH RESULTS ===\n{state['search_results']}\n\n"
        f"=== DEEP SCRAPED CONTENT ===\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": user_prompt,
        "research": combined_research
    })
    print("\n✓ Draft Generated Successfully.")

    # ----------------------------------------------------
    # STEP 4: Critic Chain
    # ----------------------------------------------------
    print("\n[AGENT 4/4]  Critic Chain: Reviewing and Grading Report Quality...")
    
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })
    print("\n✓ Evaluation Completed.")

    # ----------------------------------------------------
    # FINAL DISPLAY
    # ----------------------------------------------------
    print("\n" + "=" * 65)
    print("  FINAL RESEARCH REPORT ")
    print("=" * 65 + "\n")
    print(state["report"])

    print("\n" + "=" * 65)
    print("🔍 CRITIC AUDIT & FEEDBACK ")
    print("=" * 65 + "\n")
    print(state["feedback"])

    return state


if __name__ == "__main__":
    print("\n" + " MULTI-AGENT RESEARCH SYSTEM INITIALIZED".center(65))
    print("-" * 65)
    
    user_query = input("\n Enter your research prompt: ")
    
    if user_query.strip():
        run_research_pipeline(user_query.strip())
    else:
        print(" Error: Prompt cannot be empty.")