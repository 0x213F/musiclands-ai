from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    uid: str = Field(..., description="Firebase user ID")
    email: str = Field(..., description="User email address")
    display_name: Optional[str] = Field(None, description="User display name")
    email_verified: bool = Field(default=False, description="Email verification status")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    
    # Subscription management fields
    stripe_customer_id: Optional[str] = Field(None, description="Stripe customer ID")
    subscription_status: Optional[str] = Field(None, description="Subscription status (active, canceled, past_due, etc.)")
    subscription_id: Optional[str] = Field(None, description="Stripe subscription ID")
    plan_type: Optional[str] = Field(None, description="Plan type (monthly, yearly)")
    trial_end: Optional[datetime] = Field(None, description="Trial end date")
    subscription_end: Optional[datetime] = Field(None, description="Subscription end date")
    
    # Google Calendar integration
    google_calendar_connected: bool = Field(default=False, description="Google Calendar connection status")
    google_calendar_token: Optional[str] = Field(None, description="Google Calendar access token")
    google_calendar_refresh_token: Optional[str] = Field(None, description="Google Calendar refresh token")
    google_calendar_connected_at: Optional[datetime] = Field(None, description="Calendar connection timestamp")
    google_calendar_id: Optional[str] = Field(None, description="ID of the dedicated calendar created for this app")
    
    # Webhook channel information
    google_calendar_channel_id: Optional[str] = Field(None, description="Google Calendar webhook channel ID")
    google_calendar_resource_id: Optional[str] = Field(None, description="Google Calendar webhook resource ID")
    google_calendar_channel_expiration: Optional[int] = Field(None, description="Webhook channel expiration timestamp (milliseconds)")

    class Config:
        from_attributes = True

class UserSignup(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password (min 6 characters)")
    display_name: str = Field(..., description="User display name")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class UserPasswordReset(BaseModel):
    email: EmailStr = Field(..., description="User email address")

class UserPasswordUpdate(BaseModel):
    old_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password (min 6 characters)")

class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, description="User display name")

class PasswordReset(BaseModel):
    email: EmailStr = Field(..., description="User email address")

class PasswordUpdate(BaseModel):
    uid: str = Field(..., description="User ID")
    new_password: str = Field(..., min_length=6, description="New password (min 6 characters)")

# Auth token models
class AuthToken(BaseModel):
    access_token: str = Field(..., description="Access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")

class AuthResponse(BaseModel):
    user: User = Field(..., description="User information")
    token: AuthToken = Field(..., description="Authentication token")

class TokenPayload(BaseModel):
    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    email: str = Field(..., description="User email")

class FirebaseAuthResponse(BaseModel):
    user: User
    message: str