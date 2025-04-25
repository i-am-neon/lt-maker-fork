#!/usr/bin/env python3
"""
Check and fix directory permissions for project creation
This script ensures the target directory exists and has proper permissions
"""

import sys
import os
import stat
import traceback

def ensure_directory_with_permissions(directory_path, create_if_missing=False):
    """
    Ensure a directory exists with proper permissions for project creation
    
    Args:
        directory_path: The directory to check/fix
        create_if_missing: Whether to create the directory if it doesn't exist
        
    Returns:
        True if directory exists and has proper permissions, False otherwise
    """
    try:
        # Remove any quotes that might be in the path
        directory_path = directory_path.replace('"', '')
        
        print(f"Checking directory: {directory_path}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Check if directory exists
        if not os.path.exists(directory_path):
            if create_if_missing:
                print(f"Creating directory: {directory_path}")
                os.makedirs(directory_path, exist_ok=True)
                print(f"Directory created: {directory_path}")
            else:
                print(f"Directory does not exist: {directory_path}")
                return False
        
        # Check if it's a directory
        if not os.path.isdir(directory_path):
            print(f"Path exists but is not a directory: {directory_path}")
            return False
            
        # On non-Windows platforms, set directory permissions
        if os.name != 'nt':
            try:
                # Get current permissions
                current_mode = os.stat(directory_path).st_mode
                print(f"Current permissions: {current_mode & 0o777:o}")
                
                # Set read/write/execute permissions for user and group
                new_mode = current_mode | stat.S_IRWXU | stat.S_IRWXG
                print(f"Setting permissions to: {new_mode & 0o777:o}")
                os.chmod(directory_path, new_mode)
                
                # Verify permissions were set
                updated_mode = os.stat(directory_path).st_mode
                print(f"Updated permissions: {updated_mode & 0o777:o}")
            except Exception as e:
                print(f"Error setting permissions: {e}")
                traceback.print_exc()
                # Continue even if permission setting fails
        
        # Test write permissions by creating a test file
        test_file_path = os.path.join(directory_path, '.permissions_test')
        try:
            with open(test_file_path, 'w') as f:
                f.write('test')
            os.remove(test_file_path)
            print(f"Write test successful in {directory_path}")
        except Exception as e:
            print(f"Write test failed in {directory_path}: {e}")
            traceback.print_exc()
            return False
            
        return True
    except Exception as e:
        print(f"Error checking directory: {e}")
        traceback.print_exc()
        return False

def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python check_directory_permissions.py <directory_path> [create_if_missing]")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    create_if_missing = False
    
    if len(sys.argv) >= 3:
        create_if_missing = sys.argv[2].lower() in ('true', 'yes', '1')
    
    success = ensure_directory_with_permissions(directory_path, create_if_missing)
    
    if success:
        print("Directory permissions check passed")
        sys.exit(0)
    else:
        print("Directory permissions check failed")
        sys.exit(1)

if __name__ == '__main__':
    main()