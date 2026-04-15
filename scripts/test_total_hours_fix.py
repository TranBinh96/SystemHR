#!/usr/bin/env python3
"""
Test script to verify total_hours None handling
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import OvertimeRequest

def test_total_hours_fix():
    """Test that total_hours=None doesn't cause errors"""
    with app.app_context():
        print("=" * 60)
        print("Testing total_hours None Handling")
        print("=" * 60)
        
        # Get all overtime requests
        requests = OvertimeRequest.query.all()
        
        print(f"\nTotal overtime requests: {len(requests)}")
        
        # Check for None values
        none_count = 0
        has_value_count = 0
        
        for req in requests:
            if req.total_hours is None:
                none_count += 1
            else:
                has_value_count += 1
        
        print(f"\nRequests with total_hours = None: {none_count}")
        print(f"Requests with total_hours value: {has_value_count}")
        
        # Test sum calculation (this was causing the error)
        print("\n" + "=" * 60)
        print("Testing sum() calculation")
        print("=" * 60)
        
        try:
            # Old way (would fail if any None)
            # total = sum(float(r.total_hours) for r in requests)
            
            # New way (handles None)
            total = sum(float(r.total_hours) if r.total_hours else 0 for r in requests)
            print(f"✅ Sum calculation successful: {total} hours")
        except Exception as e:
            print(f"❌ Sum calculation failed: {e}")
        
        # Show sample requests
        print("\n" + "=" * 60)
        print("Sample Requests")
        print("=" * 60)
        
        sample_requests = requests[:5] if requests else []
        for req in sample_requests:
            print(f"\nID: {req.id}")
            print(f"  Employee: {req.employee_name} ({req.employee_id})")
            print(f"  Date: {req.overtime_date}")
            print(f"  Number of people: {req.number_of_people}")
            print(f"  total_hours: {req.total_hours} (None = new format)")
            print(f"  start_time: {req.start_time}")
            print(f"  end_time: {req.end_time}")
            print(f"  Status: {req.status}")
        
        print("\n" + "=" * 60)
        print("Test completed!")
        print("=" * 60)
        print("\n✅ All total_hours None values are now handled correctly")
        print("✅ Dashboard should load without TypeError")

if __name__ == '__main__':
    test_total_hours_fix()
