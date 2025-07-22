# Musiclands AI Backend

FastAPI backend server for the Musiclands AI mobile application with Firebase authentication and Firestore database.

## Setup

1. **Install dependencies using pipenv:**
   ```bash
   pipenv install
   ```

2. **Copy environment variables:**
   ```bash
   cp .env.example .env
   ```

3. **Configure your environment variables in `.env`:**
   - Set your desired `PORT` (default: 8000)
   - Set your `JWT_SECRET_KEY` (generate a strong secret key for production)
   - Add your Firebase service account JSON as base64 in `FIREBASE_JSON_BASE64`
   - Add API keys for AI services when ready

## Firebase Setup

1. **Create a Firebase project** at https://console.firebase.google.com/
2. **Enable Firestore Database** in your Firebase project
3. **Create a service account:**
   - Go to Project Settings → Service Accounts
   - Generate a new private key (JSON file)
4. **Encode the JSON file to base64:**
   ```bash
   base64 -i path/to/your-service-account.json
   ```
5. **Add the base64 string to your `.env` file** as `FIREBASE_JSON_BASE64`

## Running the Server

### Option 1: Using the startup script
```bash
pipenv run python start.py
```

### Option 2: Using uvicorn directly
```bash
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using Python directly
```bash
pipenv run python main.py
```

## API Endpoints

### Public Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check endpoint with service status
- `POST /auth/register` - Register new user with Firebase Auth
- `POST /auth/login` - Login user with email/password
- `POST /auth/verify-token` - Verify Firebase ID token

### User Management Endpoints
- `GET /auth/user/{uid}` - Get user by Firebase UID
- `GET /auth/user/email/{email}` - Get user by email
- `POST /auth/password-reset` - Send password reset email
- `POST /auth/password-update` - Update user password
- `DELETE /auth/user/{uid}` - Delete user account

### Chat Endpoints (ChatGPT Integration)
- `POST /chat` - Simple chat with ChatGPT (personalized if authenticated)
- `POST /chat/music` - Music-specialized chat endpoint
- `POST /chat/conversation` - Multi-turn conversation endpoint

### Advanced LLM Query Endpoints
- `POST /llm/time-range-extraction` - Extract time ranges from user queries
- `POST /llm/activity-recommendation` - Get contextual activity recommendations
- `POST /llm/music-discovery` - Advanced music discovery with context
- `POST /llm/complex-query` - Process any complex query with full context
- `POST /llm/batch` - Process multiple queries in batch (sequential or parallel)
- `GET /llm/example-queries` - Get example queries for testing

### Festival Management Endpoints
- `POST /festival/artists` - Create new artist
- `GET /festival/artists` - List artists with filtering
- `GET /festival/artists/search/{term}` - Search artists by name
- `POST /festival/stages` - Create new stage location
- `GET /festival/stages` - List stages with filtering
- `POST /festival/performances` - Create new performance
- `GET /festival/performances` - List performances with filtering
- `GET /festival/schedule` - Get complete festival schedule
- `GET /festival/stats` - Get festival statistics

## Authentication

The API uses Firebase Authentication with Firebase ID tokens:

1. **Register or login** to get a Firebase ID token from your client app
2. **Include the token** in the Authorization header:
   ```
   Authorization: Bearer <firebase-id-token>
   ```

## ChatGPT Integration

The API includes ChatGPT integration for AI-powered responses:

- **Basic Chat**: Send any message and get an AI response
- **Music Chat**: Specialized for music-related queries with enhanced context
- **Conversations**: Support for multi-turn conversations with conversation history

All chat endpoints support optional authentication for personalized responses.

## Advanced LLM Query System

The API features a sophisticated LLM query system for handling complex requests with contextual information:

### Time Range Extraction
Analyzes user queries to determine relevant time ranges for activities:
```json
{
    "query": "What should I do tonight?",
    "location": {"lat": 40.7128, "lng": -74.0060, "city": "New York"},
    "timezone": "America/New_York"
}
```

Returns structured time range data with confidence scores and reasoning.

### Activity Recommendations
Provides contextual activity suggestions based on:
- Current time and day
- User location (GPS coordinates)
- Weather conditions (if integrated)
- User preferences and history

### Batch Processing
Process multiple LLM queries efficiently:
- Sequential or parallel processing
- Configurable concurrency limits
- Comprehensive error handling
- Processing time metrics

### Context-Aware Responses
All advanced LLM endpoints support:
- GPS location context
- Time zone awareness
- User authentication for personalization
- Query history and preferences

## Documentation

Once the server is running, you can access:
- Interactive API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | 8000 |
| `HOST` | Server host | 0.0.0.0 |
| `ENVIRONMENT` | Runtime environment | development |
| `FIREBASE_JSON_BASE64` | Base64 encoded Firebase service account JSON | - |
| `FIREBASE_WEB_API_KEY` | Firebase Web API key for authentication | - |
| `OPENAI_API_KEY` | OpenAI API key for ChatGPT | - |
| `ANTHROPIC_API_KEY` | Anthropic API key (optional) | - |

## Database Structure

The app uses Firestore with the following collections:
- `users` - User profiles and authentication data
- `artists` - Artist/performer information with genres and social media
- `stages` - Stage locations with GPS coordinates and amenities
- `performances` - Performance schedules with artist and stage relationships

### Festival Data Model
- **Artists**: Name, genres, bio, social media, popularity score
- **Stages**: Name, type, GPS location, capacity, amenities, technical specs
- **Performances**: Artist-stage relationships with start/end times, descriptions
- **Relationships**: Performances link Artists to Stages with temporal data

## Development

The server runs in development mode with auto-reload when `ENVIRONMENT=development`.