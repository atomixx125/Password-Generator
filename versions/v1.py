import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import string
import pyperclip

class QuotePasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Quote Password Generator")
        self.root.geometry("920x780")
        
        # Predefined Quotes
        self.predefined_quotes = [
            "To be or not to be that is the question.",
            "I think therefore I am.",
            "The only way to do great work is to love what you do.",
            "Stay hungry, stay foolish.",
            "Be the change that you wish to see in the world.",
            "May the Force be with you.",
            "I have a dream that one day this nation will rise up.",
            "Life is what happens when you're busy making other plans.",
            "The journey of a thousand miles begins with one step.",
            "Not all those who wander are lost.",
            "To infinity and beyond!"
        ]
        
        self.wordlist = ["apple","mountain","river","ocean","forest","thunder","shadow","dragon",
                        "phoenix","galaxy","starlight","whisper","midnight","horizon","echo",
                        "brave","victory","freedom","legend","quantum","nebula","warrior"]
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Quote Password Generator", 
                font=("Helvetica", 18, "bold")).pack(pady=10)
        
        # Predefined Quotes
        tk.Label(self.root, text="Predefined Quotes (Select & Load)", 
                font=("Helvetica", 11, "bold")).pack(anchor="w", padx=20)
        
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=20, pady=5, fill="x")
        
        self.quote_listbox = tk.Listbox(list_frame, height=6, font=("Helvetica", 10))
        for quote in self.predefined_quotes:
            self.quote_listbox.insert(tk.END, quote)
        
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.quote_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.quote_listbox.yview)
        
        self.quote_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        tk.Button(list_frame, text="Load Selected Quote →", 
                 command=self.load_selected_quote, bg="#2196F3", fg="white").pack(pady=5)
        
        # Mode Selection
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)
        
        self.mode_var = tk.StringVar(value="full")
        tk.Radiobutton(mode_frame, text="Full Quote Transform", variable=self.mode_var, 
                      value="full", command=self.switch_mode).pack(side=tk.LEFT, padx=15)
        tk.Radiobutton(mode_frame, text="First Letters Only", variable=self.mode_var, 
                      value="acronym", command=self.switch_mode).pack(side=tk.LEFT, padx=15)
        tk.Radiobutton(mode_frame, text="Memorable Passphrase", variable=self.mode_var, 
                      value="passphrase", command=self.switch_mode).pack(side=tk.LEFT, padx=15)
        
        # Frames (same as before)
        self.full_frame = tk.Frame(self.root)
        tk.Label(self.full_frame, text="Your Quote:").pack(anchor="w", padx=20, pady=(5,0))
        self.custom_quote = scrolledtext.ScrolledText(self.full_frame, height=5, wrap=tk.WORD)
        self.custom_quote.pack(padx=20, pady=5, fill="x")
        
        self.acronym_frame = tk.Frame(self.root)
        tk.Label(self.acronym_frame, text="Your Quote:").pack(anchor="w", padx=20, pady=(5,0))
        self.acronym_quote = scrolledtext.ScrolledText(self.acronym_frame, height=5, wrap=tk.WORD)
        self.acronym_quote.pack(padx=20, pady=5, fill="x")
        
        self.phrase_frame = tk.Frame(self.root)
        tk.Label(self.phrase_frame, text="Number of words:").pack(anchor="w", padx=20, pady=(10,0))
        self.num_words_var = tk.IntVar(value=5)
        tk.Scale(self.phrase_frame, from_=3, to=8, orient=tk.HORIZONTAL, 
                variable=self.num_words_var, length=400).pack(padx=20)
        
        tk.Button(self.phrase_frame, text="Generate New Passphrase", bg="#2196F3", fg="white",
                 command=self.generate_passphrase).pack(pady=8)
        
        self.phrase_display = tk.Text(self.phrase_frame, height=2, font=("Helvetica", 11), bg="#f0f0f0")
        self.phrase_display.pack(padx=20, pady=5, fill="x")
        
        # Options
        opt_frame = tk.Frame(self.root)
        opt_frame.pack(pady=12)
        
        tk.Label(opt_frame, text="Strength:").pack(side=tk.LEFT, padx=10)
        self.strength_var = tk.IntVar(value=2)   # Lower default
        tk.Scale(opt_frame, from_=1, to=4, orient=tk.HORIZONTAL, 
                variable=self.strength_var, length=200).pack(side=tk.LEFT)
        
        self.add_extra_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Add 1-3 extra characters", 
                      variable=self.add_extra_var).pack(side=tk.LEFT, padx=20)
        
        # Generate
        tk.Button(self.root, text="Generate Password", font=("Helvetica", 13, "bold"),
                 bg="#4CAF50", fg="white", height=2, command=self.generate_password).pack(pady=15)
        
        tk.Label(self.root, text="Generated Password:", font=("Helvetica", 11, "bold")).pack(anchor="w", padx=20)
        self.result_text = tk.Text(self.root, height=3, font=("Courier", 16, "bold"), bg="#f0f0f0")
        self.result_text.pack(padx=20, pady=8, fill="x")
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Copy Password", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=10)
        
        self.switch_mode()
    
    def load_selected_quote(self):
        selection = self.quote_listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Quote", "Please select a quote from the list.")
            return
        quote = self.predefined_quotes[selection[0]]
        mode = self.mode_var.get()
        
        if mode == "full":
            self.custom_quote.delete("1.0", tk.END)
            self.custom_quote.insert(tk.END, quote)
        elif mode == "acronym":
            self.acronym_quote.delete("1.0", tk.END)
            self.acronym_quote.insert(tk.END, quote)
    
    def switch_mode(self):
        for frame in (self.full_frame, self.acronym_frame, self.phrase_frame):
            frame.pack_forget()
        mode = self.mode_var.get()
        if mode == "full":
            self.full_frame.pack(fill="x", padx=20, pady=5)
        elif mode == "acronym":
            self.acronym_frame.pack(fill="x", padx=20, pady=5)
        else:
            self.phrase_frame.pack(fill="x", padx=20, pady=5)
    
    def transform_text(self, text, strength=2):
        """Gentler transformation - keeps most of the original text"""
        replacements = {'a':['4','@','a'], 'e':['3','e'], 'i':['1','!','i'],
                       'o':['0','o'], 's':['5','$','s'], 'l':['1','l']}
        
        result = []
        for char in text:
            if char.isalpha():
                lower = char.lower()
                # Much lower chance of replacement
                if lower in replacements and random.random() < (strength / 6.0):
                    result.append(random.choice(replacements[lower]))
                else:
                    # Random case only
                    result.append(char.upper() if random.random() < 0.45 else char.lower())
            else:
                result.append(char)
        
        password = "".join(result)
        
        # Add only 1 to 3 extra characters at the end
        if self.add_extra_var.get():
            extras = ""
            num_extras = random.randint(1, 3)
            for _ in range(num_extras):
                extras += random.choice(string.digits + "!@#$%^&*")
            password += extras
        
        return password
    
    def get_acronym(self, text):
        words = text.split()
        return "".join(word[0].upper() for word in words if word)
    
    def generate_password(self):
        mode = self.mode_var.get()
        strength = self.strength_var.get()
        
        if mode == "full":
            text = self.custom_quote.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Input Required", "Please enter a quote!")
                return
            password = self.transform_text(text, strength)
            
        elif mode == "acronym":
            text = self.acronym_quote.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Input Required", "Please enter a quote!")
                return
            base = self.get_acronym(text)
            password = self.transform_text(base, strength)
            
        else:  # passphrase
            phrase = self.phrase_display.get("1.0", tk.END).strip()
            if not phrase:
                messagebox.showwarning("No Phrase", "Please generate a passphrase first!")
                return
            base = self.get_acronym(phrase)
            password = self.transform_text(base, strength)
        
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, password)
    
    def generate_passphrase(self):
        num = self.num_words_var.get()
        words = random.sample(self.wordlist, num)
        phrase = " ".join(words)
        self.phrase_display.delete("1.0", tk.END)
        self.phrase_display.insert(tk.END, phrase)
        self.generate_password()
    
    def copy_to_clipboard(self):
        pw = self.result_text.get("1.0", tk.END).strip()
        if pw:
            pyperclip.copy(pw)
            messagebox.showinfo("Copied!", pw)
    
    def clear_all(self):
        self.custom_quote.delete("1.0", tk.END)
        self.acronym_quote.delete("1.0", tk.END)
        self.phrase_display.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuotePasswordGenerator(root)
    root.mainloop()
