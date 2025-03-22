#!/usr/bin/env python3
import os
import sys
from pathlib import Path

print("=== Setup Verification Tool ===")
print(f"Current working directory: {os.getcwd()}")

# Check file structure
frontend_dir = Path("simple-scheduling-ui")
required_files = [
    frontend_dir / "index.html",
    frontend_dir / "styles.css",
    frontend_dir / "app.js",
    Path("app.py"),
    Path("scheduling_agent.py"),
    Path("start-scheduling.sh"),
    Path(".env")
]

print("\nChecking required files:")
all_files_exist = True
for file_path in required_files:
    exists = file_path.exists()
    print(f"- {file_path}: {'✅ Found' if exists else '❌ Not found'}")
    if not exists:
        all_files_exist = False

# Check environment variables
print("\nChecking environment variables:")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    env_vars = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
    }
    
    all_env_vars_set = True
    for var_name, var_value in env_vars.items():
        if var_value:
            display_value = var_value[:5] + "..." if var_name == "OPENAI_API_KEY" and var_value else var_value
            print(f"- {var_name}: ✅ Set to {display_value}")
        else:
            print(f"- {var_name}: ❌ Not set")
            all_env_vars_set = False
except ImportError:
    print("❌ python-dotenv not installed, skipping environment check")
    all_env_vars_set = False

# Check Flask installation
print("\nChecking Python dependencies:")
dependencies = ["flask", "flask_cors", "supabase", "openai", "asyncio"]
all_deps_installed = True

for dep in dependencies:
    try:
        __import__(dep)
        print(f"- {dep}: ✅ Installed")
    except ImportError:
        print(f"- {dep}: ❌ Not installed")
        all_deps_installed = False

# Final verdict
print("\n=== SUMMARY ===")
if all_files_exist and all_env_vars_set and all_deps_installed:
    print("✅ All checks passed! Your setup appears to be correct.")
    print("\nTo start the application, run:")
    print("./start-scheduling.sh")
else:
    print("❌ Some checks failed. Please fix the issues above and try again.")
    
    if not all_files_exist:
        print("\nSome files are missing. Make sure all required files are in the correct location.")
    
    if not all_env_vars_set:
        print("\nEnvironment variables are not set correctly. Make sure to edit the .env file with your credentials.")
    
    if not all_deps_installed:
        print("\nSome Python dependencies are missing. Run:")
        print("pip3 install flask flask-cors python-dotenv supabase openai") 