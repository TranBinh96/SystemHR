"""
Setup script for OKI Vietnam HR System
Helps with initial setup and configuration
"""
import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    if os.path.exists('.env'):
        print("\n✓ .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        print("\n📝 Creating .env file...")
        with open('.env.example', 'r') as example:
            with open('.env', 'w') as env:
                env.write(example.read())
        print("✓ .env file created from .env.example")
        print("⚠️  Please update .env with your actual configuration")
        return True
    else:
        print("❌ .env.example not found")
        return False

def initialize_database():
    """Initialize database tables"""
    print("\n🗄️  Initializing database...")
    response = input("Do you want to initialize the database now? (y/n): ")
    
    if response.lower() == 'y':
        try:
            # Use auto_setup_db instead of init_db
            subprocess.check_call([sys.executable, "auto_setup_db.py"])
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to initialize database")
            print("You can run 'python auto_setup_db.py' manually later")
            return False
    else:
        print("⚠️  Skipped database initialization")
        print("Run 'python auto_setup_db.py' when ready")
        return True

def main():
    """Main setup process"""
    print("="*60)
    print("OKI VIETNAM HR SYSTEM - Setup")
    print("="*60)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("\n❌ Setup failed at .env creation")
        sys.exit(1)
    
    # Initialize database
    initialize_database()
    
    print("\n" + "="*60)
    print("✓ Setup completed!")
    print("="*60)
    print("\nNext steps:")
    print("1. Update .env file with your configuration")
    print("2. Run 'python auto_setup_db.py' to setup database (auto-creates if not exists)")
    print("3. Run 'python app.py' to start the application")
    print("\nDefault login credentials:")
    print("  Admin: ADMIN / admin123")
    print("  User: EMP001 / password123")
    print("="*60)

if __name__ == '__main__':
    main()
