import os
import jwt
from datetime import datetime, timedelta
from typing import Optional
from models.user import User, TokenPayload, AuthToken


class JWTService:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours

    def create_access_token(self, user: User) -> AuthToken:
        """Create JWT access token for user"""
        try:
            now = datetime.utcnow()
            expire = now + timedelta(minutes=self.access_token_expire_minutes)
            
            payload = {
                "sub": user.uid,  # subject (user ID)
                "email": user.email,
                "exp": expire,
                "iat": now,
                "type": "access"
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            
            return AuthToken(
                access_token=token,
                token_type="bearer",
                expires_in=self.access_token_expire_minutes * 60  # convert to seconds
            )
        except Exception as e:
            raise ValueError(f"Failed to create access token: {str(e)}")

    def verify_token(self, token: str) -> Optional[TokenPayload]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if token is still valid
            exp = payload.get("exp")
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                return None
            
            return TokenPayload(
                sub=payload.get("sub"),
                exp=payload.get("exp"),
                iat=payload.get("iat"),
                email=payload.get("email")
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
        except Exception as e:
            print(f"Token verification error: {e}")
            return None

    def refresh_token(self, user: User) -> AuthToken:
        """Create a new access token for user (refresh)"""
        return self.create_access_token(user)

    def revoke_token(self, token: str) -> bool:
        """Revoke a token (add to blacklist)"""
        # In a production app, you'd want to maintain a blacklist of revoked tokens
        # For simplicity, we'll just return True here
        # You could store revoked tokens in Redis or database
        return True