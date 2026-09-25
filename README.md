# ✨ AURA AI Assistant

**Think • Research • Create • Organize**

AURA is a personal AI work assistant built with [Streamlit](https://streamlit.io) and [Google Gemini](https://ai.google.dev/). It replaces the daily habit of switching between a blank document, a search engine, a spreadsheet, and a to-do list by handling four recurring job categories in one place: writing, research, analysis, and productivity.

## Features

- **Single-prompt chat core** — a Gemini-powered text box that answers any free-form request.
- **Role-based expert personas** — switch AURA's tone and reasoning with one click:
  - 🎯 Marketing Expert
  - 🚀 Founder Advisor
  - 🔍 Research Specialist
  - 📊 Data Analyst
- **Structured research workflows**:
  - 🏢 Competitor Research
  - 📰 Article Summarization
  - 📈 Market Trend Analysis
- **10-prompt starter library** — one-click templates across Writing, Research, Analysis, and Productivity so you're never starting from a blank box.
- **Friendly error handling** — empty-input warnings and graceful messages if the Gemini API is temporarily busy.

## Target users

Business professionals who produce a high volume of written and analytical work under deadline — project managers, procurement/coordination roles, small-business owners, marketers, researchers, and students.

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/aura-ai-assistant.git
cd aura-ai-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Copy `.env.example` to `.env` and add your key (get one from [Google AI Studio](https://aistudio.google.com/apikey)):

```bash
cp .env.example .env
```

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Project structure

```
aura-ai-assistant/
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
├── .env.example        # Template for your API key
├── .gitignore
└── README.md
```

## How it works

Selecting a role or workflow from the sidebar doesn't change the interface — it changes the **system instruction** sent to Gemini alongside your prompt. The chat box and Generate button stay identical across every mode, so the tool stays simple even as its capability grows.

## Roadmap

- [ ] Save/reuse prompt & response history
- [ ] Real web-grounded research (current version relies on the model's own knowledge)
- [ ] Export responses to Word/PDF
- [ ] Expanded error handling (invalid key, network timeout)

## License

MIT
