# VulnChatBot (m8a8a8y-Bot)

![Project Logo](https://img.shields.io/badge/Vulnerability-Intelligence-blue?style=for-the-badge&logo=target)
![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_UI-white?style=for-the-badge&logo=flask)

**VulnChatBot** is a premium, AI-powered vulnerability intelligence platform. It combines local database searching (Metasploit, SSTI) with deep AI analysis via the **Groq API** to help security researchers find and understand exploits lightning-fast.

## 🚀 Key Features

*   **AI Deep Search**: Specialized mode for CVEs and Service Version vulnerabilities.
*   **Live Exploit-DB Integration**: Direct links to the latest exploit code.
*   **Metasploit Integration**: Search local MSF database modules instantly.
*   **Premium Web UI**: A sleek, glassmorphism-themed interface with dark mode.
*   **Professional CLI**: A color-coded terminal version for fast operation.
*   **Secure API Handling**: Uses `.env` to keep your keys safe from exposure.

## 🛠️ Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/m8a8a8y/VulnChatBot.git
    cd VulnChatBot
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**:
    Never hardcode your API key. VulnChatBot reads it from the `GROQ_API_KEY` environment variable.
    Local development: Create a `.env` file (use `.env.example` as a template):
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    GROQ_MODEL=llama-3.3-70b-versatile
    ```
    Production/Hosting: Set `GROQ_API_KEY` (and optionally `GROQ_MODEL`) in your server's environment settings. (e.g. GitHub Secrets, Heroku Config Vars, etc.) If the configured model is unavailable or encounters a `404 / model_not_found` error, VulnChatBot will automatically fall back to alternate available Groq models (such as `llama-3.1-70b-versatile`, `llama3-70b-8192`, `llama3-8b-8192`).

4.  **Run the App**:
    *   **Web Version**: `python app.py` (Access at `http://127.0.0.1:5000`)
    *   **CLI Version**: `python chat.py`

## 🛡️ Usage

- **General Search**: Enter keywords like `ssh`, `windows`, or `smb` in the main search bar to see local database matches.
- **AI Search**: Click "AI Search" in the sidebar and enter a specific CVE (e.g., `CVE-2021-44228`) for a deep analysis and direct exploit links.

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
*Created with ❤️ by m8a8a8y*
