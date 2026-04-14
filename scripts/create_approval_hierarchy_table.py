#!/usr/bin/env python3
"""
Create approval_hierarchy table for managing department-specific approval rules
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import ApprovalHierarchy

def create_approval_hierarchy_table():
    """Create the approval_hierarchy table"""
    try:
        with app.app_context():
            # Create the table
            db.create_all()
            print("✅ Created approval_hierarchy table successfully")
            
            # Check if table exists and show structure
            inspector = db.inspect(db.engine)
            if 'approval_hierarchy' in inspector.get_table_names():
                columns = inspector.get_columns('approval_hierarchy')
                print("\n📋 Table structure:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
                    
                print(f"\n📊 Table created with {len(columns)} columns")
            else:
                print("❌ Table was not created properly")
                
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Creating approval_hierarchy table...")
    success = create_approval_hierarchy_table()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\nNext steps:")
        print("1. The approval hierarchy page is now ready to use")
        print("2. Admin can configure approval rules for each department")
        print("3. The system will use these rules for overtime approval workflow")
    else:
        print("\n❌ Setup failed. Please check the errors above.")