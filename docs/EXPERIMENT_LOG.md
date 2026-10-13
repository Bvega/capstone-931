# Prompt and Workflow Experiment Log

This log compares two completed account-research runs. The experiment changed the competitor inputs while keeping the product, prospect, model, and three-role workflow the same. It evaluates input relevance, not prompt quality: the exact prompt text and application commit were not recorded.

Ratings are retrospective qualitative assessments of the generated briefs, not benchmark measurements. Scale: 1 = low, 5 = high.

| Run | Date | Version | Account inputs | Research prompt | Analysis/writer prompt | Sources returned | Relevance (1-5) | Grounding (1-5) | Missing/unsupported claims | Changes for next run |
|---|---|---|---|---|---|---|---:|---:|---|---|
| 1 | 2026-10-12 | Three-role workflow; model gpt-6-luna; app commit not recorded | Wooden baseball bats for Target Corporation; competitor references Snowflake and Databricks; no contact or product overview | Default Research Agent prompt; exact text/version not captured | Default Account Analyst and Brief Writer prompts; exact text/version not captured | Target strategy, earnings-call material, wooden-bat listings, and leadership/technology sources | 2 | 4 | Competitor references were technology companies and did not match baseball bats. The “best wooden bat” value claim was unsubstantiated. No category buyer was identified. The suggested sales-angle sentence ended abruptly. | Replace technology competitors with baseball-bat brands and review the report for completeness. |
| 2 | 2026-10-12 | Three-role workflow; model gpt-6-luna; app commit not recorded | Same product and Target prospect; competitor references Marucci, Mizuno, and Victus; no contact or product overview | Default Research Agent prompt; exact text/version not captured | Default Account Analyst and Brief Writer prompts; exact text/version not captured | Target strategy, wooden-bat and Victus listings, annual-report material, and leadership pages | 4 | 4 | No category buyer or evidence that Target prioritizes wooden bats was found. The “best wooden bat” claim remained unsubstantiated. Retail listings do not establish a strategic competitor relationship; the Victus listing was sold by a third party. | Verify sources and product claims, investigate buyer requirements, and complete the planned single-pass baseline before making claims about the three-role workflow's comparative advantage. |

## Planned comparison

The two runs above test whether better-matched competitor inputs improve relevance. They do not compare the three-role pipeline against a single-pass baseline. That baseline has not been run, so no comparative performance result is claimed.

For a future baseline, use the same prospect, product details, model, source-evaluation checklist, and competitor URLs as Run 2. Record elapsed time, citation coverage, unsupported claims, coverage of company strategy, competitor mentions, leadership, and product/strategy summary, and whether the output fits on one page.