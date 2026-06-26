import ast
import sys
from pathlib import Path

def extract_imports(filepath):
    print(f"🧠 Scanning file: {filepath}...\n")
    
    # 1. File ko safely read karna
    with open(filepath, "r", encoding="utf-8") as file:
        file_content = file.read()
        
    # 2. String code ko Abstract Syntax Tree (AST) mein convert karna
    tree = ast.parse(file_content)

    imports_found = set()

    # 3. AST ke har ek node (hisse) par jana
    for node in ast.walk(tree):
        
        # Agar node normal import hai (jaise: import pandas as pd)
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_name = alias.name.split('.')[0]
                imports_found.add(base_name)
                
        # Agar node specific import hai (jaise: from datetime import datetime)
        elif isinstance(node, ast.ImportFrom):
            if node.module: # module check karna zaroori hai
                base_name = node.module.split('.')[0]
                imports_found.add(base_name)

    third_party_packages = []
    target_dir = Path(filepath).parent
    for pkg in imports_found:
        # Check 1: Kya ye built-in module hai?
        is_builtin = pkg in sys.builtin_module_names
        
        # Check 2: Kya ye standard library hai?
        is_stdlib = hasattr(sys, 'stdlib_module_names') and pkg in sys.stdlib_module_names
        
        # Check 3: NAYA LOGIC - Kya ye koi local file ya folder hai? (e.g. brain.py)
        is_local_file = (target_dir / f"{pkg}.py").exists()
        is_local_folder = (target_dir / pkg).is_dir()
        
        # Agar built-in, stdlib, local file, ya local folder NAHI hai, tabhi add karo
        if not is_builtin and not is_stdlib and not is_local_file and not is_local_folder:
            third_party_packages.append(pkg)
    
    third_party_packages.sort()
    return third_party_packages

def analyze_project(folder_path):
    print(f"📁 Scanning entire project folder: {folder_path}...\n")
    
    # Ek set banayenge taaki poore project mein koi package do baar na aaye
    all_project_packages = set()
    
    # pathlib ka .rglob() folder aur uske andar ke sub-folders mein saari .py files dhoondhta hai
    python_files = list(Path(folder_path).rglob("*.py"))
    
    if not python_files:
        print("❌ No Python files found in this folder.")
        return []

    # Har file ko ek-ek karke humare purane 'extract_imports' brain ke paas bhejenge
    for filepath in python_files:
        # Har file ke chhante hue packages nikalenge
        file_packages = extract_imports(filepath)
        # Unhe main set mein daal denge (duplicates apne aap delete ho jayenge)
        all_project_packages.update(file_packages)
        
    # Set ko wapas sorted list mein badal kar bhej denge
    final_list = list(all_project_packages)
    final_list.sort()
    
    return final_list    

# 🚀 Test The Brain
if __name__ == "__main__":
    detected_packages = extract_imports("test_code.py")
    
    print("✅ Filtered Third-Party Packages (Ready for requirements.txt):")
    if detected_packages:
        for pkg in detected_packages:
            print(f" -> {pkg}")
    else:
        print(" ❌ No external packages found.")