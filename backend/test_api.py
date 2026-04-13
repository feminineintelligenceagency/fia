"""
Quick script to test the RAG API endpoints.
Make sure the server is running first: uvicorn app.main:app --reload
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("=" * 80)
    print("Testing Health Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_patterns():
    """Test patterns listing endpoint."""
    print("=" * 80)
    print("Testing Patterns Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/patterns")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total Patterns: {data.get('count', 0)}")
    print(f"Patterns: {', '.join(data.get('patterns', [])[:5])}...\n")

def test_analyze(story: str):
    """Test the analyze endpoint with RAG."""
    print("=" * 80)
    print("Testing RAG Analysis Endpoint")
    print("=" * 80)
    print(f"User Story:\n{story}\n")

    response = requests.post(
        f"{API_URL}/analyze",
        json={"content": story},
        headers={"Content-Type": "application/json"}
    )

    print(f"Status: {response.status_code}\n")

    if response.status_code == 200:
        result = response.json()

        print("Patterns Detected:")
        print(f"   {', '.join(result.get('patterns_detected', []))}\n")

        print("AI Response:")
        print("-" * 80)
        print(result.get('content', 'No content'))
        print("-" * 80)

        findings = result.get('findings', [])
        if findings:
            print(f"\nFindings ({len(findings)}):")
            for i, finding in enumerate(findings, 1):
                print(f"\n[{finding['type'].upper()}] {finding['title']}")
                print(f"   {finding['description']}")
                if finding.get('matched_pattern'):
                    print(f"   Pattern: {finding['matched_pattern']}")
    else:
        print(f"Error: {response.text}")

def test_typologies():
    """Test GET /typologies."""
    print("=" * 80)
    print("Testing Typologies Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/typologies")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total Typologies: {len(data)}")
    names = [t.get("name", "?") for t in data[:5]]
    print(f"First 5: {', '.join(names)}\n")

def test_single_typology():
    """Test GET /typologies/{name}."""
    print("=" * 80)
    print("Testing Single Typology Endpoint")
    print("=" * 80)
    name = "Mr. Always Right"
    response = requests.get(f"{API_URL}/typologies/{name}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data.get('name')}")
        print(f"Summary: {str(data.get('summary', ''))[:120]}...\n")
    else:
        print(f"Error: {response.text}\n")

def test_abuse_flavors():
    """Test GET /abuse-flavors."""
    print("=" * 80)
    print("Testing Abuse Flavors Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/abuse-flavors")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total Flavors: {len(data)}")
    flavors = [f.get("Flavor", "?") for f in data[:5]]
    print(f"First 5: {', '.join(flavors)}\n")

def test_trauma_types():
    """Test GET /trauma-types."""
    print("=" * 80)
    print("Testing Trauma Types Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/trauma-types")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total Trauma Types: {len(data)}")
    names = [t.get("Name", "?") for t in data[:5]]
    print(f"First 5: {', '.join(names)}\n")

def test_vulnerability_types():
    """Test GET /vulnerability-types."""
    print("=" * 80)
    print("Testing Vulnerability Types Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/vulnerability-types")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total Vulnerability Types: {len(data)}")
    names = [v.get("name", "?") for v in data[:5]]
    print(f"First 5: {', '.join(names)}\n")

def test_search():
    """Test POST /search."""
    print("=" * 80)
    print("Testing Semantic Search Endpoint")
    print("=" * 80)
    response = requests.post(
        f"{API_URL}/search",
        params={"query": "guilt tripping behavior", "k": 3},
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Query: {data['query']}")
        print(f"Results: {data['count']}")
        for i, r in enumerate(data["results"][:3], 1):
            print(f"  {i}. score={r['relevance_score']:.4f}  {r['content'][:80]}...")
    print()

def test_explain_pattern():
    """Test POST /explain-pattern."""
    print("=" * 80)
    print("Testing Explain Pattern Endpoint")
    print("=" * 80)
    response = requests.post(
        f"{API_URL}/explain-pattern",
        json={"pattern_name": "Mr. Always Right"},
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Pattern: {data['pattern_name']}")
        print(f"Explanation: {data['explanation'][:200]}...")
        print(f"Red Flags: {data['key_red_flags'][:3]}")
        print(f"Safety Tips: {data['safety_tips'][:3]}")
    print()

def test_compare_patterns():
    """Test POST /compare-patterns."""
    print("=" * 80)
    print("Testing Compare Patterns Endpoint")
    print("=" * 80)
    response = requests.post(
        f"{API_URL}/compare-patterns",
        json={"pattern_a": "Mr. Always Right", "pattern_b": "The Subtle Saboteur"},
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Similarities: {data['similarities'][:2]}")
        print(f"Differences: {data['differences'][:2]}")
        print(f"Combined Danger: {data['combined_danger'][:200]}...")
    print()

def test_safety_plan():
    """Test POST /safety-plan."""
    print("=" * 80)
    print("Testing Safety Plan Endpoint")
    print("=" * 80)
    response = requests.post(
        f"{API_URL}/safety-plan",
        json={
            "story": "My partner controls everything I do and isolates me from friends.",
            "patterns_detected": ["Mr. Always Right"],
        },
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Immediate Steps: {data['immediate_steps'][:3]}")
        print(f"Long-term: {data['long_term_strategies'][:2]}")
        print(f"Resources: {data['resources'][:2]}")
        print(f"Affirmation: {data['affirmation'][:200]}")
    print()


# Test cases for analyze
TEST_STORIES = [
    {
        "name": "Control and Superiority",
        "story": "My partner always needs to be right about everything. When I share my opinion, he talks over me or dismisses what I say. He uses a patronizing tone and acts like I'm stupid. If I get upset, he says I'm being too sensitive and can't handle his honesty. Nothing I do is ever good enough."
    },
    {
        "name": "Charming to Controlling",
        "story": "He was so charming at first and made me feel special. But now he isolates me from my friends, checks my phone constantly, and gets angry when I don't do exactly what he wants. He says he loves me but I feel like I'm walking on eggshells."
    },
    {
        "name": "Gaslighting",
        "story": "He constantly denies things he said or did. When I bring up something hurtful, he says it never happened or that I'm remembering it wrong. Now I question my own memory and feel like I'm going crazy."
    }
]

if __name__ == "__main__":
    print("\nFIA RAG API Test Suite\n")

    try:
        # Test 1: Health check
        test_health()

        # Test 2: List patterns
        test_patterns()

        # Test 3: Data browsing endpoints
        test_typologies()
        test_single_typology()
        test_abuse_flavors()
        test_trauma_types()
        test_vulnerability_types()

        # Test 4: Semantic search
        test_search()

        # Test 5: AI-powered endpoints
        test_explain_pattern()
        test_compare_patterns()
        test_safety_plan()

        # Test 6: Analyze stories
        for i, test in enumerate(TEST_STORIES, 1):
            print(f"\n{'='*80}")
            print(f"Test Case {i}: {test['name']}")
            print(f"{'='*80}\n")
            test_analyze(test['story'])

            if i < len(TEST_STORIES):
                input("\nPress Enter to continue to next test case...")

        print("\n" + "=" * 80)
        print("All tests completed!")
        print("=" * 80)

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Make sure the server is running:")
        print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
