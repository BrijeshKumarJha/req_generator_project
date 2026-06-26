import customtkinter as ctk
from tkinter import filedialog
import os
from pathlib import Path
from brain import extract_imports

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ReqGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ReqGen - Dependency Analyzer")
        self.geometry("650x650")
        self.filepath = None
        self.checkbox_objects = [] # Checkboxes ka data store karne ke liye

        # --- UI Elements ---
        self.title_label = ctk.CTkLabel(self, text="🐍 Python Dependency Analyzer", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=15)

        # File Selection
        self.select_btn = ctk.CTkButton(self, text="📂 Select Python File", command=self.select_file)
        self.select_btn.pack(pady=5)
        
        self.file_label = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.file_label.pack(pady=5)

        # 1. Naya Button: Analyze Imports
        self.analyze_btn = ctk.CTkButton(self, text="🔍 Analyze Imports", command=self.analyze_file, fg_color="#E67E22", hover_color="#D35400")
        self.analyze_btn.pack(pady=10)

        # 2. Naya Frame: Scrollable Checkbox Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=300, height=150, label_text="Detected Packages (Uncheck to exclude)")
        self.scroll_frame.pack(pady=10)

        # Output Name & Generate
        self.filename_entry = ctk.CTkEntry(self, width=200, placeholder_text="Output file name")
        self.filename_entry.insert(0, "requirements.txt")
        self.filename_entry.pack(pady=10)

        self.generate_btn = ctk.CTkButton(self, text="⚡ Generate File", command=self.generate_reqs, fg_color="#28a745", hover_color="#218838")
        self.generate_btn.pack(pady=10)

        self.console = ctk.CTkTextbox(self, width=500, height=100)
        self.console.pack(pady=10)
        self.console.insert("0.0", "System Ready...\n")

    # --- Methods ---
    def log(self, message):
        self.console.insert("end", message + "\n")
        self.console.see("end")

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.filepath:
            filename = os.path.basename(self.filepath)
            self.file_label.configure(text=filename, text_color="white")
            self.log(f"Selected: {self.filepath}")
            
            # Purane checkboxes saaf karna naya file select hone par
            for cb in self.checkbox_objects:
                cb.destroy()
            self.checkbox_objects.clear()

    def analyze_file(self):
        if not self.filepath:
            self.log("❌ Error: Please select a file first.")
            return
            
        self.log("\n⏳ Analyzing imports...")
        
        # Purane checkboxes clear karo (agar user ne do baar analyze dabaya)
        for cb in self.checkbox_objects:
            cb.destroy()
        self.checkbox_objects.clear()
            
        try:
            packages = extract_imports(self.filepath)
            
            if not packages:
                self.log("⚠️ No external packages found.")
                return
                
            self.log(f"✅ Found {len(packages)} external packages.")
            
            # 3. Har package ke liye ek checkbox banana
            for pkg in packages:
                cb = ctk.CTkCheckBox(self.scroll_frame, text=pkg)
                cb.pack(pady=5, anchor="w", padx=20)
                cb.select() # Default tick mark lagana
                self.checkbox_objects.append(cb)
                
        except Exception as e:
            self.log(f"❌ Error occurred: {e}")

    def generate_reqs(self):
        if not self.filepath:
            self.log("❌ Error: Please select a Python file.")
            return
            
        if not self.checkbox_objects:
            self.log("❌ Error: Please 'Analyze Imports' first.")
            return

        # 4. Sirf un checkboxes ko uthana jo 'Checked' (1) hain
        selected_packages = []
        for cb in self.checkbox_objects:
            if cb.get() == 1:
                selected_packages.append(cb.cget("text"))

        if not selected_packages:
            self.log("⚠️ Error: You unchecked everything! Nothing to save.")
            return

        output_name = self.filename_entry.get()
        if not output_name.endswith(".txt"):
            output_name += ".txt"

        target_file_path = Path(self.filepath)
        output_dir = target_file_path.parent
        final_output_path = output_dir / output_name

        try:
            with open(final_output_path, "w", encoding="utf-8") as f:
                for pkg in selected_packages:
                    f.write(pkg + "\n")

            self.log(f"\n🎉 Success! Generated '{output_name}' with {len(selected_packages)} packages.")
            
        except Exception as e:
            self.log(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    app = ReqGenApp()
    app.mainloop()