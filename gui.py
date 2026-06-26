import customtkinter as ctk
from tkinter import filedialog
import os
from pathlib import Path
from brain import extract_imports, analyze_project


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ReqGenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ReqGen - Dependency Analyzer")
        self.geometry("650x700")
        
        self.target_path = None
        self.is_folder_mode = False
        self.checkbox_objects = [] # Checkboxes ka data store karne ke liye

        # --- UI Elements ---
        self.title_label = ctk.CTkLabel(self, text="🐍 Python Dependency Analyzer", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=15)

        # File Selection
        self.file_btn = ctk.CTkButton(self, text="📄 Select Single File", command=self.select_file)
        self.file_btn.pack(pady=5)
        
        self.folder_btn = ctk.CTkButton(self, text="📂 Select Project Folder", command=self.select_folder)
        self.folder_btn.pack(pady=5)
        
        self.file_label = ctk.CTkLabel(self, text="No target selected", text_color="gray")
        self.file_label.pack(pady=5)

        # 1. Naya Button: Analyze Imports
        self.analyze_btn = ctk.CTkButton(self, text="🔍 Analyze Imports", command=self.analyze_target, fg_color="#E67E22", hover_color="#D35400")
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

    #Helper method
    def clear_checkboxes(self):
        for cb in self.checkbox_objects:
            cb.destroy()
        self.checkbox_objects.clear()
    
    # --- Methods ---
    def log(self, message):
        self.console.insert("end", message + "\n")
        self.console.see("end")

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            self.target_path = path
            self.is_folder_mode = False
            self.file_label.configure(text=os.path.basename(path), text_color="white")
            self.log(f"Selected File: {path}")
            self.clear_checkboxes()

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.target_path = path
            self.is_folder_mode = True
            self.file_label.configure(text=f"Folder: {os.path.basename(path)}", text_color="#F1C40F") # Yellow color for folder
            self.log(f"Selected Folder: {path}")
            self.clear_checkboxes()

    def analyze_target(self):
        if not self.target_path:
            self.log("❌ Error: Please select a file or folder first.")
            return
            
        self.log("\n⏳ Analyzing dependencies...")
        self.clear_checkboxes()
            
        try:
            # 2. Logic: Decide karna ki brain ka kaunsa function chalana hai
            if self.is_folder_mode:
                packages = analyze_project(self.target_path)
            else:
                packages = extract_imports(self.target_path)
            
            if not packages:
                self.log("⚠️ No external packages found.")
                return
                
            self.log(f"✅ Found {len(packages)} unique external packages.")
            
            for pkg in packages:
                cb = ctk.CTkCheckBox(self.scroll_frame, text=pkg)
                cb.pack(pady=5, anchor="w", padx=20)
                cb.select()
                self.checkbox_objects.append(cb)
                
        except Exception as e:
            self.log(f"❌ Error occurred: {e}")

    def generate_reqs(self):
        if not self.target_path:
            self.log("❌ Error: Please select a target.")
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

        if self.is_folder_mode:
            output_dir = Path(self.target_path)
        else:
            output_dir = Path(self.target_path).parent
            
        final_output_path = output_dir / output_name

        try:
            with open(final_output_path, "w", encoding="utf-8") as f:
                for pkg in selected_packages:
                    f.write(pkg + "\n")

            self.log(f"\n🎉 Success! Generated '{output_name}' at target location.")
            
        except Exception as e:
            self.log(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    app = ReqGenApp()
    app.mainloop()