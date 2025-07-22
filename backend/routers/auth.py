from fastapi import APIRouter, HTTPException
from models.user import User, UserSignup, UserLogin, UserUpdate, PasswordReset, PasswordUpdate, FirebaseAuthResponse
from services.firebase_auth_service import FirebaseAuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
firebase_auth = FirebaseAuthService()

@router.post("/register", response_model=FirebaseAuthResponse)
async def register(user_data: UserSignup):
    """Register a new user with Firebase Auth"""
    try:
        user = firebase_auth.create_user(user_data)
        return FirebaseAuthResponse(
            user=user,
            message="User registered successfully"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=FirebaseAuthResponse)
async def login(credentials: UserLogin):
    """Login with email and password"""
    try:
        user = firebase_auth.authenticate_user(credentials.email, credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        return FirebaseAuthResponse(
            user=user,
            message="Login successful"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/user/{uid}", response_model=User)
async def get_user_by_uid(uid: str):
    """Get user by Firebase UID"""
    user = firebase_auth.get_user_by_uid(uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/user/email/{email}", response_model=User)
async def get_user_by_email(email: str):
    """Get user by email address"""
    user = firebase_auth.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/password-reset")
async def send_password_reset(reset_request: PasswordReset):
    """Send password reset email"""
    try:
        success = firebase_auth.send_password_reset_email(reset_request.email)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send password reset email")
        
        return {"message": "Password reset email sent successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send password reset: {str(e)}")

@router.post("/password-update")
async def update_password(password_update: PasswordUpdate):
    """Update user password"""
    try:
        success = firebase_auth.update_user_password(password_update.uid, password_update.new_password)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update password")
        
        return {"message": "Password updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update password: {str(e)}")

@router.delete("/user/{uid}")
async def delete_user(uid: str):
    """Delete user account"""
    try:
        success = firebase_auth.delete_user(uid)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete user")
        
        return {"message": "User deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

@router.post("/verify-token")
async def verify_firebase_token(token_data: dict):
    """Verify Firebase ID token"""
    try:
        id_token = token_data.get("id_token")
        if not id_token:
            raise HTTPException(status_code=400, detail="ID token is required")
        
        decoded_token = firebase_auth.verify_id_token(id_token)
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        return {"message": "Token is valid", "token_data": decoded_token}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token verification failed: {str(e)}")