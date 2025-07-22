import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

class FirestoreClient:
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize Firebase Admin SDK and Firestore client using base64 encoded credentials"""
        try:
            if firebase_admin._apps:
                self._db = firestore.client()
                return

            firebase_json_base64 = os.getenv("FIREBASE_JSON_BASE64")
            if not firebase_json_base64:
                self._db = None
                return
                
            firebase_json_str = base64.b64decode(firebase_json_base64).decode('utf-8')
            firebase_json = json.loads(firebase_json_str)
            cred = credentials.Certificate(firebase_json)
            firebase_admin.initialize_app(cred)
            self._db = firestore.client()
            
        except Exception as e:
            self._db = None

    @property
    def db(self):
        """Get the Firestore database client"""
        return self._db

    def is_available(self) -> bool:
        """Check if Firestore client is available"""
        return self._db is not None

# Global Firestore client instance
firestore_client = FirestoreClient()