import firebase_admin
from firebase_admin import auth
from datetime import datetime
from typing import Optional
from models.user import User, UserSignup, UserLogin
from services.firebase_client import firestore_client


class FirebaseAuthService:
    def __init__(self):
        self.db = firestore_client.db

    def create_user(self, user_data: UserSignup) -> User:
        """Create a new user with Firebase Auth"""
        try:
            # Create user in Firebase Auth
            firebase_user = auth.create_user(
                email=user_data.email,
                password=user_data.password,
                display_name=user_data.display_name
            )
            
            # Create user document in Firestore
            user_doc = {
                "uid": firebase_user.uid,
                "email": firebase_user.email,
                "display_name": firebase_user.display_name,
                "email_verified": firebase_user.email_verified,
                "created_at": datetime.now(),
                "last_login": None
            }
            
            if self.db:
                self.db.collection("users").document(firebase_user.uid).set(user_doc)
            
            return User(**user_doc)
            
        except auth.EmailAlreadyExistsError as e:
            print(f"Email already exists: {e}")
            raise ValueError("User with this email already exists")
        except ValueError as e:
            # Firebase raises ValueError for invalid arguments like password length
            print(f"Invalid argument: {e}")
            error_msg = str(e).lower()
            if "password" in error_msg:
                raise ValueError("Password must be at least 6 characters long")
            elif "email" in error_msg:
                raise ValueError("Invalid email address")
            else:
                raise ValueError(f"Invalid user data: {str(e)}")
        except Exception as e:
            print(f"Firebase user creation error: {e}")
            raise ValueError(f"Failed to create user: {str(e)}")

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            # Firebase Admin SDK doesn't have built-in password verification
            # We'll use Firebase Auth REST API for this
            import requests
            import os
            
            # Get Firebase Web API key from environment
            api_key = os.getenv("FIREBASE_WEB_API_KEY")
            if not api_key:
                print("Warning: FIREBASE_WEB_API_KEY not found in environment variables")
                return None
            
            # Firebase Auth REST API endpoint
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
            
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                auth_data = response.json()
                uid = auth_data.get("localId")
                
                # Get user from Firebase Auth
                firebase_user = auth.get_user(uid)
                
                # Update last login in Firestore
                user_doc = {
                    "uid": firebase_user.uid,
                    "email": firebase_user.email,
                    "display_name": firebase_user.display_name,
                    "email_verified": firebase_user.email_verified,
                    "created_at": datetime.now(),
                    "last_login": datetime.now()
                }
                
                if self.db:
                    self.db.collection("users").document(firebase_user.uid).update({
                        "last_login": datetime.now()
                    })
                
                return User(**user_doc)
            else:
                return None
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    def get_user_by_uid(self, uid: str) -> Optional[User]:
        """Get user by Firebase UID"""
        try:
            firebase_user = auth.get_user(uid)
            
            user_doc = {
                "uid": firebase_user.uid,
                "email": firebase_user.email,
                "display_name": firebase_user.display_name,
                "email_verified": firebase_user.email_verified,
                "created_at": datetime.now(),
                "last_login": None
            }
            
            # Try to get additional data from Firestore
            if self.db:
                doc = self.db.collection("users").document(uid).get()
                if doc.exists:
                    firestore_data = doc.to_dict()
                    user_doc.update(firestore_data)
            
            return User(**user_doc)
            
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            firebase_user = auth.get_user_by_email(email)
            return self.get_user_by_uid(firebase_user.uid)
        except auth.UserNotFoundError:
            return None

    def send_password_reset_email(self, email: str) -> bool:
        """Send password reset email"""
        try:
            # Generate password reset link
            link = auth.generate_password_reset_link(email)
            
            # In a real application, you would send this via your email service
            # For now, we'll just print it (you should implement proper email sending)
            print(f"Password reset link for {email}: {link}")
            
            return True
        except Exception as e:
            print(f"Error sending password reset: {e}")
            return False

    def update_user_password(self, uid: str, new_password: str) -> bool:
        """Update user password"""
        try:
            auth.update_user(uid, password=new_password)
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False

    def delete_user(self, uid: str) -> bool:
        """Delete user from Firebase Auth and Firestore"""
        try:
            # Delete from Firebase Auth
            auth.delete_user(uid)
            
            # Delete from Firestore
            if self.db:
                self.db.collection("users").document(uid).delete()
            
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def verify_id_token(self, id_token: str) -> Optional[dict]:
        """Verify Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None