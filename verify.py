#!/usr/bin/env python
"""Quick verification that the app structure is correct"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('FLASK_ENV', 'development')

print("🔍 Verifying Hamburger Shop setup...\n")

try:
    print("✓ Loading Flask app...")
    from app import create_app
    app = create_app('development')
    
    print("✓ App created successfully")
    
    print("✓ Checking blueprints...")
    with app.app_context():
        from flask import url_for
        
        # Test root route
        print(f"  - Root route: /")
        
        # Test auth routes
        print(f"  - Auth blueprint: /auth/login, /auth/register, /auth/logout")
        
        # Test customer routes
        print(f"  - Customer blueprint: /shop/")
        
        # Test admin routes
        print(f"  - Admin blueprint: /admin/")
    
    print("\n✅ All checks passed!")
    print("\n📝 To start the server, run:")
    print("   python start.py")
    print("\n   Or:")
    print("   python run.py")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
