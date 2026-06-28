import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import sys

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        tk.Label(main_frame, text="Password Generator", font=("Arial", 16, "bold")).pack(pady=(0, 15))
        
        # Length control
        length_frame = ttk.Frame(main_frame)
        length_frame.pack(fill="x", pady=5)
        tk.Label(length_frame, text="Password Length:", font=("Arial", 10)).pack(side="left", padx=(0, 10))
        self.length_var = tk.IntVar(value=12)
        tk.Spinbox(length_frame, from_=4, to=50, textvariable=self.length_var,
                  width=8, font=("Arial", 10)).pack(side="left")
        
        # Special characters checkbox
        self.special_var = tk.BooleanVar(value=True)
        tk.Checkbutton(main_frame, text="Include Special Characters", 
                      variable=self.special_var, font=("Arial", 10)).pack(pady=5)
        
        # Generate button
        tk.Button(main_frame, text="Generate Password", command=self.generate_password,
                 font=("Arial", 12), bg="#4CAF50", fg="white", padx=25, pady=8).pack(pady=10)
        
        # Password display with copy button side by side
        display_frame = ttk.Frame(main_frame)
        display_frame.pack(fill="x", pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(display_frame, textvariable=self.password_var, 
                                      font=("Courier", 14), justify="center",
                                      state="readonly", width=25)
        self.password_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        self.copy_btn = tk.Button(display_frame, text="Copy", command=self.copy_password,
                                 font=("Arial", 10), bg="#2196F3", fg="white",
                                 padx=10, pady=3, state="disabled")
        self.copy_btn.pack(side="right")
        
        # Status bar
        self.status_label = tk.Label(main_frame, text="", font=("Arial", 9), fg="green")
        self.status_label.pack(pady=5)
        
        # Info label
        tk.Label(main_frame, text="Minimum length: 4 characters", 
                font=("Arial", 8), fg="gray").pack()
        if not CLIPBOARD_AVAILABLE:
            tk.Label(main_frame, text="Install pyperclip for clipboard support: pip install pyperclip", 
                    font=("Arial", 8), fg="orange").pack()
        
        self.current_password = ""
    
    def generate_password(self):
        """Generate password based on user settings."""
        try:
            length = self.length_var.get()
            use_special = self.special_var.get()
            
            if length < 4:
                messagebox.showerror("Error", "Password length must be at least 4 characters!")
                return
            
            # Character pools
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            digits = string.digits
            special = string.punctuation if use_special else ""
            
            # Ensure at least one of each type
            password = [
                random.choice(lowercase),
                random.choice(uppercase),
                random.choice(digits),
            ]
            if use_special:
                password.append(random.choice(special))
            
            # Fill remaining
            all_chars = lowercase + uppercase + digits + special
            if all_chars:
                password += random.choices(all_chars, k=length - len(password))
            else:
                messagebox.showerror("Error", "No character types selected!")
                return
            
            random.shuffle(password)
            self.current_password = ''.join(password)
            self.password_var.set(self.current_password)
            self.copy_btn.config(state="normal")
            self.status_label.config(text="Password generated successfully!", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def copy_password(self):
        """Copy password to clipboard."""
        if not self.current_password:
            self.status_label.config(text="Generate a password first!", fg="orange")
            return
        
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(self.current_password)
                self.status_label.config(text="Copied to clipboard!", fg="blue")
            except Exception as e:
                self.status_label.config(text=f"Copy failed: {e}", fg="red")
        else:
            # Fallback to tkinter clipboard
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.current_password)
                self.root.update()
                self.status_label.config(text="Copied to clipboard! (tkinter)", fg="blue")
            except:
                self.status_label.config(text="Could not copy to clipboard", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()