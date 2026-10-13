from types import SimpleNamespace

from sales_agent.pipeline import SalesResearchPipeline


class FakeResponses:
    def __init__(self):
        source = SimpleNamespace(url="https://example.com/news", title="Company news")
        annotation = SimpleNamespace(url_citation=source, url=source.url, title=source.title)
        research_content = SimpleNamespace(annotations=[annotation])
        self.items = [
            SimpleNamespace(output_text="Research notes", output=[SimpleNamespace(content=[research_content])]),
            SimpleNamespace(output_text="Evidence-based analysis", output=[]),
            SimpleNamespace(output_text="## Account snapshot\nA concise brief.", output=[]),
        ]
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.items[len(self.calls) - 1]


def test_pipeline_runs_three_roles_in_order_and_keeps_sources():
    responses = FakeResponses()
    client = SimpleNamespace(responses=responses)
    account = {
        "product_name": "Data Product",
        "product_category": "Analytics",
        "value_proposition": "Find insights faster",
        "company_name": "Example Co",
        "company_url": "https://example.com",
        "competitor_urls": [],
        "target_contact": "",
        "product_overview": "",
    }

    result = SalesResearchPipeline(api_key="unused-in-test", model="test-model", client=client).run(account)

    assert len(responses.calls) == 3
    assert responses.calls[0]["tools"] == [{"type": "web_search"}]
    assert "Research packet" in responses.calls[1]["input"]
    assert "Analysis" in responses.calls[2]["input"]
    assert result.research_notes == "Research notes"
    assert result.analysis == "Evidence-based analysis"
    assert result.brief_markdown.startswith("## Account snapshot")
    assert result.sources[0].url == "https://example.com/news"

