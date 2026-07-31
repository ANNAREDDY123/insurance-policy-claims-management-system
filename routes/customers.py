from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Customer
from schemas import CustomerCreate


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# CREATE CUSTOMER

@router.post("/")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing_customer = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Customer email already exists."
        )

    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


# GET CUSTOMERS

@router.get("/")
def get_customers(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be greater than 0."
        )

    query = db.query(Customer)

    total = query.count()

    customers = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": customers
    }


# GET CUSTOMER BY ID


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    return customer
