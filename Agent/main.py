import gdrive as gd
import gemini_api as gapi
import json
def main():
    iteration=0
    max_iterations=10
    memory=[]
    creds = None
    while iteration < max_iterations:
        user_input = input("User: ")
        memory.append({"role": "user", "content": user_input})
        prompt = gapi.agent_rules + memory
        response = gapi.generate_response(prompt)
        print(f"Raw Agent Response: {response}")
        response=response.split('```')[1].strip()[4:]
        try:
            response=json.loads(response)
        except Exception as e:
            print(f"Error parsing response: {e}")

        memory.append({"role": "assistant", "content": json.dumps(response)})


        if "tool_name" in response:
            tool_name = response["tool_name"]
            parameters = response.get("parameters", {})
            if tool_name == "list_files":
                tool_response = gd.list_files()
            elif tool_name == "read_file":
                file_name = parameters.get("file_name", "")
                file_id = parameters.get("file_id", "")
                mime_type = parameters.get("mimeType", "")
                tool_response = gd.read_file(file_id,file_name,mime_type)
            elif tool_name == "document_file":
                file_name = parameters.get("file_name", "")
            else:
                tool_response = f"Unknown tool: {tool_name}"
            memory.append({"role": "user", "content": f"{tool_response}"})
        print(f"Agent: {tool_response}")
        iteration += 1

if __name__ == "__main__":
    main()