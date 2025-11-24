#!/usr/bin/env python3
"""
Lint runner for Cyber Intelligence Platform
"""

import subprocess
import sys
import os

def run_flake8():
    """Run flake8 linting"""
    print("🔍 Running flake8 linting...")
    
    result = subprocess.run([
        sys.executable, "-m", "flake8",
        ".",
        "--count",
        "--select=E9,F63,F7,F82",  # Syntax and undefined names
        "--show-source",
        "--statistics"
    ])
    
    if result.returncode == 0:
        print("✅ No critical linting errors found!")
        return True
    else:
        print("❌ Critical linting errors found!")
        return False

def run_black_check():
    """Check code formatting with black"""
    print("🎨 Checking code formatting with black...")
    
    result = subprocess.run([
        sys.executable, "-m", "black",
        "--check",
        "."
    ])
    
    if result.returncode == 0:
        print("✅ Code is properly formatted!")
        return True
    else:
        print("❌ Code formatting issues found!")
        print("   Run 'black .' to fix formatting")
        return False

def run_mypy():
    """Run type checking with mypy"""
    print("📝 Running type checking with mypy...")
    
    result = subprocess.run([
        sys.executable, "-m", "mypy",
        "--ignore-missing-imports",
        "."
    ])
    
    if result.returncode == 0:
        print("✅ Type checking passed!")
        return True
    else:
        print("❌ Type checking issues found!")
        return False

def check_syntax():
    """Check syntax of all Python files"""
    print("🐍 Checking Python syntax...")
    
    python_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if (file.endswith(".py") and 
                "venv" not in root and 
                ".pytest_cache" not in root and
                "__pycache__" not in root):
                python_files.append(os.path.join(root, file))
    
    all_valid = True
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                compile(f.read(), filepath, 'exec')
            print(f"  ✅ {filepath}")
        except SyntaxError as e:
            print(f"  ❌ {filepath}: {e}")
            all_valid = False
    
    return all_valid

def main():
    """Main lint runner"""
    print("🚀 Cyber Intelligence Platform Lint Suite")
    print("=" * 50)
    
    success = True
    
    # Check syntax first
    if not check_syntax():
        success = False
        print("\n🔧 Please fix syntax errors before continuing.")
        return 1
    
    print("\n" + "=" * 50)
    
    # Run linting tools
    success &= run_flake8()
    success &= run_black_check() 
    success &= run_mypy()
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 All linting checks passed!")
        return 0
    else:
        print("🔧 Some linting checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
