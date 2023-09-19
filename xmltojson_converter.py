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

        # ...

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
                # ...

            # Wait for 7 seconds before checking the URL for changes
            time.sleep(7)

    def run(self):
        self.thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    xml_to_json_ui = XMLToJsonUI(root)

    # ...

    xml_to_json_ui.pack()
    root.mainloop()
