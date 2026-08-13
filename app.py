"""
ResearchMind — Multi-agent research pipeline UI
Streamlit front-end for the Search -> Read -> Write -> Critique pipeline.
"""

import streamlit as st

from agent import build_reader_agent, build_search_agent, critic_chain, writer_chain

# Page configuration

st.set_page_config(
    page_title="ResearchMind",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Design tokens + global styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
    --bg:#08080b;
    --bg-elevated:#0d0d11;
    --surface:#131316;
    --surface-hover:#18181d;
    --border:#232328;
    --border-strong:#34343c;
    --text-primary:#f2f1ed;
    --text-secondary:#8e8e96;
    --text-tertiary:#54545c;
    --accent:#ff5e1a;
    --accent-2:#ffb067;
    --accent-dim:rgba(255,94,26,.10);
    --accent-border:rgba(255,94,26,.35);
    --mono:'JetBrains Mono', monospace;
    --sans:'Inter', sans-serif;
    --display:'Sora', sans-serif;
}

/* ---------- reset streamlit chrome ---------- */
#MainMenu, header[data-testid="stHeader"], footer{ visibility:hidden; height:0; }
html{ -webkit-text-size-adjust:100%; }
.block-container{
    padding-top: clamp(1.5rem, 4vw, 2.5rem);
    padding-bottom: clamp(2rem, 6vw, 4rem);
    padding-left: clamp(1rem, 4vw, 1.5rem);
    padding-right: clamp(1rem, 4vw, 1.5rem);
    max-width:1120px;
}
.stApp{
    background:
        radial-gradient(ellipse 900px 520px at 50% -10%, var(--accent-dim), transparent 60%),
        repeating-linear-gradient(0deg, rgba(255,255,255,.014) 0px, rgba(255,255,255,.014) 1px, transparent 1px, transparent 42px),
        repeating-linear-gradient(90deg, rgba(255,255,255,.014) 0px, rgba(255,255,255,.014) 1px, transparent 1px, transparent 42px),
        var(--bg);
    font-family: var(--sans);
    color: var(--text-primary);
    overflow-x:hidden;
}
* { scrollbar-width: thin; scrollbar-color: var(--border-strong) transparent; box-sizing:border-box; }
::-webkit-scrollbar{ width:8px; height:8px; }
::-webkit-scrollbar-thumb{ background:var(--border-strong); border-radius:8px; }

/* focus visibility for accessibility */
a:focus-visible, button:focus-visible, input:focus-visible{
    outline: 2px solid var(--accent) !important;
    outline-offset: 2px;
}

/* ---------- hero ---------- */
.st-key-hero{ text-align:center; padding: clamp(12px,3vw,20px) 0 clamp(32px,6vw,52px); }
.eyebrow{
    display:inline-flex; align-items:center; gap:8px;
    font-family: var(--mono); font-size:clamp(10px,1.6vw,11px); letter-spacing:.22em;
    color: var(--accent); font-weight:600; text-transform:uppercase;
    margin-bottom:clamp(14px,3vw,22px);
}
.eyebrow::before{
    content:""; width:6px; height:6px; border-radius:50%; flex-shrink:0;
    background:var(--accent); box-shadow:0 0 0 3px var(--accent-dim);
}
.hero-title{
    font-family:var(--display); font-weight:800; letter-spacing:-.025em;
    font-size:clamp(42px, 8.5vw, 96px) !important; line-height:0.98 !important; margin:0;
    word-break:break-word;
}
.hero-title .dim{ color:var(--text-primary); }
.hero-title .accent{
    background:linear-gradient(120deg, var(--accent) 15%, var(--accent-2) 100%);
    -webkit-background-clip:text; background-clip:text; color:transparent;
}
.hero-sub{
    max-width:600px; margin:clamp(16px,3vw,24px) auto 0; color:var(--text-secondary);
    font-size:clamp(14.5px, 2vw, 17px); line-height:1.65; font-weight:400;
    padding:0 8px;
}
.hero-rule{
    width:100%; max-width:220px; height:1px; margin:clamp(26px,5vw,40px) auto 0;
    background:linear-gradient(90deg, transparent, var(--border-strong), transparent);
}

/* ---------- cards (targeted via st.container(key=...)) ---------- */
.st-key-input_card, .st-key-pipeline_card, .st-key-results_card{
    background:var(--surface);
    border:1px solid var(--border);
    border-radius:16px;
    padding: 8px clamp(18px,3.5vw,28px) clamp(20px,3.5vw,28px);
    transition: border-color .2s ease;
}
.card-label{
    font-family:var(--mono); font-size:10.5px; letter-spacing:.16em;
    color:var(--text-tertiary); text-transform:uppercase; font-weight:600;
    margin: 18px 0 10px;
}

