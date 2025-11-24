#!/usr/bin/env python3
"""
Test runner for Cyber Intelligence Platform
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests with pytest"""
    print("🧪 Running Cyber Intelligence Platform Tests...")
    
    # Run pytest with coverage
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:coverage_report"
    ])
    
    if result.returncode == 0:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")
        
    return result.returncode

def run_syntax_check():
    """Check syntax of all Python files"""
    print("🔍 Checking Python syntax...")
    
    python_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and "venv" not in root and ".pytest_cache" not in root:
                python_files.append(os.path.join(root, file))
    
    all_valid = True
    for filepath in python_files:
        try:
            with open(filepath, 'r') as f:
                compile(f.read(), filepath, 'exec')
            print(f"✅ {filepath}")
        except SyntaxError as e:
            print(f"❌ {filepath}: {e}")
            all_valid = False
    
    return all_valid

if __name__ == "__main__":
    print("🚀 Cyber Intelligence Platform Test Suite")
    print("=" * 50)
    
    # First check syntax
    if not run_syntax_check():
        print("\n🔧 Please fix syntax errors before running tests.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Then run tests
    exit_code = run_tests()
    sys.exit(exit_code)
