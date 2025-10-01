# Intelligent Google Drive Agent  

This project implements an intelligent agent that wraps around the Google Gemini API (ChatGPT-style) and integrates with Google Drive to dynamically answer user queries based on Drive content.  

---

## 📝 Setup Instructions
1. **Clone the repository**  
```bash
git clone <repo-url>
cd <repo-folder>
```
2. **Set up a virtual environment** 

```bash 
python -m venv venv
```
3. **Install dependencies**
```bash
pip install -r requiremnts.txt
```

For this code to work, the .env file containing the pai keys and the credentials.json is neeeded, altough not provided in this repo for security purposes

## 🚀 Project Overview

The agent can do the following:  

- Interact via a **command-line interface (CLI)**.  
- Automatically **search for relevant files** in Google Drive based on a user query.  
- **Read file contents** from text-based files (TXT, Google Docs, PDFs).  
- Feed file contents **back into the AI** to generate informed answers.  
- Use structured actions to:  
  - `list_files` – list files in Drive.  
  - `search_files` – search for files with AI-generated queries.  
  - `read_file` – read file contents.  
  - `reply` – respond without file operations.  
  - `terminate` – end the session.  

The system dynamically combines user queries, retrieved file content, and agent rules to build prompts for the AI.

---

## ⚙️ Features & Functionality

1. **Google Drive Integration**  
   - Authenticates via OAuth2 using `credentials.json`.  
   - Supports listing and searching files.  
   - Supports reading:
     - Google Docs (exported as plain text).  
     - TXT files (directly decoded).  
     - PDFs (text extracted via PyPDF2).  

2. **Dynamic Context Injection**  
   - Retrieved file content is appended to the conversation memory before being sent to Gemini.  
   - Queries can be generated dynamically by the AI, but **fixed filters** (like date ranges) can be enforced in code to avoid API errors.  

3. **Error Handling & Robustness**  
   - Malformed AI JSON responses are retried up to 5 times.  
   - PDF parsing falls back safely if text extraction fails.  
   - Queries with dates in the future are automatically clamped to the current UTC date to prevent “cannot look into the future” errors.  



