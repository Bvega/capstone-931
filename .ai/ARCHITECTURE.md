# Architecture

Single local Streamlit app; Python; OpenAI Responses API; one configurable model assigned three explicit sequential roles.

1. Research Agent uses web search and returns notes plus source annotations.
2. Account Analyst Agent turns those notes into evidence-versus-inference analysis.
3. Brief Writer Agent creates the concise account brief.

The app validates user-entered public URLs, optionally extracts text from a product overview, renders the brief, and provides Markdown/PDF downloads. The app does not fetch user URLs directly or persist prospect inputs. Tests do not require network access or an API key.

