import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from langchain.tools import tool

from tools.tavily_tool import search_jobs, get_all_jobs
from tools.email_tool import send_email
from tools.memory import is_duplicate, mark_as_sent
from tools.scheduler import start_scheduler
import json
from langchain_google_genai import ChatGoogleGenerativeAI

# Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Load .env
env_path = Path(__file__).parent / ".env"
from pathlib import Path
from dotenv import load_dotenv
import os
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
# Create Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)
def analyze_jobs_with_ai(jobs: list) -> dict:
    """Analyze job postings and return structured JSON."""

    prompt = f"""
You are an AI Job Extraction Assistant.

Extract the following fields from each job.

Return ONLY valid JSON.

Schema:

{{
  "jobs": [
    {{
      "title": "",
      "company": "",
      "location": "",
      "experience": "",
      "salary": "",
      "matching_skills": [],
      "missing_skills": [],
      "match_score": 0,
      "apply_url": ""
    }}
  ]
}}

If any field is unavailable, return "Not specified".

Jobs:

{json.dumps(jobs, indent=2)}
"""

    try:
        response = llm.invoke(prompt)

        raw = response.content.strip()

        # Remove Markdown if Gemini returns it
        raw = raw.replace("```json", "").replace("```", "").strip()

        return json.loads(raw)

    except Exception as e:
        logger.error(f"Gemini extraction failed: {e}")
        return {"jobs": []}
    
def build_report(jobs: list) -> str:
    """Build a clean, fixed-format report string using Python (not AI)."""
    lines = []
    for idx, job in enumerate(jobs, 1):
        lines.append(f"{idx}.")
        lines.append(f"Job Title: {job['title']}")
        lines.append(f"Company: {job['company']}")
        lines.append(f"Location: {job['location']}")
        lines.append(f"Experience: {job['experience']}")
        lines.append(f"Salary: {job['salary']}")
        lines.append(f"Apply Link: {job['apply_url']}")
        lines.append("")
        lines.append("---------------------------------")
        lines.append("")

    lines.append(f"Total Jobs Found: {len(jobs)}")
    return "\n".join(lines)


def run_workflow():

    logger.info("========== JOB SEARCH STARTED ==========")

    search_query = """give me the list of jobs which are hiring for forward deployed engineer,Ai engineer,software developer"""
    jobs = get_all_jobs(search_query)

    logger.info(f"Total Jobs Retrieved : {len(jobs)}")

    if not jobs:

        logger.info("No jobs found.")

        return

    result = analyze_jobs_with_ai(jobs)

    jobs = result["jobs"]


    # Step 3 — Python formats the report (guaranteed clean)
    report = build_report(jobs)
    logger.info("Report ready!")

    # Step 4 — Send email
    logger.info("Sending email...")
    success = send_email(report)

    # Step 5 — Save to memory
    if success:
        sent_urls = [job["url"] for job in jobs]
        mark_as_sent(sent_urls)
        logger.info(f"Done! {len(jobs)} jobs emailed and saved to memory.")
    else:
        logger.error("Email failed. Jobs NOT marked as sent.")


if __name__ == "__main__":

    logger.info("Running once for testing...")

    run_workflow()

    logger.info("Starting scheduler...")

    start_scheduler(run_workflow) 