import requests
import json

# Test health check
print("=" * 50)
print("Testing Health Check...")
print("=" * 50)
response = requests.get("http://localhost:8000/")
print(json.dumps(response.json(), indent=2))

# Test word explanation
print("\n" + "=" * 50)
print("Testing Word Explanation: 'serendipity'")
print("=" * 50)
response = requests.post(
    "http://localhost:8000/explain",
    json={"text": "serendipity"}
)
print(f"Status Code: {response.status_code}")
print(json.dumps(response.json(), indent=2))

# Test sentence explanation
print("\n" + "=" * 50)
print("Testing Sentence Explanation")
print("=" * 50)
response = requests.post(
    "http://localhost:8000/explain",
    json={"text": "The quick brown fox jumps over the lazy dog"}
)
print(f"Status Code: {response.status_code}")
result = response.json()
print(json.dumps(result, indent=2))

# Check for punctuation
if result.get("status") == 200:
    meaning = result.get("meaning", "")
    has_punctuation = any(char in meaning for char in '.,!?;:"\'-')
    print(f"\nPunctuation removed: {not has_punctuation}")
    print(f"Braille-ready: {not has_punctuation}")
