"""
Script to remove all references to admin_positions from HTML templates
"""
import os
import re

def remove_position_links_from_file(filepath):
    """Remove position-related menu items from a template file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Remove entire <li> blocks containing admin_positions links
        # This handles multi-line <li>...</li> blocks
        pattern1 = r'<li>\s*<a[^>]*url_for\([\'"]admin_positions[\'"]\)[^>]*>.*?</a>\s*</li>'
        content = re.sub(pattern1, '', content, flags=re.DOTALL)
        
        # Pattern 2: Remove standalone <a> tags with admin_positions
        pattern2 = r'<a[^>]*url_for\([\'"]admin_positions[\'"]\)[^>]*>.*?</a>'
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        
        # Check if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function to process all template files"""
    templates_dir = 'templates'
    modified_files = []
    
    print("=" * 60)
    print("REMOVING POSITION REFERENCES FROM TEMPLATES")
    print("=" * 60)
    
    # Walk through all template files
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                print(f"\nProcessing: {filepath}")
                
                if remove_position_links_from_file(filepath):
                    print(f"  OK Modified: {filepath}")
                    modified_files.append(filepath)
                else:
                    print(f"  - No changes needed")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total files modified: {len(modified_files)}")
    if modified_files:
        print("\nModified files:")
        for f in modified_files:
            print(f"  - {f}")
    print("\nAll position references have been removed from templates!")

if __name__ == '__main__':
    main()
