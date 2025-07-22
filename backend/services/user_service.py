from datetime import datetime
from typing import Optional
from models.user import User, UserCreate, UserUpdate
from services.firebase_client import firestore_client
from google.cloud.firestore_v1.base_query import FieldFilter

class UserService:
    def __init__(self):
        self.collection_name = "users"

    def create_user(self, uid: str, user_data: UserCreate) -> Optional[User]:
        """Create a new user in Firestore"""
        try:
            if not firestore_client.is_available():
                return None

            db = firestore_client.db
            user_ref = db.collection(self.collection_name).document(uid)
            
            # Check if user already exists
            if user_ref.get().exists:
                return self.get_user(uid)

            now = datetime.utcnow()
            user_dict = {
                "uid": uid,
                "email": user_data.email,
                "display_name": user_data.display_name,
                "photo_url": None,
                "created_at": now,
                "updated_at": now,
                "is_premium": False
            }

            user_ref.set(user_dict)
            return User(**user_dict)

        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user(self, uid: str) -> Optional[User]:
        """Get user by UID"""
        try:
            if not firestore_client.is_available():
                return None

            db = firestore_client.db
            user_ref = db.collection(self.collection_name).document(uid)
            user_doc = user_ref.get()

            if user_doc.exists:
                return User(**user_doc.to_dict())
            return None

        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        try:
            if not firestore_client.is_available():
                return None

            db = firestore_client.db
            users_ref = db.collection(self.collection_name)
            query = users_ref.where(filter=FieldFilter("email", "==", email))
            docs = query.limit(1).stream()

            for doc in docs:
                return User(**doc.to_dict())
            return None

        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    def update_user(self, uid: str, user_data: UserUpdate) -> Optional[User]:
        """Update user data"""
        try:
            if not firestore_client.is_available():
                return None

            db = firestore_client.db
            user_ref = db.collection(self.collection_name).document(uid)

            if not user_ref.get().exists:
                return None

            update_data = {}
            if user_data.display_name is not None:
                update_data["display_name"] = user_data.display_name
            if user_data.photo_url is not None:
                update_data["photo_url"] = user_data.photo_url
            if user_data.is_premium is not None:
                update_data["is_premium"] = user_data.is_premium

            update_data["updated_at"] = datetime.utcnow()

            user_ref.update(update_data)
            return self.get_user(uid)

        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    def delete_user(self, uid: str) -> bool:
        """Delete user from Firestore"""
        try:
            if not firestore_client.is_available():
                return False

            db = firestore_client.db
            user_ref = db.collection(self.collection_name).document(uid)
            user_ref.delete()
            return True

        except Exception as e:
            print(f"Error deleting user: {e}")
            return False