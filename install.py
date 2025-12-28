#!/usr/bin/env python
"""Check and install requirements"""
import subprocess
import sys

print("📦 Hamburger Shop - Dependency Check\n")

try:
    with open('requirements.txt', 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"Installing {len(packages)} packages...\n")
    
    # Install packages
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q'] + packages)
    
    print("\n✅ All dependencies installed successfully!")
    print("\n🚀 You can now start the server:")
    print("   python start.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
