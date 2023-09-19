import threading
import tkinter as tk
import requests
import time
import json
import xmltodict
import subprocess
import os

class XMLToJsonUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.xml_url_text_box = tk.Text(self, height=10, width=50)
        self.xml_url_text_box.pack()

        self.github_local_file_path_entry = tk.Entry(self)
        self.github_local_file_path_entry.pack()

        self.github_username_entry = tk.Entry(self)
        self.github_username_entry.pack()

        self.github_email_entry = tk.Entry(self)
        self.github_email_entry.pack()

        self.github_repository_entry = tk.Entry(self)
        self.github_repository_entry.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start_conversion)
        self.start_button.pack()

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_conversion)
        self.stop_button.pack()

        self.running = False
        self.thread = None

    def start_conversion(self):
        self.running = True
        self.thread = threading.Thread(target=self.conversion_loop)
        self.thread.start()

    def stop_conversion(self):
        self.running = False

    def conversion_loop(self):
        xml_urls = self.xml_url_text_box.get("1.0", tk.END).splitlines()
        github_local_file_path = self.github_local_file_path_entry.get()
        github_username = self.github_username_entry.get()
        github_email = self.github_email_entry.get()
        github_repository = self.github_repository_entry.get()

        while self.running:
            for xml_url in xml_urls:
                # Convert the XML to JSON
                xml_response = requests.get(xml_url)
                xml_data = xml_response.content
                json_data = xmltodict.parse(xml_data)

                # Write the JSON data to the local file path
                with open(github_local_file_path, "w") as f:
                    json.dump(json_data, f, indent=4)

                # Commit the changes to GitHub
                subprocess.run(["git", "add", github_local_file_path])
                subprocess.run(["git", "commit", "-m", "Converted XML to JSON"])
                subprocess.run(["git", "push", "--set-upstream", "origin", github_repository])

            # Wait for 7 seconds before checking the URL for changes
            time.sleep(7)

    def run(self):
        self.thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    xml_to_json_ui = XMLToJsonUI(root)

    xml_to_json_ui.pack()
    root.mainloop()
