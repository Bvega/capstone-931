from __future__ import annotations

import os
from datetime import date

import streamlit as st
from dotenv import load_dotenv

from sales_agent.documents import DocumentInputError, extract_document_text
from sales_agent.pipeline import SalesResearchPipeline
from sales_agent.report import make_markdown_report, make_pdf_report
from sales_agent.validation import InputValidationError, parse_competitor_urls, validate_public_url

load_dotenv()

st.set_page_config(page_title="Sales Account Brief", page_icon="📊", layout="centered")
st.title("Sales Account Brief")
st.caption("A source-backed account research prototype for sales representatives")
st.info("Use public business information. Review every claim and source before relying on the brief.")

with st.form("account_inputs"):
    st.subheader("Product")
    product_name = st.text_input("Product name *")
    product_category = st.text_input("Product category *", placeholder="Cloud data platform")
    value_proposition = st.text_area("Value proposition *", height=90)

    st.subheader("Prospective account")
    company_name = st.text_input("Company name *")
    company_url = st.text_input("Company URL *", placeholder="https://example.com")
    competitor_text = st.text_area(
        "Competitor URLs (one per line)",
        placeholder="https://competitor-one.example\nhttps://competitor-two.example",
        height=90,
    )
    target_contact = st.text_input("Target contact (optional)")
    product_file = st.file_uploader(
        "Product overview (optional)",
        type=["txt", "md", "pdf", "docx"],
        help="Maximum 5 MB. The extracted text is included in the model request.",
    )
    submitted = st.form_submit_button("Research account", type="primary")

if submitted:
    try:
        required = {
            "Product name": product_name,
            "Product category": product_category,
            "Value proposition": value_proposition,
            "Company name": company_name,
        }
        missing = [label for label, value in required.items() if not value.strip()]
        if missing:
            raise InputValidationError("Complete required fields: " + ", ".join(missing) + ".")
        company_url = validate_public_url(company_url)
        competitor_urls = parse_competitor_urls(competitor_text)
        overview = ""
        if product_file is not None:
            raw = product_file.getvalue()
            if len(raw) > 5 * 1024 * 1024:
                raise DocumentInputError("The uploaded file is larger than 5 MB.")
            overview = extract_document_text(product_file.name, raw)

        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to your local .env file and restart the app.")

        model = os.getenv("OPENAI_MODEL", "gpt-6-luna").strip()
        payload = {
            "product_name": product_name.strip(),
            "product_category": product_category.strip(),
            "value_proposition": value_proposition.strip(),
            "company_name": company_name.strip(),
            "company_url": company_url,
            "competitor_urls": competitor_urls,
            "target_contact": target_contact.strip(),
            "product_overview": overview,
        }
        with st.spinner("Researching public information and preparing the account brief…"):
            result = SalesResearchPipeline(api_key=api_key, model=model).run(payload)

        st.session_state["brief_result"] = result
        st.session_state["brief_payload"] = payload
        st.session_state["brief_model"] = model
        st.session_state["brief_date"] = date.today().isoformat()
    except (InputValidationError, DocumentInputError, RuntimeError, ValueError) as exc:
        st.error(str(exc))
    except Exception as exc:  # show a plain error without exposing credentials or request headers
        st.error(f"The research run failed ({type(exc).__name__}). Check the key, model access, and connection, then retry.")

if "brief_result" in st.session_state:
    result = st.session_state["brief_result"]
    payload = st.session_state["brief_payload"]
    run_date = st.session_state["brief_date"]
    model = st.session_state["brief_model"]
    st.divider()
    st.subheader(f"Account brief: {payload['company_name']}")
    st.caption(f"Research date: {run_date} · Model: {model}")
    st.markdown(result.brief_markdown)
    st.subheader("Sources")
    if result.sources:
        for source in result.sources:
            st.markdown(f"- [{source.title or source.url}]({source.url})")
    else:
        st.warning("The research response did not return source annotations. Verify claims before use.")
    report_md = make_markdown_report(payload, result, run_date, model)
    report_pdf = make_pdf_report(payload, result, run_date, model)
    left, right = st.columns(2)
    left.download_button(
        "Download Markdown",
        data=report_md.encode("utf-8"),
        file_name="sales_account_brief.md",
        mime="text/markdown",
    )
    right.download_button(
        "Download PDF",
        data=report_pdf,
        file_name="sales_account_brief.pdf",
        mime="application/pdf",
    )

