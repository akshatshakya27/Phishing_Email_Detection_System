import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import requests
import json

# --- Color Palettes ---
DARK = {
    'BG': "#181c23",
    'PANEL': "#232733",
    'ORANGE': "#FF6347",
    'BLUE': "#3B6EF6",
    'WHITE': "#F5F6FA",
    'GRAY': "#A0A4B8",
    'HIST_ENTRY_BG': "#232733",
    'HIST_ENTRY_FG': "#F5F6FA",
    'HIST_ENTRY_BORDER': "#232733",
}
LIGHT = {
    'BG': "#FAFAFB",  # slightly off-white for contrast
    'PANEL': "#FFFFFF",
    'ORANGE': "#FF6347",
    'BLUE': "#3B6EF6",
    'WHITE': "#232733",
    'GRAY': "#3A3A3A",  # darker gray for text
    'HIST_ENTRY_BG': "#F1F2F6",  # more visible light gray for cards
    'HIST_ENTRY_FG': "#232733",
    'HIST_ENTRY_BORDER': "#E0E1E6",
}

class ThemeToggleSwitch(ctk.CTkFrame):
    def __init__(self, parent, command=None, **kwargs):
        super().__init__(parent, fg_color="transparent", height=34, **kwargs)
        self.command = command
        self.is_dark = True
        self.animation_running = False
        self.dark_bg = DARK['BG']
        self.light_bg = LIGHT['BG']
        self.switch_frame = ctk.CTkFrame(self, corner_radius=16, height=28, width=56, fg_color=self.dark_bg, border_width=0)
        self.switch_frame.pack(padx=4, pady=3)
        self.switch_frame.pack_propagate(False)
        self.button = ctk.CTkFrame(self.switch_frame, width=22, height=22, corner_radius=11, fg_color="#ffffff", border_width=0)
        self.button.place(x=28, rely=0.48, anchor="w")
        self.switch_frame.bind("<Button-1>", self.toggle)
        self.button.bind("<Button-1>", self.toggle)

    def animate(self, start_pos, end_pos, start_color, end_color, start_button_color, end_button_color, mode):
        ANIMATION_SPEED = 12
        STEPS = 10
        if self.animation_running:
            return
        self.animation_running = True
        def update_position(step):
            if step <= STEPS:
                progress = step / STEPS
                current_x = start_pos + (end_pos - start_pos) * progress
                self.button.place(x=int(current_x), rely=0.48, anchor="w")
                if mode == "dark":
                    self.switch_frame.configure(fg_color=self.dark_bg)
                else:
                    self.switch_frame.configure(fg_color=self.light_bg)
                self.button.configure(fg_color=end_button_color if progress > 0.5 else start_button_color)
                if step == STEPS:
                    self.animation_running = False
                    if self.command:
                        self.command(self.is_dark)
                else:
                    self.after(ANIMATION_SPEED, lambda: update_position(step + 1))
        update_position(0)

    def toggle(self, event=None):
        if self.animation_running:
            return
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.animate(4, 28, self.light_bg, self.dark_bg, "#ffffff", "#0078d4", "dark")
        else:
            self.animate(28, 4, self.dark_bg, self.light_bg, "#0078d4", "#ffffff", "light")

    def get_state(self):
        return self.is_dark

