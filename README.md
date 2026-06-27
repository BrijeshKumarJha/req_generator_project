# 🐍 ReqGen - The Smart Python Dependency Analyzer

ReqGen is a open-source, lightweight, GUI-powered desktop utility designed for developers and freelancers. It safely parses Python files and entire project directories to automatically generate clean, production-ready `requirements.txt` files—without executing the underlying code.

## 🌟 Why ReqGen?
Standard tools often rely on basic regex text matching, which accidentally picks up modules from comments or strings. ReqGen uses Python's built-in `ast` (Abstract Syntax Tree) module to structurally analyze code, ensuring 100% accurate extraction. It also intelligently filters out Python Standard Library and C-level built-in modules, outputting only true third-party dependencies.

## ✨ Features
* **Project Folder Scanning:** Select an entire directory, and ReqGen will recursively find and combine dependencies from all nested `.py` files.
* **Single File Mode:** Granular control to analyze individual Python scripts.
* **Interactive UI:** Built with `customtkinter`, the app presents a modern dark-mode interface.
* **Selective Export:** Review all detected packages in a scrollable checkbox list and uncheck any you wish to exclude before generation.
* **Smart Filtering:** Automatically ignores local sibling `.py` files, custom modules, and standard libraries (e.g., `os`, `sys`, `datetime`).

## 🛠️ Built With
* **Python 3**
* **Abstract Syntax Tree (`ast`)** - For deep code parsing
* **CustomTkinter** - For the modern, hardware-accelerated UI
* **Pathlib** - For robust cross-platform file system operations
* **PyInstaller** - Packaged into a standalone executable

## 🚀 How to Run (For Users)
1. Download the `gui.exe` from the Releases tab.
2. Double-click to launch (no Python installation required).
3. Choose either "Select Single File" or "Select Project Folder".
4. Click **Analyze Imports** to view detected third-party packages.
5. Click **Generate File** to instantly create your `requirements.txt` in the target directory!
