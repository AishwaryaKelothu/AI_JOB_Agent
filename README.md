# 🤖 AI Job Search Agent

An intelligent AI-powered job search automation system that continuously searches for relevant job opportunities based on a candidate's profile and delivers the best matching jobs directly via email every day.

Instead of manually browsing multiple job portals, this agent automatically collects recent openings, filters them using AI, and sends only the most relevant opportunities with direct application links.

---

## 🚀 Features

- 🔍 Searches jobs from multiple ATS platforms
  - Greenhouse
  - Lever
  - Ashby
  - Tavily Search

- 🤖 AI-powered job matching
  - Matches jobs against candidate skills
  - Filters irrelevant jobs
  - Scores relevance using LLMs

- 📧 Daily Email Notifications
  - Sends top matching jobs directly to email
  - Includes application links
  - Eliminates manual searching

- ⏰ Automated Scheduling
  - Runs every day at **10:00 AM**
  - Delivers fresh job openings

- ☁️ Cloud Deployment
  - Deployed on Railway for real-time testing and execution

---

# 🏗️ Architecture

```
              Candidate Profile
                     │
                     ▼
        ┌─────────────────────────┐
        │   Search Job Sources    │
        └─────────────────────────┘
           │      │      │      │
           ▼      ▼      ▼      ▼
     Greenhouse Lever Ashby Tavily
           │
           ▼
   LangChain Tools Invocation
           │
           ▼
      Collect Job Listings
           │
           ▼
      Gemini / Groq LLM
           │
           ▼
 AI Matching & Requirement Filtering
           │
           ▼
 Select Best Matching Jobs
           │
           ▼
 Email Notification (10 AM)
           │
           ▼
 Candidate Applies Directly
```

---

# 🛠️ Tech Stack

### Programming

- Python

### AI & LLM

- LangChain
- Google Gemini
- Groq LLM

### Job Sources

- Greenhouse
- Lever
- Ashby
- Tavily Search API

### Deployment

- Railway

### Notifications

- Email Automation

---

# ⚙️ Workflow

### Step 1

The system searches multiple ATS platforms for newly posted jobs.

- Greenhouse
- Lever
- Ashby
- Tavily

---

### Step 2

LangChain tools invoke each source and retrieve available job postings.

---

### Step 3

The collected jobs are passed to Gemini/Groq.

The LLM compares:

- Skills
- Experience
- Location
- Role
- Employment Type

with the candidate profile.

---

### Step 4

Only the most relevant jobs are selected.

Irrelevant opportunities are discarded automatically.

---

### Step 5

Every day at **10:00 AM**, the system sends an email containing:

- Company Name
- Job Title
- Location
- ATS Platform
- Direct Apply Link

This allows the candidate to apply immediately without spending time searching across multiple job portals.

---

# 📧 Sample Email

```
Subject: Today's AI Curated Job Matches

Hi,

Here are your top matching jobs for today.

1. Software Engineer
Company: XYZ
Location: Hyderabad
Apply:
https://...

2. AI Engineer
Company: ABC
Location: Remote
Apply:
https://...

Good luck!
```

---

# 💡 Why This Project?

Searching for jobs across different ATS platforms every day is repetitive and time-consuming.

This AI agent automates the entire process by:

- Searching multiple job portals
- Understanding the candidate's profile
- Filtering only relevant jobs
- Sending daily notifications with direct application links

This enables candidates to focus on applying rather than searching.

---

# 📂 Project Structure

```
AI_Job_Agent/
│
├── agents/
│   ├── search_agent.py
│   ├── filter_agent.py
│   ├── ranking_agent.py
│   └── notification_agent.py
│
├── tools/
│   ├── greenhouse.py
│   ├── lever.py
│   ├── ashby.py
│   └── tavily.py
│
├── prompts/
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 🎯 Future Improvements

- LinkedIn Jobs support
- Workday integration
- Smart job scoring dashboard
- Resume tailoring using AI
- Duplicate job detection
- Slack and WhatsApp notifications
- Personalized application tracking
- Multi-candidate support

---

# ⭐ Highlights

- AI-powered job search automation
- Multi-source ATS integration
- LangChain Tool Calling
- Gemini/Groq-based job filtering
- Daily scheduled email notifications
- Railway cloud deployment
- Saves time by delivering only relevant opportunities

---

## 👩‍💻 Author

**Aishwarya**

If you found this project useful, consider giving it a ⭐ on GitHub!