/* ---------- inputs ---------- */
div[data-testid="stTextInput"] input{
    background:var(--bg-elevated) !important;
    border:1px solid var(--border) !important;
    border-radius:9px !important;
    color:var(--text-primary) !important;
    font-family:var(--sans) !important;
    font-size:16px !important;
    padding:13px 14px !important;
    transition: border-color .15s ease, box-shadow .15s ease;
}
div[data-testid="stTextInput"] input:focus{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-dim) !important;
}
div[data-testid="stTextInput"] input::placeholder{ color:var(--text-tertiary) !important; }

/* ---------- primary run button ---------- */
.st-key-run_btn button{
    width:100%;
    min-height:46px;
    background: linear-gradient(120deg, var(--accent), #ff7a3d) !important;
    color:#0a0a0a !important;
    border:none !important;
    border-radius:9px !important;
    font-family:var(--sans) !important;
    font-weight:700 !important;
    font-size:14.5px !important;
    padding:11px 0 !important;
    letter-spacing:.01em;
    box-shadow: 0 1px 0 rgba(255,255,255,.15) inset, 0 8px 22px -8px rgba(255,94,26,.55);
    transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
}
.st-key-run_btn button:hover{ filter:brightness(1.06); transform:translateY(-1px); }
.st-key-run_btn button:active{ transform:translateY(0px); }
.st-key-run_btn button p{ font-weight:700 !important; }

/* ---------- example chips ---------- */
.st-key-chips div[data-testid="stHorizontalBlock"]{ flex-wrap:wrap !important; row-gap:8px; }
.st-key-chips button{
    background:transparent !important;
    border:1px solid var(--border) !important;
    color:var(--text-secondary) !important;
    font-family:var(--sans) !important;
    font-size:12.5px !important;
    font-weight:500 !important;
    border-radius:7px !important;
    padding:7px 12px !important;
    min-height:36px;
    white-space:normal !important;
}
.st-key-chips button:hover{
    border-color:var(--accent-border) !important;
    color:var(--text-primary) !important;
    background:var(--accent-dim) !important;
}

/* ---------- pipeline stage rows ---------- */
.stage-row{
    display:flex; align-items:flex-start; gap:14px;
    padding:14px 4px; border-bottom:1px solid var(--border);
}
.stage-row:last-child{ border-bottom:none; }
.stage-num{
    font-family:var(--mono); font-size:12px; font-weight:600;
    color:var(--text-tertiary); padding-top:2px; width:20px; flex-shrink:0;
}
.stage-body{ flex:1; min-width:0; }
.stage-title{
    font-family:var(--sans); font-weight:600; font-size:14px;
    color:var(--text-primary); margin-bottom:2px;
    display:flex; align-items:center; justify-content:space-between; gap:10px;
    flex-wrap:wrap;
}
.stage-desc{ font-size:12.5px; color:var(--text-tertiary); line-height:1.4; }
.stage-status{ display:flex; align-items:center; gap:6px; flex-shrink:0; }
.status-label{
    font-family:var(--mono); font-size:10px; letter-spacing:.08em;
    text-transform:uppercase; font-weight:600;
}
.status-dot{ width:8px; height:8px; border-radius:50%; position:relative; flex-shrink:0; }

.stage-row.idle .status-dot{ background:transparent; border:1.5px solid var(--border-strong); }
.stage-row.idle .status-label{ color:var(--text-tertiary); }

.stage-row.running .status-dot{ background:var(--accent); animation: pulse 1.15s ease-in-out infinite; }
.stage-row.running .status-label{ color:var(--accent); }
.stage-row.running .stage-title{ color:var(--text-primary); }

.stage-row.done .status-dot{
    background:var(--accent); border:none;
}
.stage-row.done .status-dot::after{
    content:""; position:absolute; left:2px; top:2.5px;
    width:4px; height:2px; border-left:1.5px solid #0a0a0a; border-bottom:1.5px solid #0a0a0a;
    transform:rotate(-45deg);
}
.stage-row.done .status-label{ color:var(--text-secondary); }
.stage-row.done .stage-desc{ color:var(--text-tertiary); }

@keyframes pulse{
    0%,100%{ box-shadow:0 0 0 0 rgba(255,94,26,.5); }
    50%{ box-shadow:0 0 0 5px rgba(255,94,26,0); }
}
@media (prefers-reduced-motion: reduce){ .stage-row.running .status-dot{ animation:none; } }

/* ---------- results ---------- */
.st-key-results_card{ padding-top:22px; margin-top:36px; }
.results-head{
    display:flex; align-items:baseline; justify-content:space-between;
    margin-bottom:6px;
}
.results-title{ font-family:var(--display); font-weight:700; font-size:20px; }
.st-key-results_card div[data-testid="stMarkdownContainer"] h1{ font-family:var(--display); font-size:20px; margin-top:22px;}
.st-key-results_card div[data-testid="stMarkdownContainer"] h2{ font-family:var(--display); font-size:16px; color:var(--accent-2); margin-top:20px;}

.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--border); }
.stTabs [data-baseweb="tab"]{
    font-family:var(--sans); font-weight:600; font-size:13px; color:var(--text-tertiary);
    padding:8px 4px;
}
.stTabs [aria-selected="true"]{ color:var(--accent) !important; }
.stTabs [data-baseweb="tab-highlight"]{ background-color:var(--accent) !important; }

