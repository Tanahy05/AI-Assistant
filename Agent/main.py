import gdrive as gd
import gemini_api as gapi
import json
import re
def main():
    iteration=0
    memory=[]
    creds=gd.authenticate()
    while True:
        
        user_input = input("User: ")
        memory.append({"role": "user", "content": user_input})
        prompt = gapi.agent_rules + memory
        response = gapi.generate_response(prompt)

        
        raw_response = response.strip()
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
        except Exception as e:
            print(f"Error parsing response: {e}")
            response = {}



        memory.append({"role": "model", "content": json.dumps(response)})


        if "tool_name" in response:
            tool_name = response["tool_name"]
            parameters = response.get("parameters", {})

            if tool_name == "list_files":
                tool_response = gd.list_files(creds)
                for file in tool_response:
                    print(f"Found file: {file['name']} (mimeType: {file['mimeType']})")

            elif tool_name == "read_file":
                file_id = parameters.get("file_id", "")
                mime_type = parameters.get("mimeType", "")
                tool_response = gd.read_file_content(creds,file_id,mime_type)
                print(f"File content: {tool_response}")

            elif tool_name == "reply":
                message = parameters.get("message", "")
                tool_response = gapi.reply(message)
                print(f"Agent Reply: {tool_response}")

            elif tool_name == "terminate":
                print("Agent signaled termination. Ending session.")
                break

            else:
                tool_response = f"Unknown tool: {tool_name}"

            memory.append({
                "role": "model",
                "parts": [{
                    "text": json.dumps(tool_response)
                }]
            })
      
    
        iteration += 1

if __name__ == "__main__":
    main()