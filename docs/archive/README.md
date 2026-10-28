# CAP 931 Sales Agent Prototype

A small Streamlit application that researches a prospective account and creates a source-linked sales brief through three sequential GPT agent roles: Research, Account Analyst, and Brief Writer.

## Requirements

- Python 3.11 or newer
- `uv`
- An OpenAI API key with access to a model that supports the Responses API and web search
- VS Code with Claude Code or Codex extension

The app uses one configurable model for the three roles. Each role has a separate prompt and bounded output. The Research Agent uses OpenAI web search; the later agents work only from the research packet and its source list. API calls happen only after the user submits the form.

## Run in VS Code

1. Open this folder in VS Code.
2. In the integrated terminal, run:

   ```bash
   uv sync
   cp .env.example .env
   ```

3. Open `.env` in VS Code and set `OPENAI_API_KEY` to your own key. Do not share the key or commit `.env`.
4. Start the app:

   ```bash
   uv run streamlit run app.py
   ```

5. Open the local URL printed in the terminal, enter account details, and submit once to run the agents.

To run the offline tests without an API key:

```bash
uv run pytest
```

## Inputs

- Product name, category, and value proposition
- Prospect company name and public URL
- Competitor URLs
- Target contact (optional)
- Product overview file (optional `.txt`, `.md`, `.pdf`, or `.docx`, up to 5 MB)

The URLs are sent to the model as research targets. The app does not directly fetch arbitrary URLs from the server.

## Output

The app displays a compact account brief and source list, then offers Markdown and PDF downloads. Facts that cannot be supported by the research packet should be labeled unknown or omitted. The report includes a research date and source links.

## Current scope

This is a bounded capstone prototype. It does not send alerts, deploy publicly, or store prospect data. It does not guarantee that every requested URL is indexed by web search. Check source links and verify claims before using the brief with a customer.

## Project evidence

Capture screenshots during the work, not only at the end: environment setup, completed input form, generated report with source links, and download output. The supplied report template asks for screenshots in its Steps section.

See `.ai/` for project rules, architecture, mission, and decisions. The original assignment and report template are in `docs/reference/`.

