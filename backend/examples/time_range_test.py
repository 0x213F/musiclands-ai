"""
Example usage of the Time Range Extraction system
Run with: pipenv run python examples/time_range_test.py
"""

import asyncio
import json
from datetime import datetime, timezone
from services.llm_prompt_service import llm_prompt_service
from models.llm.requests import ComplexLLMRequest, QueryType, TimeContext, LocationData

async def test_time_range_extraction():
    """Test the time range extraction functionality"""
    
    print("🚀 Testing Time Range Extraction System")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        {
            "query": "What should I do?",
            "description": "Immediate activity request"
        },
        {
            "query": "What should I do tonight?",
            "description": "Evening activity request"
        },
        {
            "query": "I need lunch ideas",
            "description": "Meal-specific request"
        },
        {
            "query": "Weekend activities",
            "description": "Weekend planning"
        },
        {
            "query": "Date ideas for Friday night",
            "description": "Specific day request"
        }
    ]
    
    # Example location (New York City)
    location = LocationData(
        lat=40.7128,
        lng=-74.0060,
        city="New York",
        country="USA"
    )
    
    for i, test_case in enumerate(test_queries):
        print(f"\n📝 Test {i+1}: {test_case['description']}")
        print(f"Query: \"{test_case['query']}\"")
        print("-" * 30)
        
        # Create request
        request = ComplexLLMRequest(
            query=test_case['query'],
            query_type=QueryType.TIME_RANGE_EXTRACTION,
            time_context=TimeContext(
                current_time=datetime.now(timezone.utc),
                timezone="America/New_York"
            ),
            location=location
        )
        
        try:
            # Process the query
            response = await llm_prompt_service.process_query(request)
            
            if response.error:
                print(f"❌ Error: {response.error}")
            else:
                # Pretty print the response
                response_data = response.response_data
                time_range = response_data['time_range']
                
                print(f"✅ Time Range: {time_range['description']}")
                print(f"   Start: {time_range['start_time']}")
                print(f"   End: {time_range['end_time']}")
                print(f"   Query Type: {response_data['query_type']}")
                print(f"   Confidence: {response_data['confidence']:.2f}")
                print(f"   Reasoning: {response_data['reasoning']}")
                print(f"   Processing Time: {response.processing_time_ms}ms")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

async def test_activity_recommendation():
    """Test activity recommendation with context"""
    
    print("\n\n🎯 Testing Activity Recommendation System")
    print("=" * 50)
    
    query = "I'm bored and want to do something fun this afternoon in the city"
    
    request = ComplexLLMRequest(
        query=query,
        query_type=QueryType.ACTIVITY_RECOMMENDATION,
        time_context=TimeContext(
            current_time=datetime.now(timezone.utc),
            timezone="America/New_York"
        ),
        location=LocationData(
            lat=40.7128,
            lng=-74.0060,
            city="New York",
            country="USA"
        )
    )
    
    print(f"Query: \"{query}\"")
    print("-" * 30)
    
    try:
        response = await llm_prompt_service.process_query(request)
        
        if response.error:
            print(f"❌ Error: {response.error}")
        else:
            print(f"✅ Recommendation:")
            print(response.response_data['recommendation'])
            print(f"\n   Processing Time: {response.processing_time_ms}ms")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

async def main():
    """Run all tests"""
    await test_time_range_extraction()
    await test_activity_recommendation()
    
    print("\n" + "=" * 50)
    print("🎉 Testing complete!")
    print("\n💡 To use this system:")
    print("1. Set your OPENAI_API_KEY in .env")
    print("2. Start the server: pipenv run python start.py")
    print("3. Make POST requests to /llm/time-range-extraction")
    print("4. Check http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    asyncio.run(main())