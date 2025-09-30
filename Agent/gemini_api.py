
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types


def generate_response(messages: List[Dict]) -> str:
    
    gemini_messages = []
    for msg in messages:
        if "parts" in msg:
            gemini_messages.append(msg)
        else:
            gemini_messages.append({
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            })

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=gemini_messages,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )

    return response.candidates[0].content.parts[0].text



agent_rules = [{"role": "user", 
               "content": """You are a helpful ai agent that helps in listing and reading and answering questions about files in google drive.
               you must always respond with an action
               ALWAYS LIST FILES FIRST
               You can use the following tools:

{
  "tool_name": "list_files",
  "description": "list the files in the drive",
  "parameters": { }
}

{
  "tool_name": "read_file",
  "description": "from the list of files, read the content of a file, given its name, id and mimeType, do not ask for confirmation, just read it",
  "parameters": {
    "type": "object",
    "properties": {
      "file_id": { "type": "int" },
      "file_name": { "type": "string" },
      "mimeType": { "type": "string" },
    },
    "required": ["file_id", "file_name", "mimeType"]
}

{
  "tool_name": "search_files",
  "description": "Search files in Google Drive using a query string. The query must follow the Google Drive v3 search syntax (e.g., name contains 'report').",
  "parameters": {
    "type": "object",
    "properties": {
      "query": { "type": "string" }
    },
    "required": ["query"]
  }
}

{
  "tool_name": "reply",
  "description": "Use if you wish to respond without an action, whether to answer a question or to say you have finished your task, or to summarize, anything that doesnt need one of the other actions. pass oyur message to this function's paramter",
  "parameters": {
    "type": "object",
    "properties": {
      "message": { "type": "string" },
   
    },
    "required": ["message"]
}

{
  "tool_name": "terminate",
  "description": "Ends the current conversation or loop. The agent should call this when the user is done.",
  "parameters": {}
}

use this fromat EXACTLY , for ALL tools:
```json
{
  "tool_name": "tool_name_here",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}
```"""}]

def reply(message: str) -> str:
    return message