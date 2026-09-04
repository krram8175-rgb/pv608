#!/usr/bin/env python3
"""
Backend API Test for Units and Measurements Chapter Bank
Tests the specific requirements from the review request
"""

import requests
import json
import sys

# Backend URL from environment
BACKEND_URL = "https://line-by-line-13.preview.emergentagent.com/api"

def test_chapter_bank_units_and_measurements():
    """Test GET /api/chapter-bank/neet-physics-units-and-measurements"""
    print("\n" + "="*80)
    print("TEST: Chapter Bank - Units and Measurements")
    print("="*80)
    
    url = f"{BACKEND_URL}/chapter-bank/neet-physics-units-and-measurements"
    print(f"\nGET {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected status 200, got {response.status_code}")
            return False
        
        data = response.json()
        print(f"\nResponse structure:")
        print(f"  - Keys: {list(data.keys())}")
        
        # Test 1: Verify total_questions = 9
        total_questions = data.get('total_questions')
        print(f"\n1. Total Questions: {total_questions}")
        if total_questions != 9:
            print(f"   ❌ FAILED: Expected 9, got {total_questions}")
            return False
        print(f"   ✅ PASSED: total_questions = 9")
        
        # Test 2: Verify exactly 2 sections
        sections = data.get('sections', [])
        print(f"\n2. Number of Sections: {len(sections)}")
        if len(sections) != 2:
            print(f"   ❌ FAILED: Expected 2 sections, got {len(sections)}")
            return False
        print(f"   ✅ PASSED: Exactly 2 sections")
        
        # Test 3: Verify section topics and question counts
        print(f"\n3. Section Details:")
        expected_sections = {
            "Unit of Physical Quantities": 5,
            "Significant Figures": 4
        }
        
        for section in sections:
            topic = section.get('topic')
            questions = section.get('questions', [])
            question_count = len(questions)
            print(f"   - Topic: '{topic}', Questions: {question_count}")
            
            if topic not in expected_sections:
                print(f"     ❌ FAILED: Unexpected topic '{topic}'")
                return False
            
            expected_count = expected_sections[topic]
            if question_count != expected_count:
                print(f"     ❌ FAILED: Expected {expected_count} questions, got {question_count}")
                return False
            
            print(f"     ✅ PASSED: Topic and count correct")
        
        # Test 4: Verify "Significant Figures" section structure
        print(f"\n4. Significant Figures Section Details:")
        sf_section = None
        for section in sections:
            if section.get('topic') == "Significant Figures":
                sf_section = section
                break
        
        if not sf_section:
            print(f"   ❌ FAILED: 'Significant Figures' section not found")
            return False
        
        sf_questions = sf_section.get('questions', [])
        expected_answers = ['d', 'c', 'd', 'a']
        
        for i, question in enumerate(sf_questions):
            question_no = question.get('question_no')
            answer = question.get('answer')
            question_image = question.get('question_image')
            option_images = question.get('option_images', [])
            solution_image = question.get('solution_image')
            header_in_image = question.get('header_in_image')
            
            print(f"\n   Question {i+1}:")
            print(f"     - question_no: {question_no}")
            print(f"     - answer: {answer}")
            print(f"     - question_image: {question_image}")
            print(f"     - option_images count: {len(option_images)}")
            print(f"     - solution_image: {solution_image}")
            print(f"     - header_in_image: {header_in_image}")
            
            # Verify question_no is 1-4
            if question_no != i + 1:
                print(f"     ❌ FAILED: Expected question_no {i+1}, got {question_no}")
                return False
            
            # Verify answer matches expected
            if answer != expected_answers[i]:
                print(f"     ❌ FAILED: Expected answer '{expected_answers[i]}', got '{answer}'")
                return False
            
            # Verify question_image exists and follows pattern
            expected_q_image = f"sf_q{i+1}_question.png"
            if question_image != expected_q_image:
                print(f"     ❌ FAILED: Expected question_image '{expected_q_image}', got '{question_image}'")
                return False
            
            # Verify exactly 4 option_images
            if len(option_images) != 4:
                print(f"     ❌ FAILED: Expected 4 option_images, got {len(option_images)}")
                return False
            
            # Verify solution_image exists
            if not solution_image:
                print(f"     ❌ FAILED: solution_image is missing")
                return False
            
            # Verify header_in_image is true
            if header_in_image != True:
                print(f"     ❌ FAILED: Expected header_in_image=true, got {header_in_image}")
                return False
            
            print(f"     ✅ PASSED: All fields correct")
        
        print(f"\n✅ ALL TESTS PASSED for chapter bank endpoint")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: Request error - {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_chapter_image_endpoint():
    """Test GET /api/chapter-image/sf_q3_question.png"""
    print("\n" + "="*80)
    print("TEST: Chapter Image Endpoint")
    print("="*80)
    
    url = f"{BACKEND_URL}/chapter-image/sf_q3_question.png"
    print(f"\nGET {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected status 200, got {response.status_code}")
            return False
        
        content_type = response.headers.get('Content-Type', '')
        print(f"Content-Type: {content_type}")
        
        # Verify content-type is image
        if not content_type.startswith('image/'):
            print(f"❌ FAILED: Expected image content-type, got '{content_type}'")
            return False
        
        # Verify we got actual content
        content_length = len(response.content)
        print(f"Content Length: {content_length} bytes")
        
        if content_length == 0:
            print(f"❌ FAILED: Image content is empty")
            return False
        
        print(f"✅ PASSED: Image endpoint returns HTTP 200 with image content-type")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ FAILED: Request error - {e}")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error - {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("BACKEND API TESTING - Units and Measurements Verification")
    print("="*80)
    print(f"Backend URL: {BACKEND_URL}")
    
    results = []
    
    # Test 1: Chapter bank endpoint
    results.append(("Chapter Bank Endpoint", test_chapter_bank_units_and_measurements()))
    
    # Test 2: Chapter image endpoint
    results.append(("Chapter Image Endpoint", test_chapter_image_endpoint()))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("="*80)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
