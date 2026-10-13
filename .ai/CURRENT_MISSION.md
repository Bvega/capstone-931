# Current Mission

## Objective

Create and validate the smallest runnable CAP 931 sales research prototype.

## Allowed scope

- Streamlit input form and report display/download.
- Three sequential agent roles over the OpenAI Responses API.
- Optional local text extraction for supported product overview files.
- Input validation and offline tests.
- Setup and project documentation.

## Acceptance criteria

- App starts with `uv run streamlit run app.py`.
- API key is read from local environment and never included in source.
- Missing inputs and unsafe URLs are rejected clearly.
- With valid API access, the pipeline invokes research, analysis, and brief-writing roles in order.
- Source links are shown with the output and included in downloads.
- `uv run pytest` passes without an API key or network.
- No commit or deployment occurs without user review.

