"""
Test script for the Word Meaning API
Tests both single word and sentence explanations
"""

import requests
import json

# API endpoint (change this when deployed)
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test if the API is running"""
    print("=" * 50)
    print("Testing Health Check...")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✓ Health check passed!\n")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}\n")
        return False


def test_single_word(word):
    """Test single word explanation"""
    print("=" * 50)
    print(f"Testing Single Word: '{word}'")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/explain",
            json={"text": word}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        # Verify format
        if result.get("status") == "success":
            meaning = result.get("meaning", "")
            # Check if punctuation is removed
            has_punctuation = any(char in meaning for char in '.,!?;:"\'-')
            if has_punctuation:
                print("⚠ Warning: Response contains punctuation!")
            else:
                print("✓ No punctuation detected (Braille compatible)")
            print(f"✓ Word explanation received!\n")
            return True
        else:
            print(f"✗ Error status received\n")
            return False
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False


def test_sentence(sentence):
    """Test sentence/paragraph explanation"""
    print("=" * 50)
    print(f"Testing Sentence: '{sentence}'")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/explain",
            json={"text": sentence}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        # Verify format
        if result.get("status") == "success":
            meaning = result.get("meaning", "")
            # Check if punctuation is removed
            has_punctuation = any(char in meaning for char in '.,!?;:"\'-')
            if has_punctuation:
                print("⚠ Warning: Response contains punctuation!")
            else:
                print("✓ No punctuation detected (Braille compatible)")
            print(f"✓ Sentence explanation received!\n")
            return True
        else:
            print(f"✗ Error status received\n")
            return False
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False


def test_empty_input():
    """Test error handling with empty input"""
    print("=" * 50)
    print("Testing Empty Input (Error Handling)")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{BASE_URL}/explain",
            json={"text": ""}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✓ Correctly rejected empty input!\n")
            return True
        else:
            print("✗ Should return 400 for empty input\n")
            return False
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("Word Meaning API - Test Suite")
    print("=" * 50 + "\n")
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Single words
    test_words = ["serendipity", "ephemeral", "ubiquitous"]
    for word in test_words:
        results.append((f"Word: {word}", test_single_word(word)))
    
    # Test 3: Sentences
    test_sentences = [
        "The quick brown fox jumps over the lazy dog",
        "To be or not to be, that is the question"
    ]
    for sentence in test_sentences:
        results.append((f"Sentence: {sentence[:30]}...", test_sentence(sentence)))
    
    # Test 4: Empty input
    results.append(("Empty Input", test_empty_input()))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
