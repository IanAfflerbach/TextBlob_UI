import tkinter as tk
from tkinter import messagebox
import os


class BaseApp():
    def __init__(self):
        self.root = tk.Tk()

    def start(self):
        self.root.mainloop()


class SentimentAnalysisApp(BaseApp):
    def __init__(self):
        super().__init__()

        self.input_entry = tk.Entry(width=60)
        self.input_entry.grid(row=0, columnspan=2, padx=(20, 20), pady=(10, 5))

        use_file_button = tk.Button(text="Use File", width=25, command=self.__use_file_button_pressed)
        use_file_button.grid(row=1, column=0, padx=(20, 5), pady=(5, 5))

        gen_tree_button = tk.Button(text="Analyze Input", width=25, command=self.__analyze_input_button_pressed)
        gen_tree_button.grid(row=1, column=1, padx=(5, 20), pady=(5, 5))

        self.output_box = tk.Text(width=50, height=20)
        self.output_box.config(state=tk.DISABLED)
        self.output_box.grid(row=2, columnspan=2, padx=(20, 20), pady=(5, 10))

    def __use_file_button_pressed(self):
        entry = self.input_entry.get()
        if entry == "": return

        file_exists = os.path.exists(entry)
        if file_exists:
            self.output_box.config(state=tk.NORMAL)
            self.output_box.insert("1.0", entry)
            self.output_box.config(state=tk.DISABLED)
        else:
            messagebox.showerror("ERROR: File Not Found", "Could not open file: " + entry)        

    def __analyze_input_button_pressed(self):
        entry = self.input_entry.get()
        if entry == "": return