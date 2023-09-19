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

        # Create labels
        self.xml_url_label = tk.Label(self, text="XML URLs:")
        self.github_username_label = tk.Label(self, text="GitHub Username:")
        self.github_email_label = tk.Label(self, text="GitHub Email:")
        self.github_repo_label = tk.Label(self, text="GitHub Repository:")
        self.github_local_file_path_label = tk.Label(self, text="GitHub Repository Local Files:")

        # Create a text box for the XML URLs
        self.xml_url_text_box = tk.Text(self, height=10, width=40)

        # Create entry fields for the GitHub username, email, repository, and local file path
        self.github_username_entry = tk.Entry(self)
        self.github_email_entry = tk.Entry(self)
        self.github_repo_entry = tk.Entry(self)
        self.github_local_file_path_entry = tk.Entry(self)

        # Create buttons
        self.start_button = tk.Button(self, text="Start", command=self.start_conversion)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_conversion)

        # Place the widgets on the grid
        self.xml_url_label.grid(row=0, column=0)
        self.xml_url_text_box.grid(row=1, column=0)
        self.github_username_label.grid(row=2, column=0)
        self.github_username_entry.grid(row=2, column=1)
        self.github_email_label.grid(row=3, column=0)
        self.github_email_entry.grid(row=3, column=1)
        self.github_repo_label.grid(row=4, column=0)
        self.github_repo_entry.grid(row=4, column=1)
        self.github_local_file_path_label.grid(row=5, column=0)
        self.github_local_file_path_entry.grid(row=5, column=1)
        self.start_button.grid(row=6, column=0)
        self.stop_button.grid(row=6, column=1)

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

        while self.running:
            for xml_url in xml_urls:
                # Get the XML file
                xml_file = requests.get(xml_url).content

                # Convert the XML file to JSON
                json_data = convert_xml_to_json(xml_file)

                # Change the current working directory to the GitHub
