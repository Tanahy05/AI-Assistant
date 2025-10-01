
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
               any date given you do not question, do not validate it, just use it as is.
               you must always respond with an action
               You can use the following tools in the exact format specified, do not forget any braces or anything else:

{
  "tool_name": "list_files",
  "description": "list the files in the drive",
  "parameters": { }
}

prioritze the following tool if there is a criteria for the lsiting: 

{
  "tool_name": "search_files",
  "description": "Search files in Google Drive using a query string. The query must follow the Google Drive v3 search syntax. Examples:\n- name contains 'report'\n- mimeType='application/pdf'\n- name contains 'sales' and mimeType='application/vnd.google-apps.document'",
  "parameters": {
    "type": "object",
    "properties": {
      "query": { "type": "string" }
    },
    "required": ["query"]
  }
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
use the following action to reply to the use in case you do not need to invoke an action, anything ranging from errors to a greeting must be done using this action:
{
  "tool_name": "reply",
  "description": "TO be used for normal replies which does not invoke any other actions",
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