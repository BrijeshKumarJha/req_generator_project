import ast
import sys

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
    for pkg in imports_found:
        is_builtin = pkg in sys.builtin_module_names
        
        # Check 2: Kya ye Python standard library hai? (jaise 'datetime', 'json')
        # hasattr check lagaya hai taaki purane Python versions (below 3.10) par script crash na ho
        is_stdlib = hasattr(sys, 'stdlib_module_names') and pkg in sys.stdlib_module_names
        
        # Agar dono nahi hain, toh hi list mein add karo
        if not is_builtin and not is_stdlib:
            third_party_packages.append(pkg)
    
    third_party_packages.sort()
    return third_party_packages
    

# 🚀 Test The Brain
if __name__ == "__main__":
    detected_packages = extract_imports("test_code.py")
    
    print("✅ Filtered Third-Party Packages (Ready for requirements.txt):")
    if detected_packages:
        for pkg in detected_packages:
            print(f" -> {pkg}")
    else:
        print(" ❌ No external packages found.")