from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import User, TokenPayload
from services.jwt_service import JWTService
from services.user_service import UserService

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)
jwt_service = JWTService()
user_service = UserService()

class AuthService:
    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
        """Get current authenticated user from JWT token"""
        token = credentials.credentials
        token_payload = jwt_service.verify_token(token)
        
        if not token_payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = user_service.get_user(token_payload.sub)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user

    @staticmethod
    def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Security(security_optional)) -> Optional[User]:
        """Get current user if token is provided, otherwise return None"""
        if not credentials:
            return None
        
        try:
            return AuthService.get_current_user(credentials)
        except HTTPException:
            return None

# Dependency functions for FastAPI
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    """FastAPI dependency to get current authenticated user"""
    return AuthService.get_current_user(credentials)

def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Security(security_optional)) -> Optional[User]:
    """FastAPI dependency to get current user (optional)"""
    return AuthService.get_current_user_optional(credentials)