/* download button */
.stDownloadButton button{
    background:var(--bg-elevated) !important; border:1px solid var(--border) !important;
    color:var(--text-secondary) !important; font-family:var(--sans) !important;
    font-size:12.5px !important; font-weight:600 !important; border-radius:8px !important;
}
.stDownloadButton button:hover{ border-color:var(--accent-border) !important; color:var(--text-primary) !important; }

/* footer */
.footer{
    text-align:center; margin-top:56px; padding-top:22px;
    border-top:1px solid var(--border);
    font-family:var(--mono); font-size:11px; color:var(--text-tertiary);
    letter-spacing:.04em;
}

/* generic column gap tightening */
div[data-testid="stHorizontalBlock"]{ gap:22px; }

/* results markdown fluid sizing */
div[data-testid="stMarkdownContainer"]{ font-size:clamp(13.5px, 1.6vw, 15px); line-height:1.7; }
.st-key-results_card div[data-testid="stMarkdownContainer"] h1{ font-size:clamp(17px,2.4vw,20px); }
.st-key-results_card div[data-testid="stMarkdownContainer"] h2{ font-size:clamp(14.5px,2vw,16px); }

/* ================= MOBILE BREAKPOINTS ================= */
@media (max-width: 900px){
    /* Streamlit stacks columns automatically below this width;
       give the two cards breathing room once stacked. */
    div[data-testid="stHorizontalBlock"]{ flex-wrap:wrap !important; }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]{
        width:100% !important; flex:1 1 100% !important; min-width:100% !important;
    }
    .st-key-pipeline_card{ margin-top:18px; }
}

@media (max-width: 640px){
    .st-key-hero{ text-align:left; padding-top:8px; }
    .hero-sub{ margin-left:0; padding:0; }
    .hero-rule{ margin-left:0; }
    .card-label{ margin-top:14px; }
    .st-key-input_card, .st-key-pipeline_card, .st-key-results_card{
        padding-left:18px; padding-right:18px; border-radius:14px;
    }
    .stage-row{ gap:10px; }
    .results-head{ flex-direction:column; align-items:flex-start; gap:4px; }
}

