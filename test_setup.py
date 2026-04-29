"""Quick setup verification script."""
import sys
import os

def check_dependencies():
    """Check if required packages are installed."""
    print("🔍 Checking dependencies...")
    
    try:
        import google.genai
        print("   ✅ google-generativeai installed")
    except ImportError:
        print("   ❌ google-generativeai not found")
        return False
    
    try:
        import dotenv
        print("   ✅ python-dotenv installed")
    except ImportError:
        print("   ❌ python-dotenv not found")
        return False
    
    return True


def check_api_key():
    """Check if API key is configured."""
    print("\n🔑 Checking API key...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("   ❌ GOOGLE_API_KEY not found in .env")
        print("   📝 Create a .env file with your API key:")
        print("      GOOGLE_API_KEY=your_key_here")
        return False
    
    if api_key == "your_api_key_here":
        print("   ⚠️  GOOGLE_API_KEY is still the placeholder value")
        print("   📝 Replace it with your actual API key")
        return False
    
    print(f"   ✅ API key found (starts with: {api_key[:10]}...)")
    return True


def check_structure():
    """Check if project structure is correct."""
    print("\n📁 Checking project structure...")
    
    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "prompts/profiler.md",
        "prompts/interviewer.md",
        "prompts/turn_evaluator.md",
        "prompts/coach.md",
        "agents/__init__.py",
        "state/__init__.py",
        "tools/__init__.py",
    ]
    
    all_good = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} missing")
            all_good = False
    
    return all_good


def test_imports():
    """Test if all modules can be imported."""
    print("\n🔧 Testing imports...")
    
    try:
        import config
        print("   ✅ config module")
    except Exception as e:
        print(f"   ❌ config module: {e}")
        return False
    
    try:
        import state
        print("   ✅ state module")
    except Exception as e:
        print(f"   ❌ state module: {e}")
        return False
    
    try:
        import agents
        print("   ✅ agents module")
    except Exception as e:
        print(f"   ❌ agents module: {e}")
        return False
    
    try:
        import tools
        print("   ✅ tools module")
    except Exception as e:
        print(f"   ❌ tools module: {e}")
        return False
    
    return True


def main():
    """Run all checks."""
    print("\n" + "=" * 60)
    print("🚀 AI Mock Interview Coach - Setup Verification")
    print("=" * 60 + "\n")
    
    checks = [
        ("Dependencies", check_dependencies),
        ("API Key", check_api_key),
        ("Project Structure", check_structure),
        ("Module Imports", test_imports),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {name}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✨ All checks passed! You're ready to run:")
        print("   python main.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("   Then run this script again to verify.")
    
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
