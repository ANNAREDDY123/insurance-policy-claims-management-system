from fastapi import FastAPI

from database import Base, engine

from models import (
    User,
    Customer,
    Policy,
    Claim
)

from routes.auth import router as auth_router
from routes.customers import router as customers_router
from routes.policies import router as policies_router
from routes.claims import router as claims_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Insurance Policy & Claims Management System",
    description=(
        "FastAPI backend application for customer, "
        "insurance policy and claims management."
    ),
    version="1.0.0"
)


# Include Routers
app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(policies_router)
app.include_router(claims_router)


@app.get("/")
def home():
    return {
        "message": (
            "Insurance Policy & Claims "
            "Management System API"
        )
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
