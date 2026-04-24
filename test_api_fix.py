#!/usr/bin/env python3
"""
Test script để kiểm tra API endpoints
"""

import requests
import json

def test_stats_api():
    """Test stats API"""
    print("🧪 Testing Stats API...")
    
    try:
        # Test local server
        url = "http://localhost:5000/admin/stats/data"
        
        # Test with parameters
        params = {
            'period': 'week',
            'date_from': '2026-04-21',
            'date_to': '2026-04-27'
        }
        
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ JSON Response OK")
                print(f"Success: {data.get('success')}")
                print(f"Period: {data.get('period')}")
                if 'summary' in data:
                    print(f"Total meals: {data['summary'].get('total')}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON Decode Error: {e}")
                print(f"Response text: {response.text[:200]}...")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running. Start with: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_auto_register_api():
    """Test auto-register API"""
    print("\n🧪 Testing Auto-Register API...")
    
    try:
        url = "http://localhost:5000/admin/auto-register/run"
        
        # This requires authentication, so it will likely fail
        response = requests.post(url)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code in [200, 401, 403]:
            try:
                data = response.json()
                print("✅ JSON Response OK")
                print(f"Success: {data.get('success')}")
                print(f"Message: {data.get('message')}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON Decode Error: {e}")
                print(f"Response text: {response.text[:200]}...")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running. Start with: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔧 API ENDPOINTS TEST")
    print("=" * 40)
    
    test_stats_api()
    test_auto_register_api()
    
    print("\n" + "=" * 40)
    print("📋 SUMMARY:")
    print("1. Stats API should return JSON with meal statistics")
    print("2. Auto-register API should return JSON (may need auth)")
    print("3. If server not running: python app.py")
    print("4. Check browser console for actual errors")

if __name__ == "__main__":
    main()