# Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-10-12 | Use VS Code, Claude Code as primary builder, and ChatGPT/Codex for architecture and validation. | Matches the established project workflow. |
| 2026-10-12 | Use a single local Streamlit app and three sequential agent roles. | Satisfies the multi-agent prototype while keeping a two-day capstone manageable. |
| 2026-10-12 | Use OpenAI Responses API web search; make model configurable and default to `gpt-6-luna`. | Provides current source-backed web research with a cost-sensitive model option; confirm API access and pricing before live runs. |
| 2026-10-12 | No database, alerts, deployment, or automatic API calls on app load. | Keeps the MVP bounded and avoids unnecessary data retention or spend. |