@media (max-width: 400px){
    .eyebrow{ font-size:9.5px; letter-spacing:.14em; }
    .hero-title{ font-size:clamp(34px, 11vw, 44px); }
}
</style>
""",
    unsafe_allow_html=True,
)

# Session state
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "report" not in st.session_state:
    st.session_state.report = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None

PIPELINE_STAGES = [
    ("01", "Search Agent", "Gathers recent web information"),
    ("02", "Reader Agent", "Scrapes and extracts deep content"),
    ("03", "Writer Chain", "Drafts the full research report"),
    ("04", "Critic Chain", "Reviews and scores the report"),
]

EXAMPLE_TOPICS = [
    "LLM agents 2025",
    "CRISPR gene editing",
    "Fusion energy progress",
]


def set_topic(value: str) -> None:
    st.session_state.topic = value


def stage_html(num: str, title: str, desc: str, status: str) -> str:
    label = {"idle": "Waiting", "running": "Running", "done": "Complete"}[status]
    return f"""
    <div class="stage-row {status}">
        <div class="stage-num">{num}</div>
        <div class="stage-body">
            <div class="stage-title">
                <span>{title}</span>
                <span class="stage-status">
                    <span class="status-label">{label}</span>
                    <span class="status-dot"></span>
                </span>
            </div>
            <div class="stage-desc">{desc}</div>
        </div>
    </div>
    """


# Hero
with st.container(key="hero"):
    st.markdown(
        """
        <div class="eyebrow">Multi-agent AI system</div>
        <h1 class="hero-title"><span class="dim">Research</span><span class="accent">Mind</span></h1>
        <p class="hero-sub">
            Four specialized AI agents collaborate — searching, scraping, writing, and
            critiquing — to deliver a polished research report on any topic.
        </p>
        <div class="hero-rule"></div>
        """,
        unsafe_allow_html=True,
    )

# Main grid: input card (left) + pipeline card (right)

left, right = st.columns([1.15, 1], gap="medium")

with left:
    with st.container(key="input_card"):
        st.markdown('<div class="card-label">Research Topic</div>', unsafe_allow_html=True)
        st.text_input(
            "Research topic",
            key="topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            label_visibility="collapsed",
        )

        with st.container(key="run_btn"):
            run_clicked = st.button("Run Research Pipeline", type="primary", use_container_width=True)

        st.markdown('<div class="card-label" style="margin-top:20px;">Try</div>', unsafe_allow_html=True)
        with st.container(key="chips"):
            chip_cols = st.columns(len(EXAMPLE_TOPICS))
            for c, ex in zip(chip_cols, EXAMPLE_TOPICS):
                with c:
                    st.button(ex, key=f"chip_{ex}", on_click=set_topic, args=(ex,), use_container_width=True)

with right:
    with st.container(key="pipeline_card"):
        st.markdown('<div class="card-label">Pipeline</div>', unsafe_allow_html=True)
        stage_slots = [st.empty() for _ in PIPELINE_STAGES]
        for slot, (num, title, desc) in zip(stage_slots, PIPELINE_STAGES):
            slot.markdown(stage_html(num, title, desc, "idle"), unsafe_allow_html=True)

# Pipeline execution
if run_clicked:
    topic = st.session_state.topic.strip()
    if not topic:
        st.warning("Enter a research topic before running the pipeline.")
    else:
        try:
            state = {}

            stage_slots[0].markdown(stage_html(*PIPELINE_STAGES[0], "running"), unsafe_allow_html=True)
            search_agent = build_search_agent()
            search_response = search_agent.invoke(
                {"input": f"Perform deep, comprehensive research on: {topic}"}
            )
            state["search_results"] = search_response["output"]
            stage_slots[0].markdown(stage_html(*PIPELINE_STAGES[0], "done"), unsafe_allow_html=True)

            stage_slots[1].markdown(stage_html(*PIPELINE_STAGES[1], "running"), unsafe_allow_html=True)
            reader_agent = build_reader_agent()
            reader_response = reader_agent.invoke(
                {
                    "input": (
                        f"Review these search results for query: '{topic}'. "
                        f"Select the single most authoritative article URL and scrape it using `scrape_url`.\n\n"
                        f"Search Data:\n{state['search_results']}"
                    )
                }
            )
            state["scraped_content"] = reader_response["output"]
            stage_slots[1].markdown(stage_html(*PIPELINE_STAGES[1], "done"), unsafe_allow_html=True)

            stage_slots[2].markdown(stage_html(*PIPELINE_STAGES[2], "running"), unsafe_allow_html=True)
            combined_research = (
                f"=== SEARCH RESULTS ===\n{state['search_results']}\n\n"
                f"=== DEEP SCRAPED CONTENT ===\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": combined_research})
            stage_slots[2].markdown(stage_html(*PIPELINE_STAGES[2], "done"), unsafe_allow_html=True)

            stage_slots[3].markdown(stage_html(*PIPELINE_STAGES[3], "running"), unsafe_allow_html=True)
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            stage_slots[3].markdown(stage_html(*PIPELINE_STAGES[3], "done"), unsafe_allow_html=True)

            st.session_state.report = state["report"]
            st.session_state.feedback = state["feedback"]

        except Exception as exc:
            st.error(f"Pipeline failed: {exc}")

# Results
if st.session_state.report:
    with st.container(key="results_card"):
        st.markdown(
            '<div class="results-head"><span class="results-title">Research Output</span></div>',
            unsafe_allow_html=True,
        )
        tab_report, tab_critic = st.tabs(["Report", "Critic Review"])
        with tab_report:
            st.markdown(st.session_state.report)
            st.download_button(
                "Download report (.md)",
                data=st.session_state.report,
                file_name="research_report.md",
                mime="text/markdown",
            )
        with tab_critic:
            st.markdown(st.session_state.feedback)

# Footer
st.markdown(
    '<div class="footer">RESEARCHMIND — POWERED BY LANGCHAIN MULTI-AGENT PIPELINE</div>',
    unsafe_allow_html=True,
)