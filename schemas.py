from datetime import date
from pydantic import BaseModel, EmailStr, Field


# USER SCHEMAS


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# CUSTOMER SCHEMAS


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True


# POLICY SCHEMAS

class PolicyCreate(BaseModel):
    customer_id: int
    policy_number: str
    policy_type: str
    premium_amount: float = Field(gt=0)
    coverage_amount: float = Field(gt=0)
    policy_start_date: date
    policy_end_date: date
    status: str = "Active"


class PolicyUpdate(BaseModel):
    customer_id: int
    policy_number: str
    policy_type: str
    premium_amount: float = Field(gt=0)
    coverage_amount: float = Field(gt=0)
    policy_start_date: date
    policy_end_date: date
    status: str


class PolicyResponse(PolicyCreate):
    id: int

    class Config:
        from_attributes = True


# CLAIM SCHEMAS


class ClaimCreate(BaseModel):
    policy_id: int
    claim_amount: float = Field(gt=0)
    claim_reason: str
    claim_date: date
    claim_status: str = "Submitted"


class ClaimUpdate(BaseModel):
    policy_id: int
    claim_amount: float = Field(gt=0)
    claim_reason: str
    claim_date: date
    claim_status: str


class ClaimResponse(ClaimCreate):
    id: int

    class Config:
        from_attributes = True
