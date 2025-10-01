import gdrive as gd
import gemini_api as gapi
import json
import re

class Assistant:
    def __init__(self):
        self.iteration = 0
        self.memory = []
        self.creds = gd.authenticate()

    def process_input(self, user_input: str):
        self.memory.append({"role": "user", "content": user_input})
        prompt = gapi.agent_rules + self.memory
        response = gapi.generate_response(prompt)

        max_tries = 5
        tries = 0
        while tries < max_tries:
            raw_response = response
            candidate = raw_response

            if "```" in raw_response:
                parts = raw_response.split("```")
                if len(parts) > 1:
                    candidate = parts[1].strip()
                else:
                    candidate = raw_response

            if candidate.lower().startswith("json"):
                candidate = candidate[4:].strip()

            match = re.search(r'\{.*\}', candidate, re.DOTALL)
            if match:
                candidate = match.group(0)

            try:
                response = json.loads(candidate)
                break
            except Exception as e:
                print(f"Error parsing response: {e}")
                response = {}
                tries += 1

        self.memory.append({"role": "model", "content": json.dumps(response)})

        tool_response = None
        if "tool_name" in response:
            tool_name = response["tool_name"]
            parameters = response.get("parameters", {})

            if tool_name == "list_files":
                tool_response = gd.list_files(self.creds)
                enumerator = 1
                for file in tool_response:
                    print(f"{enumerator}) {file['name']}, mimeType: {file['mimeType']})")
                    enumerator += 1

            elif tool_name == "read_file":
                file_id = parameters.get("file_id", "")
                mime_type = parameters.get("mimeType", "")
                tool_response = gd.read_file_content(self.creds, file_id, mime_type)
                print(f"File content:\n{tool_response}")

            elif tool_name == "reply":
                message = parameters.get("message", "")
                tool_response = gapi.reply(message)
                print(f"Agent Reply: {tool_response}")

            elif tool_name == "search_files":
                query = parameters.get("query", "").strip()
                if (query.startswith("'") and query.endswith("'")) or (query.startswith('"') and query.endswith('"')):
                    query = query[1:-1]

                tool_response = gd.search_files(self.creds, query)
                enumerator = 1
                for file in tool_response:
                    print(f"{enumerator}) {file['name']}, mimeType: {file['mimeType']})")
                    enumerator += 1

            elif tool_name == "terminate":
                print("Agent signaled termination. Ending session.")
                return "TERMINATE"

            else:
                tool_response = f"Unknown tool: {tool_name}"

            self.memory.append({
                "role": "model",
                "parts": [{"text": json.dumps(tool_response)}]
            })

        self.iteration += 1
        return tool_response

    def run_cli(self):
        while True:
            user_input = input("User: ")
            result = self.process_input(user_input)
            if result == "TERMINATE":
                break


