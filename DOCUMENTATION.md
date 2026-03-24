# VulnChatBot - Complete Technical Documentation

## 1. Introduction
**VulnChatBot (m8a8a8y-Bot)** is a hybrid vulnerability intelligence platform that integrates local dataset searches (using Metasploit, SSTI payloads, and Exploit-DB datasets) with Large Language Model (LLM) interpretations. The core objective of the platform is to empower penetration testers and security researchers to rapidly locate exploits and understand complex vulnerabilities without bouncing between multiple tools and search engines.

It offers two interfaces:
1. **Premium Web Application**: A sleek HTML/CSS/JS frontend powered by a Flask backend.
2. **CLI Interface**: A robust, color-coded terminal tool.

---

## 2. Architecture & Components

The application is structured around a few core modules:

### 2.1 Backend (`app.py` & `chat.py`)
- **`app.py`**: A Flask server hosting the web application. It handles routing, serving static files, and provides RESTful endpoints consumed by the web UI. It incorporates fuzzy matching (`thefuzz` library) to effectively search local CSV databases.
- **`chat.py`**: The Command Line Interface implementation of the bot. It uses pandas to load datasets and `subprocess` to integrate directly with `searchsploit` natively on the terminal.
- **`aibot`**: A prototype/alternative CLI that originally utilized OpenAI instead of Groq.

### 2.2 Frontend (`static/`)
- **`index.html`**: The main structure representing a modern chat-like vulnerability interface. Includes modals for fetching exploit code dynamically and distinct UI sections for conversational AI output and raw database results.
- **`script.js`**: Drives the interactivity. Handles executing `/api/search` and `/api/ai_deep_search`, interpreting JSON repsonses, and injecting both the AI chat bubbles and raw database matches into the user screen seamlessly.
- **`style.css` & `pro.css`**: Provides the styling using premium Glassmorphism and dynamic dark mode color palettes.

### 2.3 Datasets (`*.csv`)
The project searches across 3 primary local datasets to remain fast and functional:
- **`metasploit_data.csv`**: Contains information on Metasploit modules, linking them directly to rapid7 GitHub source files via API parsing.
- **`ssti_payloads_full.csv`**: Contains categorized server-side template injection payloads with the targeted platforms.
- **`exploitdb.csv`**: A legacy mapped CSV of Exploit-DB entries serving as an offline fallback when `searchsploit` output isn't readily available.

---

## 3. Core Features & AI Integration

The intelligence of VulnChatBot is heavily driven by **Groq's LLaMA-3.3-70B-versatile inference endpoint**, giving it near-instant reasoning capabilities.

### 3.1 Intuitive Database Searching
When queried, the Bot automatically queries Metasploit, SSTI, and Exploit-DB. It utilizes `thefuzz` to conduct partial ratio string matching (Threshold: 60) for broad keyword discovery. Simultaneously, it triggers a `searchsploit` sub-process to pull live path results.

### 3.2 Automated AI Interpretation (`/api/search`)
As of the latest iteration, regular searches automatically consult the Groq AI. If a user queries *"windows xp smb"*, the AI will:
1. Contextually explain the vulnerability (e.g., MS08-067).
2. Gracefully handle misspellings or vague queries by suggesting the closest known match.
This interpretation is displayed seamlessly as an AI response bubble before the raw database tables are shown.

### 3.3 Deep AI Search (`/api/ai_deep_search`)
Dedicated feature prioritizing specific CVEs (e.g., `CVE-2021-44228`) or explicit Service Versions (e.g., `Apache 2.4.49`). The AI is instructed to return a strictly formatted JSON object containing an in-depth analysis and explicit internet-searchable URLs for the exploit on GitHub and Exploit-DB.

### 3.4 Live Exploit Fetching (`/api/fetch_exploit`)
VulnChatBot maps `searchsploit` outputs to their live GitLab hosted equivalents (via `gitlab.com/exploit-database/exploitdb/-/raw/main`) and allows users to read the raw exploit code directly in a web UI modal without leaving the app.

---

## 4. REST API Reference

The Flask application exposes a concise API for the frontend JS:

#### `POST /api/search`
- **Body**: `{"query": "keyword"}`
- **Purpose**: Performs the comprehensive database scan. Automatically invokes Groq for an AI interpretation of the keyword. 
- **Returns**: Metasploit arrays, SSTI arrays, Exploit-DB legacy titles, parsed Searchsploit links, AI textual interpretation, and synthesized Exploit-DB search URLs.

#### `POST /api/ai_deep_search`
- **Body**: `{"query": "CVE-xxxx-xxxx"}`
- **Purpose**: Specific deep extraction. Enforces Regex checks ensuring input is a CVE or explicit version before querying the LLM to output pure JSON.
- **Returns**: Strict JSON structured data detailing the analysis and verified URLs.

#### `GET /api/fetch_exploit?url={gitlab_raw_url}`
- **Purpose**: Proxies external requests securely to grab raw exploit scripts from GitLab. Validates the URL strongly to prevent SSRF vulnerabilities.
- **Returns**: Raw text of the requested exploit code.

#### `POST /api/ask_ai`
- **Body**: `{"query": "question"}`
- **Purpose**: General purpose AI consultation endpoint. Ask the AI pentester agent plain-text questions on vulnerabilities.

---

## 5. Setup & Usage Instructions

1. **Prerequisites**:
   * Python 3.10+
   * Ensure `searchsploit` is installed functionally on your host system (comes pre-packaged mostly on Kali/Parrot OS), as `subprocess.run(['searchsploit'...])` assumes the binary is in your PATH.
   
2. **Environment Configuration**:
   VulnChatBot strictly reads your Groq API key from the `GROQ_API_KEY` environment variable for security.
   *   **Local Development**: Create a `.env` file in the root directory (based on `.env.example`). This file is ignored by git to prevent accidental exposure of your keys.
   *   **Production Hosting**: Professional hosting environments provide interfaces to set environment variables. Set `GROQ_API_KEY` there to keep it completely hidden from the codebase and the public.


3. **Running the Platform**:
   * **To use the Web Interface**: 
     ```bash
     python app.py
     ```
     Navigate your browser to `http://127.0.0.1:5000` or `http://localhost:5000`.
   
   * **To use the Terminal Chatbot**: 
     ```bash
     python chat.py
     ```
     This opens `m8a8a8y-Bot (CLI Version)`, listening for commands continuously. Type `exit` to close.