class PhishingUIDemo:
    def __init__(self, root):
        self.root = root
        self.mode = 'dark'
        self.palette = DARK
        ctk.set_appearance_mode("dark")
        self.root.title("Phishing Email Detector")
        self.root.geometry("900x550")
        self.root.configure(bg=self.palette['BG'])
        self.build_layout()
        self.api_url = "http://localhost:8000/predict"  # FastAPI backend URL

    def build_layout(self):
        self.container = ctk.CTkFrame(self.root, fg_color=self.palette['BG'], corner_radius=20)
        self.container.pack(fill="both", expand=True, padx=16, pady=16)
        # Left panel
        self.left_panel = ctk.CTkFrame(self.container, fg_color=self.palette['PANEL'], corner_radius=22, width=520, height=500)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=0)
        self.left_panel.pack_propagate(False)
        # Divider (make it same as BG)
        self.divider = ctk.CTkFrame(self.container, fg_color=self.palette['BG'], width=8, height=500)
        self.divider.pack(side="left", fill="y", padx=0, pady=0)
        # Right panel
        self.right_panel = ctk.CTkFrame(self.container, fg_color=self.palette['PANEL'], corner_radius=22, width=320, height=500)
        self.right_panel.pack(side="right", fill="y", padx=(0, 0), pady=0)
        self.right_panel.pack_propagate(False)
        # --- Left Panel Content ---
        ctk.CTkLabel(self.left_panel, text="Phishing Email Detector", font=("Segoe UI", 28, "bold"), text_color=self.palette['ORANGE'], fg_color="transparent").place(x=32, y=24)
        ctk.CTkLabel(self.left_panel, text="Enter Email Body:", font=("Segoe UI", 16), text_color=self.palette['WHITE'], fg_color="transparent", anchor="w").place(x=32, y=80)
        self.textbox_frame = ctk.CTkFrame(self.left_panel, fg_color=self.palette['BG'], corner_radius=16, width=420, height=120)
        self.textbox_frame.place(x=32, y=120)
        self.email_body = ctk.CTkTextbox(self.textbox_frame, font=("Segoe UI", 16), fg_color=self.palette['BG'], text_color=self.palette['WHITE'], corner_radius=12, width=400, height=100)
        self.email_body.place(x=10, y=10)
        self.predict_btn = ctk.CTkButton(self.left_panel, text="Predict", font=("Segoe UI", 18, "bold"), fg_color=self.palette['BLUE'], text_color="#FFFFFF", corner_radius=12, width=120, height=44, command=self.predict)
        self.predict_btn.place(x=32, y=270)
        ctk.CTkLabel(self.left_panel, text="Predicion:", font=("Segoe UI", 16), text_color=self.palette['GRAY'], fg_color="transparent").place(x=32, y=350)
        self.pred_value = ctk.CTkLabel(self.left_panel, text="phishing", font=("Segoe UI", 16, "bold"), text_color=self.palette['ORANGE'], fg_color="transparent")
        self.pred_value.place(x=140, y=350)
        ctk.CTkLabel(self.left_panel, text="Confidence:", font=("Segoe UI", 16), text_color=self.palette['GRAY'], fg_color="transparent").place(x=32, y=390)
        self.conf_value = ctk.CTkLabel(self.left_panel, text="87,45%", font=("Segoe UI", 16, "bold"), text_color=self.palette['ORANGE'], fg_color="transparent")
        self.conf_value.place(x=150, y=390)
        # --- Right Panel Content ---
        ctk.CTkLabel(self.right_panel, text="Prediction History", font=("Segoe UI", 22, "bold"), text_color=self.palette['GRAY'], fg_color="transparent").place(x=24, y=32)
        self.history_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.history_frame.place(x=12, y=80)
        example_entries = [
            ("Please verify your account", "phishing", "phishing"),
            ("Account suspended", "phishing", "legitimate"),
            ("Dear valued customer", "phishing", "legitimate"),
            ("Your invoice for March", "phishing", "legitimate"),
            ("Sign in to view document", "phishing", "legitimate"),
        ]
        y_offset = 0
        self.history_blocks = []
        for text, left_label, right_label in example_entries:
            block = self.add_history_entry(text, left_label, right_label, y_offset)
            self.history_blocks.append(block)
            y_offset += 76
        # Toggle mode switch
        toggle_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        toggle_frame.place(x=24, y=480)
        ctk.CTkLabel(toggle_frame, text="Toggle Mode", font=("Segoe UI", 16), text_color=self.palette['GRAY'], fg_color="transparent").pack(side="left")
        self.toggle_switch = ThemeToggleSwitch(toggle_frame, command=self.toggle_mode)
        self.toggle_switch.pack(side="left", padx=8)

    def add_history_entry(self, text, left_label, right_label, y):
        entry_frame = ctk.CTkFrame(self.history_frame, fg_color=self.palette['HIST_ENTRY_BG'], corner_radius=18, width=292, height=72, border_width=0)
        entry_frame.place(x=0, y=y)
        ctk.CTkLabel(entry_frame, text=text, font=("Segoe UI", 15), text_color=self.palette['HIST_ENTRY_FG'], fg_color="transparent", anchor="w").place(x=20, y=10)
        ctk.CTkLabel(entry_frame, text=left_label, font=("Segoe UI", 15, "bold"), text_color=self.palette['ORANGE'], fg_color="transparent", anchor="w").place(x=20, y=38)
        ctk.CTkLabel(entry_frame, text=right_label, font=("Segoe UI", 15, "bold"), text_color=self.palette['GRAY'], fg_color="transparent", anchor="e").place(x=272, y=38)
        return entry_frame

    def toggle_mode(self, is_dark):
        self.mode = 'dark' if is_dark else 'light'
        self.palette = DARK if self.mode == 'dark' else LIGHT
        ctk.set_appearance_mode(self.mode)
        self.update_colors()

    def update_colors(self):
        self.container.configure(fg_color=self.palette['BG'])
        self.left_panel.configure(fg_color=self.palette['PANEL'])
        self.right_panel.configure(fg_color=self.palette['PANEL'])
        self.divider.configure(fg_color=self.palette['BG'])
        for widget in self.left_panel.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                if 'Phishing Email Detector' in widget.cget('text'):
                    widget.configure(text_color=self.palette['ORANGE'])
                elif 'Enter Email Body:' in widget.cget('text'):
                    widget.configure(text_color=self.palette['WHITE'])
                elif 'Predicion:' in widget.cget('text') or 'Confidence:' in widget.cget('text'):
                    widget.configure(text_color=self.palette['GRAY'])
        self.pred_value.configure(text_color=self.palette['ORANGE'])
        self.conf_value.configure(text_color=self.palette['ORANGE'])
        self.textbox_frame.configure(fg_color=self.palette['BG'])
        self.email_body.configure(fg_color=self.palette['BG'], text_color=self.palette['WHITE'])
        self.predict_btn.configure(fg_color=self.palette['BLUE'], text_color="#FFFFFF")
        for widget in self.right_panel.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(text_color=self.palette['GRAY'])
        for block in self.history_blocks:
            block.destroy()
        self.history_blocks.clear()
        example_entries = [
            ("Please verify your account", "phishing", "phishing"),
            ("Account suspended", "phishing", "legitimate"),
            ("Dear valued customer", "phishing", "legitimate"),
            ("Your invoice for March", "phishing", "legitimate"),
            ("Sign in to view document", "phishing", "legitimate"),
        ]
        y_offset = 0
        for text, left_label, right_label in example_entries:
            block = self.add_history_entry(text, left_label, right_label, y_offset)
            self.history_blocks.append(block)
            y_offset += 76

    def predict(self):
        try:
            email_body = self.email_body.get("1.0", tk.END).strip()
            if not email_body:
                return

            response = requests.post(self.api_url, json={"body": email_body})
            if response.status_code == 200:
                result = response.json()
                self.pred_value.configure(text=result["prediction"])
                self.conf_value.configure(text=f"{result['confidence']*100:.2f}%")
                
                # Add to history
                self.add_to_history(email_body, result["prediction"], "legitimate" if result["prediction"] == "phishing" else "phishing")
            else:
                self.pred_value.configure(text="Error")
                self.conf_value.configure(text="0%")
        except Exception as e:
            self.pred_value.configure(text="Error")
            self.conf_value.configure(text="0%")

    def add_to_history(self, text, left_label, right_label):
        # Remove oldest entry if we have 5 entries
        if len(self.history_blocks) >= 5:
            self.history_blocks[0].destroy()
            self.history_blocks.pop(0)
        
        # Add new entry at the bottom
        y_offset = len(self.history_blocks) * 76
        block = self.add_history_entry(text, left_label, right_label, y_offset)
        self.history_blocks.append(block)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = PhishingUIDemo(root)
    root.mainloop()