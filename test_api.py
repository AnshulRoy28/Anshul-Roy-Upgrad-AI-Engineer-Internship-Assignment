#!/usr/bin/env python3
"""Quick API test script to verify the backend is working correctly."""

import requests
import json
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Active sessions: {data['active_sessions']}")
            print(f"   API key configured: {data['api_key_configured']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        print("   Make sure the API server is running: python api_server.py")
        return False

def test_parse_resume():
    """Test resume parsing."""
    print("\nTesting resume parsing...")
    
    # Simple LaTeX resume
    latex_content = r"""
\documentclass{article}
\begin{document}
\name{John Doe}
\email{john@example.com}
\section{Experience}
Senior Software Engineer at Tech Corp
\section{Skills}
Python, JavaScript, React
\end{document}
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/parse/resume",
            json={"latex_content": latex_content}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resume parsing passed")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Skills: {len(data.get('skills', []))} found")
            return True
        else:
            print(f"❌ Resume parsing failed: {response.status_code}")
            print(f"   {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Resume parsing failed: {str(e)}")
        return False

def test_parse_job():
    """Test job description parsing."""
    print("\nTesting job description parsing...")
    
    job_text = """
Senior Software Engineer

Requirements:
- 5+ years of experience
- Python and JavaScript expertise
- Strong problem-solving skills

Responsibilities:
- Lead development team
- Design scalable systems
- Mentor junior developers
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/parse/job",
            json={"job_text": job_text}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Job parsing passed")
            print(f"   Title: {data.get('title', 'N/A')}")
            print(f"   Requirements: {len(data.get('requirements', []))} found")
            return True
        else:
            print(f"❌ Job parsing failed: {response.status_code}")
            print(f"   {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Job parsing failed: {str(e)}")
        return False

def test_input_validation():
    """Test input validation."""
    print("\nTesting input validation...")
    
    # Test empty input
    try:
        response = requests.post(
            f"{BASE_URL}/parse/resume",
            json={"latex_content": ""}
        )
        if response.status_code == 400:
            print(f"✅ Empty input validation passed")
        else:
            print(f"⚠️  Empty input validation: unexpected status {response.status_code}")
    except Exception as e:
        print(f"❌ Empty input validation failed: {str(e)}")
        return False
    
    # Test too long input
    try:
        response = requests.post(
            f"{BASE_URL}/parse/resume",
            json={"latex_content": "x" * 100000}  # 100K chars
        )
        if response.status_code == 400:
            print(f"✅ Length validation passed")
            return True
        else:
            print(f"⚠️  Length validation: unexpected status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Length validation failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("AI Mock Interview Coach - API Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    
    if results[0][1]:  # Only continue if health check passed
        results.append(("Resume Parsing", test_parse_resume()))
        results.append(("Job Parsing", test_parse_job()))
        results.append(("Input Validation", test_input_validation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The API is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
