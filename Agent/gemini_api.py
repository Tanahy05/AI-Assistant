from litellm import completion
from typing import List, Dict
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def generate_response(messages: List[Dict]) -> str:
    """
    Sends a prompt to Gemini via LiteLLM and returns the assistant's raw response.
    """
    response = completion(
        model="gemini/gemini-1.5-flash-latest",
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content


agent_rules = [{"role": "system", 
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
  "description": "from the list of files, read the content of a file, given its name, id and mimeType",
  "parameters": {
    "type": "object",
    "properties": {
      "file_id": { "type": "int" },
      "file_name": { "type": "string" },
      "mimeType": { "type": "string" },
    },
    "required": ["file_id", "file_name", "mimeType"]
  }
}



use this fromat EXACTLY :
```json
{
  "tool_name": "tool_name_here",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  }
}
```"""}]

