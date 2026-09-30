from typing import Literal
from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    email: str
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)
class UserLogin(BaseModel):
    email: str
    password: str
class RoomInput(BaseModel):
    room_type: str = Field(min_length=2, max_length=60)
    quantity: int = Field(default=1, ge=1, le=50)
    notes: str = Field(default="", max_length=500)
class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=100_000_000)
    currency: str = Field(default="INR", min_length=3, max_length=5)
    rooms: list[RoomInput] = Field(min_length=1, max_length=20)
    preferences: str = Field(default="", max_length=2000)
class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=100_000_000)
    currency: str = Field(default="INR", min_length=3, max_length=5)
    guest_count: int = Field(ge=1, le=100_000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="", max_length=200)
    preferences: str = Field(default="", max_length=2000)
class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=100_000_000)
    currency: str = Field(default="INR", min_length=3, max_length=5)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="", max_length=500)
    outfit_description: str = Field(default="", max_length=1000)
class RecommendationItem(BaseModel):
    name: str
    category: str
    estimated_price: float
    currency: str = "INR"
    platform: str
    reason: str
    search_url: str
    priority: Literal["essential", "recommended", "optional"] = "recommended"
class BudgetAllocation(BaseModel):
    category: str
    amount: float
    percentage: float
    note: str
class RecommendationResponse(BaseModel):
    title: str
    summary: str
    budget: float
    currency: str
    total_estimated: float
    remaining_budget: float
    budget_allocations: list[BudgetAllocation] = []
    recommendations: list[RecommendationItem] = []
    tips: list[str] = []
    source: Literal["gemini", "fallback"] = "fallback"
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    full_name: str
class SessionInfo(BaseModel):
    authenticated: bool
    user_id: int | None = None
    email: str | None = None
    full_name: str | None = None
