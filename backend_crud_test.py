#!/usr/bin/env python3
"""
Test CRUD operations for questions endpoint
"""

import requests
import json
import sys
from pathlib import Path

# Load backend URL from frontend .env
env_file = Path("/app/frontend/.env")
BACKEND_URL = None
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line.startswith("REACT_APP_BACKEND_URL="):
            BACKEND_URL = line.split("=", 1)[1].strip()
            break

if not BACKEND_URL:
    print("❌ ERROR: Could not find REACT_APP_BACKEND_URL in /app/frontend/.env")
    sys.exit(1)

API_BASE = f"{BACKEND_URL}/api"
print(f"🔍 Testing CRUD operations at: {API_BASE}\n")

tests_passed = 0
tests_failed = 0

print("=" * 70)
print("QUESTION CRUD TESTS")
print("=" * 70)
print()

# Test 1: Create a new question
print("1️⃣  Testing CREATE question (POST /api/questions)...")
new_question = {
    "subject": "physics",
    "pattern": "mcq",
    "chapter": "Test Chapter",
    "difficulty": "Understanding",
    "marks": 1,
    "question": "Test question for CRUD operations?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A",
    "solution": "This is a test solution",
    "teacher_note": "Test note"
}

try:
    response = requests.post(f"{API_BASE}/questions", json=new_question, timeout=10)
    if response.status_code == 200:
        created_question = response.json()
        question_id = created_question.get("id")
        if question_id:
            print(f"✅ CREATE question - Question created with ID: {question_id}")
            tests_passed += 1
        else:
            print(f"❌ CREATE question - No ID in response")
            tests_failed += 1
            question_id = None
    else:
        print(f"❌ CREATE question - Status {response.status_code}: {response.text[:200]}")
        tests_failed += 1
        question_id = None
except Exception as e:
    print(f"❌ CREATE question - Exception: {str(e)}")
    tests_failed += 1
    question_id = None
print()

# Test 2: Read the created question
if question_id:
    print("2️⃣  Testing READ question (GET /api/questions)...")
    try:
        response = requests.get(f"{API_BASE}/questions?subject=physics", timeout=10)
        if response.status_code == 200:
            questions = response.json()
            found = any(q.get("id") == question_id for q in questions)
            if found:
                print(f"✅ READ question - Found created question in list")
                tests_passed += 1
            else:
                print(f"❌ READ question - Created question not found in list")
                tests_failed += 1
        else:
            print(f"❌ READ question - Status {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ READ question - Exception: {str(e)}")
        tests_failed += 1
    print()

# Test 3: Update the question
if question_id:
    print("3️⃣  Testing UPDATE question (PUT /api/questions/{id})...")
    update_data = {
        "question": "Updated test question?",
        "difficulty": "Application"
    }
    try:
        response = requests.put(f"{API_BASE}/questions/{question_id}", json=update_data, timeout=10)
        if response.status_code == 200:
            updated_question = response.json()
            if updated_question.get("question") == "Updated test question?" and updated_question.get("difficulty") == "Application":
                print(f"✅ UPDATE question - Question updated successfully")
                tests_passed += 1
            else:
                print(f"❌ UPDATE question - Update not reflected in response")
                tests_failed += 1
        else:
            print(f"❌ UPDATE question - Status {response.status_code}: {response.text[:200]}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ UPDATE question - Exception: {str(e)}")
        tests_failed += 1
    print()

# Test 4: Delete the question
if question_id:
    print("4️⃣  Testing DELETE question (DELETE /api/questions/{id})...")
    try:
        response = requests.delete(f"{API_BASE}/questions/{question_id}", timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("deleted") == True:
                print(f"✅ DELETE question - Question deleted successfully")
                tests_passed += 1
            else:
                print(f"❌ DELETE question - Unexpected response: {result}")
                tests_failed += 1
        else:
            print(f"❌ DELETE question - Status {response.status_code}: {response.text[:200]}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ DELETE question - Exception: {str(e)}")
        tests_failed += 1
    print()

# Test 5: Verify deletion
if question_id:
    print("5️⃣  Testing VERIFY deletion (GET /api/questions)...")
    try:
        response = requests.get(f"{API_BASE}/questions?subject=physics", timeout=10)
        if response.status_code == 200:
            questions = response.json()
            found = any(q.get("id") == question_id for q in questions)
            if not found:
                print(f"✅ VERIFY deletion - Question no longer in list")
                tests_passed += 1
            else:
                print(f"❌ VERIFY deletion - Question still exists after deletion")
                tests_failed += 1
        else:
            print(f"❌ VERIFY deletion - Status {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ VERIFY deletion - Exception: {str(e)}")
        tests_failed += 1
    print()

# Summary
print("=" * 70)
print("CRUD TEST SUMMARY")
print("=" * 70)
print(f"✅ Passed: {tests_passed}")
print(f"❌ Failed: {tests_failed}")
print(f"📊 Total:  {tests_passed + tests_failed}")
print()

if tests_failed > 0:
    print("⚠️  Some CRUD operations failed")
    sys.exit(1)
else:
    print("🎉 All CRUD operations passed!")
    sys.exit(0)
