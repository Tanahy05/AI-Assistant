import tkinter as tk
from tkinter import scrolledtext
from assistant import Assistant  # Your backend class


class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.assistant = Assistant()

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state="disabled", bg="#F5F5F5"
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input frame
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_field = tk.Entry(self.input_frame, font=("Arial", 12))
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.input_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)

        # Tag configs
        self.chat_area.tag_config(
            "user",
            foreground="white",
            background="#3A81F1",
            justify="right",
            lmargin1=200,
            rmargin=10,
        )
        self.chat_area.tag_config(
            "model",
            foreground="black",
            background="#EAEAEA",
            justify="left",
            lmargin1=10,
            rmargin=200,
        )

    def add_message(self, message, sender="user"):
        """Add a chat bubble to the chat area."""
        self.chat_area.config(state="normal")

        if sender == "user":
            self.chat_area.insert(tk.END, f"\nYou: {message}\n", "user")
        else:
            self.chat_area.insert(tk.END, f"\nAssistant:\n{message}\n", "model")

        self.chat_area.config(state="disabled")
        self.chat_area.yview(tk.END)

    def format_response(self, response):
        """Format assistant responses like the CLI output."""
        # Case: list of files (list of dicts with 'name' + 'mimeType')
        if isinstance(response, list) and all(isinstance(f, dict) for f in response):
            formatted = []
            for i, file in enumerate(response, start=1):
                name = file.get("name", "Unnamed")
                mime = file.get("mimeType", "Unknown")
                formatted.append(f"{i}) {name}, mimeType: {mime}")
            return "\n".join(formatted)

        # Case: dictionary (fallback → key: value lines)
        if isinstance(response, dict):
            return "\n".join(f"{k}: {v}" for k, v in response.items())

        # Default: plain string
        return str(response)

    def send_message(self, event=None):
        """Handle user input and display assistant response."""
        user_input = self.input_field.get().strip()
        if not user_input:
            return

        self.add_message(user_input, sender="user")
        self.input_field.delete(0, tk.END)

        response = self.assistant.process_input(user_input)

        if response == "TERMINATE":
            self.add_message("Session ended by Assistant.", sender="model")
            self.root.quit()
        elif response:
            formatted = self.format_response(response)
            self.add_message(formatted, sender="model")


