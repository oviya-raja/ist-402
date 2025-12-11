"""
Test script for EventRegistry API integration
Run this to verify the API is working correctly
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
app_dir = Path(__file__).parent
env_path = app_dir / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Test EventRegistry API
try:
    from eventregistry import EventRegistry, QueryEvents, RequestEventsInfo
    
    api_key = os.getenv('EVENTREGISTRY_API_KEY')
    if not api_key:
        print("❌ ERROR: EVENTREGISTRY_API_KEY not found in .env file")
        exit(1)
    
    print("=" * 80)
    print("TESTING EVENTREGISTRY API")
    print("=" * 80)
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    print()
    
    # Initialize EventRegistry
    er = EventRegistry(apiKey=api_key, allowUseOfArchive=False)
    print("✓ EventRegistry initialized")
    print()
    
    # Test 1: Simple query with keywords only
    print("TEST 1: Simple query with keywords only")
    print("-" * 80)
    try:
        q1 = QueryEvents(keywords=["artificial intelligence", "AI"])
        q1.setRequestedResult(RequestEventsInfo(sortBy="date", count=5))
        result1 = er.execQuery(q1)
        
        if isinstance(result1, dict) and 'error' in result1:
            print(f"❌ Error: {result1.get('error')}")
        else:
            events = result1.get('events', {}).get('results', [])
            print(f"✓ Success! Found {len(events)} events")
            if events:
                print(f"  First event: {events[0].get('title', {}).get('eng', 'N/A')}")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
    print()
    
    # Test 2: Query with concept URI
    print("TEST 2: Query with concept URI")
    print("-" * 80)
    try:
        concept_uri = er.getConceptUri("Artificial Intelligence")
        print(f"✓ Got concept URI: {concept_uri}")
        
        q2 = QueryEvents(conceptUri=concept_uri)
        q2.setRequestedResult(RequestEventsInfo(sortBy="date", count=5))
        result2 = er.execQuery(q2)
        
        if isinstance(result2, dict) and 'error' in result2:
            print(f"❌ Error: {result2.get('error')}")
        else:
            events = result2.get('events', {}).get('results', [])
            print(f"✓ Success! Found {len(events)} events")
            if events:
                print(f"  First event: {events[0].get('title', {}).get('eng', 'N/A')}")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
    print()
    
    # Test 3: Query with keywords and concept URI (like our implementation)
    print("TEST 3: Query with keywords AND concept URI")
    print("-" * 80)
    try:
        concept_uri = er.getConceptUri("Artificial Intelligence")
        q3 = QueryEvents(
            keywords=["AI Summit", "artificial intelligence"],
            conceptUri=concept_uri
        )
        q3.setRequestedResult(RequestEventsInfo(sortBy="date", count=5))
        result3 = er.execQuery(q3)
        
        if isinstance(result3, dict) and 'error' in result3:
            print(f"❌ Error: {result3.get('error')}")
            print(f"   Full error: {result3}")
        else:
            events = result3.get('events', {}).get('results', [])
            print(f"✓ Success! Found {len(events)} events")
            if events:
                for i, event in enumerate(events[:3], 1):
                    title = event.get('title', {}).get('eng', 'N/A')
                    date = event.get('eventDate', 'N/A')
                    print(f"  {i}. {title} ({date})")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        import traceback
        traceback.print_exc()
    print()
    
    # Test 4: Test our actual implementation method
    print("TEST 4: Testing our implementation method")
    print("-" * 80)
    try:
        from core.api_integration import EventRegistryAPI
        
        api = EventRegistryAPI()
        if not api.er:
            print("❌ EventRegistryAPI not initialized")
        else:
            result4 = api.get_ai_conferences(limit=5)
            if result4.get('conferences'):
                print(f"✓ Success! Found {len(result4['conferences'])} conferences")
                for i, conf in enumerate(result4['conferences'][:3], 1):
                    print(f"  {i}. {conf.get('title', 'N/A')}")
            else:
                print(f"⚠ No conferences found. Status: {result4.get('status')}")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        import traceback
        traceback.print_exc()
    print()
    
    print("=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)
    
except ImportError as e:
    print(f"❌ ERROR: {str(e)}")
    print("Install eventregistry: pip install eventregistry")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
