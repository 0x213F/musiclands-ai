"""
Location Intelligence System Prompt
Handles complex queries with location data, events, travel times, and user context
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import json

class LocationIntelligencePrompt:
    """Advanced prompt template for location-based recommendations and queries"""
    
    @staticmethod
    def build_comprehensive_prompt(
        user_query: str,
        current_time: datetime,
        user_location: Optional[Dict[str, float]],
        locations_data: List[Dict[str, Any]],
        travel_time_matrix: Dict[str, Dict[str, int]],
        user_context: Optional[Dict[str, Any]] = None,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build a comprehensive prompt for location-based intelligence
        
        Args:
            user_query: The user's question/request
            current_time: Current datetime
            user_location: User's current GPS coordinates
            locations_data: List of location data with events
            travel_time_matrix: Travel times between locations in minutes
            user_context: Additional user context (mood, group size, etc.)
            user_preferences: User preferences (music genres, activity types, etc.)
            
        Returns:
            Formatted comprehensive prompt
        """
        
        # Format current time and context
        time_info = f"Current time: {current_time.strftime('%A, %B %d, %Y at %I:%M %p')}"
        
        # Format user location
        user_location_info = ""
        if user_location:
            user_location_info = f"""
USER LOCATION:
Current GPS: {user_location.get('lat', 'N/A')}, {user_location.get('lng', 'N/A')}
"""
        
        # Format locations and events data
        locations_info = LocationIntelligencePrompt._format_locations_data(locations_data)
        
        # Format travel time matrix
        travel_info = LocationIntelligencePrompt._format_travel_matrix(travel_time_matrix)
        
        # Format user context and preferences
        context_info = LocationIntelligencePrompt._format_user_context(user_context, user_preferences)
        
        prompt = f"""You are an expert location intelligence assistant for a music festival/event app. You help users make smart decisions about where to go, what to see, and how to optimize their experience based on real-time location data, event schedules, and travel times.

CURRENT CONTEXT:
{time_info}
{user_location_info}

USER QUERY: "{user_query}"

{locations_info}

{travel_info}

{context_info}

INSTRUCTIONS:
1. Analyze the user's query in the context of all available location and event data
2. Consider current time, user location, travel times, and event schedules
3. Provide personalized recommendations based on user preferences and context
4. Factor in practical considerations like travel time, crowd levels, and timing
5. Be specific about locations, times, and logistics
6. Consider the user's current situation (energy level, group dynamics, etc.)

RESPONSE GUIDELINES:
- Give actionable, specific recommendations with clear reasoning
- Include travel time estimates and logistics when relevant
- Mention alternative options if applicable
- Consider the user's current mood and energy level
- Factor in crowd dynamics and wait times
- Prioritize experiences that align with user preferences
- Be conversational and helpful, not robotic
- Include practical tips (best routes, timing, what to bring, etc.)

RESPONSE FORMAT:
Provide your recommendation as natural, conversational text. Include:
1. Primary recommendation with specific reasoning
2. Logistics (travel time, directions, timing)
3. Alternative options if applicable
4. Pro tips for the best experience
5. What to expect (crowds, atmosphere, etc.)

Remember: You have complete information about all locations, events, and travel times. Use this data intelligently to provide the most helpful response possible.

Now provide your recommendation:"""

        return prompt
    
    @staticmethod
    def _format_locations_data(locations_data: List[Dict[str, Any]]) -> str:
        """Format locations and events data for the prompt"""
        if not locations_data:
            return "LOCATION DATA: No location data available."
        
        formatted_data = ["LOCATION & EVENT DATA:"]
        
        for i, location in enumerate(locations_data, 1):
            location_id = location.get('id', f'location_{i}')
            name = location.get('name', 'Unknown Location')
            description = location.get('description', '')
            coordinates = location.get('coordinates', {})
            amenities = location.get('amenities', [])
            capacity = location.get('capacity', 'Unknown')
            current_crowd = location.get('current_crowd_level', 'Unknown')
            
            # Format location info
            formatted_data.append(f"\n{i}. {name} (ID: {location_id})")
            if description:
                formatted_data.append(f"   Description: {description}")
            if coordinates:
                formatted_data.append(f"   GPS: {coordinates.get('lat')}, {coordinates.get('lng')}")
            if capacity != 'Unknown':
                formatted_data.append(f"   Capacity: {capacity}")
            if current_crowd != 'Unknown':
                formatted_data.append(f"   Current crowd level: {current_crowd}")
            if amenities:
                formatted_data.append(f"   Amenities: {', '.join(amenities)}")
            
            # Format events at this location
            events = location.get('events', [])
            if events:
                formatted_data.append(f"   EVENTS:")
                for event in events:
                    event_name = event.get('name', 'Unnamed Event')
                    start_time = event.get('start_time', 'TBD')
                    end_time = event.get('end_time', 'TBD')
                    event_type = event.get('type', 'Event')
                    artist = event.get('artist', '')
                    genre = event.get('genre', '')
                    description = event.get('description', '')
                    vip_only = event.get('vip_only', False)
                    age_restriction = event.get('age_restriction', '')
                    expected_crowd = event.get('expected_crowd', 'Unknown')
                    
                    event_info = f"     • {event_name}"
                    if artist:
                        event_info += f" - {artist}"
                    if start_time != 'TBD' and end_time != 'TBD':
                        event_info += f" ({start_time} - {end_time})"
                    formatted_data.append(event_info)
                    
                    if genre:
                        formatted_data.append(f"       Genre: {genre}")
                    if description:
                        formatted_data.append(f"       Description: {description}")
                    if vip_only:
                        formatted_data.append(f"       VIP ONLY")
                    if age_restriction:
                        formatted_data.append(f"       Age restriction: {age_restriction}")
                    if expected_crowd != 'Unknown':
                        formatted_data.append(f"       Expected crowd: {expected_crowd}")
            else:
                formatted_data.append(f"   No events scheduled")
        
        return '\n'.join(formatted_data)
    
    @staticmethod
    def _format_travel_matrix(travel_time_matrix: Dict[str, Dict[str, int]]) -> str:
        """Format travel time matrix for the prompt"""
        if not travel_time_matrix:
            return "TRAVEL TIMES: No travel time data available."
        
        formatted_data = ["TRAVEL TIME MATRIX (in minutes):"]
        formatted_data.append("Note: Travel times include walking between locations and any wait times.")
        
        # Create a readable matrix format
        locations = list(travel_time_matrix.keys())
        
        for from_location in locations:
            travel_times = travel_time_matrix.get(from_location, {})
            if travel_times:
                formatted_data.append(f"\nFrom {from_location}:")
                for to_location, minutes in travel_times.items():
                    if from_location != to_location:  # Don't show travel to same location
                        formatted_data.append(f"  → {to_location}: {minutes} minutes")
        
        return '\n'.join(formatted_data)
    
    @staticmethod
    def _format_user_context(user_context: Optional[Dict[str, Any]], user_preferences: Optional[Dict[str, Any]]) -> str:
        """Format user context and preferences"""
        sections = []
        
        if user_context:
            context_info = ["USER CONTEXT:"]
            for key, value in user_context.items():
                context_info.append(f"  {key.replace('_', ' ').title()}: {value}")
            sections.append('\n'.join(context_info))
        
        if user_preferences:
            pref_info = ["USER PREFERENCES:"]
            for key, value in user_preferences.items():
                if isinstance(value, list):
                    pref_info.append(f"  {key.replace('_', ' ').title()}: {', '.join(value)}")
                else:
                    pref_info.append(f"  {key.replace('_', ' ').title()}: {value}")
            sections.append('\n'.join(pref_info))
        
        return '\n\n'.join(sections) if sections else ""
    
    @staticmethod
    def get_sample_location_data() -> Dict[str, Any]:
        """Return sample location and event data for testing"""
        return {
            "locations": [
                {
                    "id": "main_stage",
                    "name": "Main Stage",
                    "description": "Primary performance venue with state-of-the-art sound system",
                    "coordinates": {"lat": 40.7589, "lng": -73.9851},
                    "capacity": 10000,
                    "current_crowd_level": "High",
                    "amenities": ["VIP viewing", "Food vendors", "Merchandise", "Restrooms"],
                    "events": [
                        {
                            "name": "Headliner Performance",
                            "artist": "Electric Dreams",
                            "genre": "Electronic",
                            "start_time": "9:00 PM",
                            "end_time": "11:00 PM",
                            "description": "High-energy electronic set with stunning visuals",
                            "expected_crowd": "Very High",
                            "vip_only": False
                        }
                    ]
                },
                {
                    "id": "acoustic_garden",
                    "name": "Acoustic Garden",
                    "description": "Intimate outdoor venue perfect for acoustic performances",
                    "coordinates": {"lat": 40.7505, "lng": -73.9934},
                    "capacity": 2000,
                    "current_crowd_level": "Medium",
                    "amenities": ["Seating area", "Coffee stand", "Quiet zone"],
                    "events": [
                        {
                            "name": "Sunset Session",
                            "artist": "Folk Stories",
                            "genre": "Folk",
                            "start_time": "6:30 PM",
                            "end_time": "8:00 PM",
                            "description": "Acoustic storytelling as the sun sets",
                            "expected_crowd": "Low",
                            "vip_only": False
                        }
                    ]
                },
                {
                    "id": "food_court",
                    "name": "Festival Food Court",
                    "description": "Diverse food options from local vendors",
                    "coordinates": {"lat": 40.7549, "lng": -73.9840},
                    "capacity": 5000,
                    "current_crowd_level": "Medium",
                    "amenities": ["Multiple food vendors", "Seating", "Vegetarian options", "Bar"],
                    "events": [
                        {
                            "name": "Late Night Eats",
                            "type": "Food Service",
                            "start_time": "10:00 PM",
                            "end_time": "2:00 AM",
                            "description": "Extended food service for late night festival goers"
                        }
                    ]
                }
            ],
            "travel_time_matrix": {
                "main_stage": {
                    "acoustic_garden": 8,
                    "food_court": 5,
                    "main_entrance": 3
                },
                "acoustic_garden": {
                    "main_stage": 8,
                    "food_court": 12,
                    "main_entrance": 15
                },
                "food_court": {
                    "main_stage": 5,
                    "acoustic_garden": 12,
                    "main_entrance": 7
                }
            },
            "user_context": {
                "energy_level": "Medium",
                "group_size": 3,
                "group_vibe": "Social and fun-loving",
                "time_at_festival": "3 hours",
                "last_meal": "2 hours ago"
            },
            "user_preferences": {
                "music_genres": ["Electronic", "Indie", "Alternative"],
                "activity_types": ["Live music", "Food", "Social activities"],
                "crowd_preference": "Medium crowds",
                "walking_tolerance": "Moderate"
            }
        }
    
    @staticmethod
    def get_example_queries() -> Dict[str, str]:
        """Return example queries for testing the system"""
        return {
            "what_should_i_do": "What should I do right now?",
            "food_recommendations": "I'm getting hungry, where should I eat?",
            "music_discovery": "What's the best music happening in the next hour?",
            "crowd_avoidance": "I want to avoid big crowds, what do you recommend?",
            "group_planning": "We're a group of 3 looking for something fun and social",
            "time_optimization": "I have 45 minutes before the headliner, what should I do?",
            "location_logistics": "How do I get from here to the main stage quickly?",
            "event_planning": "Plan my evening around electronic music",
            "energy_management": "I'm getting tired but don't want to miss good music",
            "discovery": "What's happening that I might not know about?"
        }