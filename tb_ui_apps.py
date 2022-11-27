import tkinter as tk
from tkinter import messagebox
import os
from textblob import TextBlob


class BaseApp():
    def __init__(self):
        self.root = tk.Tk()

        self.input_entry = tk.Entry(width=100)
        self.input_entry.grid(row=0, columnspan=2, padx=(20, 20), pady=(10, 5))

        use_file_button = tk.Button(text="Use File", width=45, command=self._use_file_button_pressed)
        use_file_button.grid(row=1, column=0, padx=(20, 5), pady=(5, 5))

        gen_tree_button = tk.Button(text="Analyze Input", width=45, command=self._analyze_input_button_pressed)
        gen_tree_button.grid(row=1, column=1, padx=(5, 20), pady=(5, 5))

    def start(self):
        self.root.mainloop()

    def _use_file_button_pressed(self):
        return

    def _analyze_input_button_pressed(self):
        return


class SentimentAnalysisApp(BaseApp):
    def __init__(self):
        super().__init__()

        self.output_box = tk.Text(width=43, height=20)
        self.output_box.config(state=tk.DISABLED)
        self.output_box.grid(row=2, column=0, padx=(20, 2), pady=(5, 10))

        self.stats_box = tk.Text(width=43, height=20)
        self.stats_box.config(state=tk.DISABLED)
        self.stats_box.grid(row=2, column=1, padx=(2, 20), pady=(5, 10))

    def _use_file_button_pressed(self):
        entry = self.input_entry.get()
        if entry == "": return

        file_exists = os.path.exists(entry)
        if not file_exists:
            messagebox.showerror("ERROR: File Not Found", "Could not open file: " + entry)      
            return

        with open(entry, "r") as f:
            lines = [x.strip() for x in f]
            self.__analyze_text(lines)  

    def _analyze_input_button_pressed(self):
        entry = self.input_entry.get()
        if entry == "": return
        self.__analyze_text([entry])

    def __analyze_text(self, text):
        total_phrases = len(text)
        num_pos, num_neut, num_neg = 0, 0, 0
        avg_sub, avg_pol = 0, 0
        analyzed_text = []

        for t in text:
            blob = TextBlob(t)
            avg_sub += blob.sentiment.subjectivity
            avg_pol += blob.sentiment.polarity
            
            if blob.sentiment.polarity < -0.25:
                num_neg += 1
                analyzed_text.append(t + " - neg")
            elif blob.sentiment.polarity < 0.25:
                num_neut += 1
                analyzed_text.append(t + " - neut")
            else:
                num_pos += 1
                analyzed_text.append(t + " - pos")

        avg_sub /= total_phrases
        avg_pol /= total_phrases

        # output analyzed phrase(s)
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete("1.0", "end")
        for t in analyzed_text:
            self.output_box.insert("end", t + "\n")
        self.output_box.config(state=tk.DISABLED)

        # output stats for phrase(s)
        self.stats_box.config(state=tk.NORMAL)
        self.stats_box.delete("1.0", "end")
        
        self.stats_box.insert("end", "Total Phrases: " + str(total_phrases) + "\n")

        self.stats_box.insert("end", "Number Positive Phrases: " + str(num_pos) + "\n")
        self.stats_box.insert("end", "Number Neutral Phrases: " + str(num_neut) + "\n")
        self.stats_box.insert("end", "Number Negative Phrases: " + str(num_neg) + "\n")

        self.stats_box.insert("end", "Average Subjectivity: " + str(avg_sub) + "\n")
        self.stats_box.insert("end", "Average Polarity: " + str(avg_pol) + "\n")

        self.stats_box.config(state=tk.DISABLED)


class POSApp(BaseApp):
    def __init__(self):
        super().__init__()

        self.output_box = tk.Text(width=90, height=20)
        self.output_box.config(state=tk.DISABLED)
        self.output_box.grid(row=2, columnspan=2, padx=(20, 20), pady=(5, 10))

    def _use_file_button_pressed(self):
        entry = self.input_entry.get()
        if entry == "": return

        file_exists = os.path.exists(entry)
        if not file_exists:
            messagebox.showerror("ERROR: File Not Found", "Could not open file: " + entry)      
            return

        with open(entry, "r") as f:
            self.__analyze_text(f.read())

    def _analyze_input_button_pressed(self):
        entry = self.input_entry.get()
        if entry == "": return
        self.__analyze_text(entry)

    def __analyze_text(self, phrase):
        # output tags
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete("1.0", "end")
        blob = TextBlob(phrase)
        for tag in blob.tags:
            self.output_box.insert("end", tag[1] + " - " + tag[0] + "\n")
        self.output_box.config(state=tk.DISABLED)