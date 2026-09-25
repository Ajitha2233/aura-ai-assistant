import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="AURA AI Assistant", page_icon="✨", layout="wide")

# ---------------------------------------------------------------------------
# Content: role-based experts, prompt library, workflows
# (mirrors the Project AURA documentation)
# ---------------------------------------------------------------------------
ROLE_PROMPTS = {
    "Free Chat": None,
    "🎯 Marketing Expert": (
        "You are a senior marketing strategist with 15 years of experience across "
        "B2B and B2C brands. When the user describes a product, audience, or goal, "
        "respond with: (1) a clear positioning angle, (2) 2-3 campaign or content "
        "ideas suited to their stated channel and budget, (3) one measurable success "
        "metric per idea. Be specific and practical - avoid generic advice like "
        "'post more on social media.' Ask one clarifying question only if the "
        "audience or goal is missing."
    ),
    "🚀 Founder Advisor": (
        "You are an experienced startup advisor who has coached early-stage founders "
        "through fundraising, hiring, and go-to-market decisions. When the user brings "
        "a business question or decision, respond with: (1) the key trade-offs at "
        "stake, (2) a recommendation with reasoning, (3) the biggest risk to watch. "
        "Be direct and pragmatic, favor decisions that preserve runway and focus, and "
        "flag when a decision needs data the user hasn't provided yet."
    ),
    "🔍 Research Specialist": (
        "You are a research analyst who produces concise, well-organized briefs. For "
        "any research request, structure your answer as: a one-line summary, 3-6 key "
        "findings as bullet points, and (if sources are available) a short source "
        "list. Distinguish clearly between verified facts and your own inference. "
        "Never present an estimate as a confirmed figure."
    ),
    "📊 Data Analyst": (
        "You are a data analyst who turns raw numbers into decisions. When given "
        "data (pasted figures, a table, or a description of a dataset), identify the "
        "2-3 most important trends, call out any outliers or data-quality concerns, "
        "and end with one concrete, actionable recommendation. Use plain language "
        "over jargon, and state your assumptions explicitly when the data is "
        "incomplete."
    ),
}

WORKFLOW_PROMPTS = {
    "🏢 Competitor Research Workflow": (
        "You are running a Competitor Research workflow. Given the competitor(s) and "
        "context the user provides, respond with: (1) a table with columns "
        "Competitor | Offer summary | Strengths | Weaknesses | Notes, (2) a line "
        "starting 'Key gap identified:', (3) 2-3 bullet 'Recommended actions'."
    ),
    "📰 Article Summarization Workflow": (
        "You are running an Article Summarization workflow. Given the article text "
        "or topic the user provides, respond with: a one-line summary, then 3-5 "
        "bullet 'Key points', then a 1-2 sentence 'Why it matters', then a 'Source' "
        "line if one is available."
    ),
    "📈 Market Trend Analysis Workflow": (
        "You are running a Market Trend Analysis workflow. Given the industry/market "
        "the user names, respond with: a table of Trend | Direction "
        "(rising/stable/declining) | Why it matters, then a 'Opportunities to watch' "
        "section, then a short 'Outlook' with an explicit caveat that this is "
        "directional, not a guarantee."
    ),
}

PROMPT_LIBRARY = {
    "✍️ Writing": {
        "Professional email": (
            "Write a formal email to [recipient/role] about [topic]. The goal is to "
            "[request approval / follow up / deliver bad news]. Keep it under 150 "
            "words and end with a clear next step."
        ),
        "Content draft": (
            "Write a blog post about [topic] for an audience of [audience]. Tone: "
            "professional. Include a strong opening line and 3 concrete points. "
            "Length: 300-500 words."
        ),
        "Rewrite & tone adjustment": (
            "Rewrite the following text to be more concise and persuasive while "
            "keeping every factual detail unchanged: [paste text]. Return only the "
            "rewritten version."
        ),
    },
    "🔎 Research": {
        "Topic research brief": (
            "Research [topic] and summarize the 5 most important facts or "
            "developments as of today. For each point, note why it matters and, if "
            "possible, the source. Present as a short bulleted brief."
        ),
        "Company/product research": (
            "Research [company/product name]. Summarize what it does, who it's for, "
            "pricing model (if public), and 2-3 notable strengths or weaknesses. "
            "Keep it factual and cite sources where available."
        ),
        "Fact-check": (
            "Verify the following claim and tell me if it's accurate, partly "
            "accurate, or false, with the reasoning and sources: [claim]. Flag "
            "anything you're not confident about."
        ),
    },
    "📊 Analysis": {
        "Data/trend analysis": (
            "Here is a dataset or set of figures: [paste data]. Identify the 3 most "
            "important trends or patterns, note any anomalies, and suggest one "
            "action based on the data."
        ),
        "Comparison / decision matrix": (
            "Compare these options - [option A, option B, option C] - on "
            "[criteria: cost, quality, speed, risk]. Present as a table and "
            "recommend one option with a one-line reason."
        ),
    },
    "✅ Productivity": {
        "Meeting notes → action items": (
            "Turn these raw meeting notes into a clean summary with: (1) key "
            "decisions, (2) action items with owner and due date if mentioned, "
            "(3) open questions. Notes: [paste notes]."
        ),
        "Daily/weekly prioritization": (
            "Here is my task list for this week: [paste tasks]. Group them by "
            "priority (urgent/important/later), flag anything that looks unrealistic "
            "for the time available, and suggest an order to tackle them."
        ),
    },
}

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""
if "mode" not in st.session_state:
    st.session_state.mode = "Free Chat"


def set_prompt(text: str):
    st.session_state.user_prompt = text


# ---------------------------------------------------------------------------
# Sidebar: mode selector
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### MODE")
    mode = st.radio(
        "Choose how AURA should respond",
        list(ROLE_PROMPTS.keys()) + list(WORKFLOW_PROMPTS.keys()),
        label_visibility="collapsed",
    )
    st.session_state.mode = mode

    st.markdown("---")
    st.markdown("### PROMPT LIBRARY")
    for category, prompts in PROMPT_LIBRARY.items():
        with st.expander(category):
            for label, text in prompts.items():
                if st.button(label, key=f"lib_{label}", use_container_width=True):
                    set_prompt(text)

# ---------------------------------------------------------------------------
# Main panel
# ---------------------------------------------------------------------------
st.title("✨ AURA AI Assistant")
st.subheader("Think • Research • Create • Organize")
st.caption(f"Mode: **{st.session_state.mode}**")

prompt = st.text_area(
    "What would you like AURA to help with?",
    value=st.session_state.user_prompt,
    key="user_prompt",
    placeholder="Example: Explain artificial intelligence in simple terms.",
    height=160,
)

if st.button("✨ Generate Response", type="primary"):
    if prompt:
        system_prompt = ROLE_PROMPTS.get(st.session_state.mode) or WORKFLOW_PROMPTS.get(
            st.session_state.mode
        )

        with st.spinner("AURA is thinking..."):
            try:
                config = (
                    types.GenerateContentConfig(system_instruction=system_prompt)
                    if system_prompt
                    else None
                )
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                    config=config,
                )
                st.markdown("### 🤖 AURA Response")
                st.write(response.text)

            except Exception as e:
                if "503" in str(e):
                    st.warning(
                        "Gemini is temporarily busy. "
                        "Please wait a few seconds and try again."
                    )
                else:
                    st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a request first.")
