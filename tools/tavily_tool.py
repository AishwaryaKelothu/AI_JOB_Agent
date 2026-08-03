import os
import requests
from tavily import TavilyClient
from bs4 import BeautifulSoup
from pathlib import Path
from langchain.tools import tool



# -------------------- Tavily Search -------------------- #
@tool
def search_jobs(query: str) -> list:
    """Search the jobs related to AI engineers,FDE,SE"""

    api_key = os.getenv("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")

    if not api_key:
        print("TAVILY_API_KEY not found.")
        return []
    
    try:
        client = TavilyClient(api_key=api_key)

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=5,
            include_answer=False,
        )

        jobs = []

        for result in response.get("results", []):
            jobs.append({
                "title": result.get("title"),
                "company": None,
                "location": None,
                "description": result.get("content", ""),
                "apply_url": result.get("url"),
                "source": "Tavily"
            })

        return jobs

    except Exception as e:
        print(f"Tavily Error : {e}")
        return []



# -------------------- Greenhouse -------------------- #

GREENHOUSE_BOARDS = {
    "Workato": "workato",
    "OpenAI": "openai",
    "Stripe": "stripe",
    "Notion": "notion",
    "Canva": "canva",
}

@tool
def greenhouse_search_jobs(query: str):

    """Search the jobs related to AI engineers,FDE,SE"""

    jobs = []

    query = query.lower()

    for company, board in GREENHOUSE_BOARDS.items():

        url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

        try:

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                continue

            data = response.json()

            for job in data.get("jobs", []):

                searchable = (
                    job.get("title", "")
                    + " "
                    + job.get("absolute_url", "")
                ).lower()

                if query in searchable:

                    jobs.append({
                        "title": job.get("title"),
                        "company": company,
                        "location": job.get("location", {}).get("name"),
                        "description": "",
                        "apply_url": job.get("absolute_url"),
                        "source": "Greenhouse"
                    })

        except Exception as e:
            print(f"{company}: {e}")

    return jobs


# -------------------- Ashby -------------------- #

ASHBY_COMPANIES = {
    "OpenAI": "openai",
    "ElevenLabs": "elevenlabs",
    "Notion": "notion",
    "Ramp": "ramp",
    "Vanta": "vanta",
    "Clay": "clay",
    "Boomi": "boomi",
    "PostHog": "posthog",
}
@tool
def ashby_search_jobs(query: str):
    """Search the jobs related to AI engineers,FDE,SE roles"""
    jobs = []

    query = query.lower()

    for company, slug in ASHBY_COMPANIES.items():

        url = f"https://jobs.ashbyhq.com/{slug}"

        try:

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):

                title = link.get_text(strip=True)

                if title and query in title.lower():

                    href = link["href"]

                    if href.startswith("/"):
                        href = "https://jobs.ashbyhq.com" + href

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": None,
                        "description": "",
                        "apply_url": href,
                        "source": "Ashby"
                    })

        except Exception as e:
            print(f"{company}: {e}")

    return jobs


# -------------------- Lever -------------------- #

LEVER_COMPANIES = {
    "Postman": "postman",
    "Rippling": "rippling",
    "Miro": "miro",
    "Coupa": "coupa",
    "Kinsta": "kinsta",
    "Entrata": "entrata",
}

@tool
def lever_search_jobs(query: str):
    """Search the jobs related to AI engineers,FDE,SE"""
    jobs = []

    query = query.lower()

    for company, board in LEVER_COMPANIES.items():

        url = f"https://api.lever.co/v0/postings/{board}"

        try:

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                continue

            postings = response.json()

            for job in postings:

                searchable = (
                    job.get("text", "")
                    + " "
                    + job.get("categories", {}).get("location", "")
                ).lower()

                if query in searchable:

                    jobs.append({
                        "title": job.get("text"),
                        "company": company,
                        "location": job.get("categories", {}).get("location"),
                        "description": job.get("descriptionPlain", ""),
                        "apply_url": job.get("hostedUrl"),
                        "source": "Lever"
                    })

        except Exception as e:
            print(f"{company}: {e}")

    return jobs


# -------------------- Combine All Sources -------------------- #

def get_all_jobs(query: str):
    jobs = []

    jobs.extend(search_jobs.invoke(query))
    jobs.extend(greenhouse_search_jobs.invoke(query))
    jobs.extend(ashby_search_jobs.invoke(query))
    jobs.extend(lever_search_jobs.invoke(query))

    # Remove duplicate URLs
    unique = {}

    for job in jobs:
        url = job.get("apply_url")
        if url:
            unique[url] = job

    return list(unique.values())
    return unique



if __name__ == "__main__":

    jobs = get_all_jobs("AI Engineer")
   
    print(f"Found {len(jobs)} jobs")

    import json
    print(json.dumps(jobs, indent=2))




