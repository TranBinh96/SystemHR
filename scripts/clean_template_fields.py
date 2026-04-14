#!/usr/bin/env python3
"""
Script to clean up email and level references from admin_users.html template
"""

import re

def clean_template():
    """Clean up email and level references from template"""
    template_path = 'templates/admin_users.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("Cleaning up template references...")
        print("="*60)
        
        # Remove email from data attributes
        content = re.sub(r'data-email="[^"]*"\s*', '', content)
        
        # Remove email from onclick function calls
        content = re.sub(r", '[^']*email[^']*'", '', content)
        
        # Remove email parameters from function definitions
        content = re.sub(r', email', '', content)
        content = re.sub(r'email, ', '', content)
        
        # Remove email form fields
        content = re.sub(r'<div[^>]*>\s*<label[^>]*>\s*Email\s*</label>.*?</div>', '', content, flags=re.DOTALL)
        
        # Remove email validation
        content = re.sub(r'&& !data\.email', '', content)
        content = re.sub(r'!data\.email \|\| ', '', content)
        content = re.sub(r'\|\| !data\.email', '', content)
        
        # Remove email from formData
        content = re.sub(r"formData\.append\('email'[^)]*\);\s*", '', content)
        
        # Remove email from data objects
        content = re.sub(r"email: [^,}]*,?\s*", '', content)
        
        # Remove email from search functionality
        content = re.sub(r'email\.includes\(searchTerm\) \|\| ', '', content)
        content = re.sub(r'\|\| email\.includes\(searchTerm\)', '', content)
        
        # Remove email dataset references
        content = re.sub(r'row\.dataset\.email = [^;]*;\s*', '', content)
        content = re.sub(r'card\.dataset\.email = [^;]*;\s*', '', content)
        content = re.sub(r'const email = [^;]*;\s*', '', content)
        
        print("✅ Cleaned up email references")
        
        # Write back to file
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Template updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == '__main__':
    clean_template()