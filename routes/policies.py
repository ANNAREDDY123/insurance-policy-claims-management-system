from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Policy, Customer
from schemas import PolicyCreate, PolicyUpdate


router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)



# CREATE POLICY


@router.post("/")
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db)
):

    # Check customer
    customer = db.query(Customer).filter(
        Customer.id == policy.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    # Check unique policy number
    existing_policy = db.query(Policy).filter(
        Policy.policy_number == policy.policy_number
    ).first()

    if existing_policy:
        raise HTTPException(
            status_code=400,
            detail="Policy number already exists."
        )

    # Validate dates
    if policy.policy_end_date <= policy.policy_start_date:
        raise HTTPException(
            status_code=400,
            detail=(
                "Policy end date must be after "
                "policy start date."
            )
        )

    # Validate status
    valid_statuses = [
        "Active",
        "Expired",
        "Cancelled"
    ]

    if policy.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid policy status."
        )

    db_policy = Policy(
        customer_id=policy.customer_id,
        policy_number=policy.policy_number,
        policy_type=policy.policy_type,
        premium_amount=policy.premium_amount,
        coverage_amount=policy.coverage_amount,
        policy_start_date=policy.policy_start_date,
        policy_end_date=policy.policy_end_date,
        status=policy.status
    )

    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)

    return db_policy


# GET POLICIES


@router.get("/")
def get_policies(
    policy_number: str = None,
    status: str = None,
    customer_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    if page < 1 or limit < 1:
        raise HTTPException(
            status_code=400,
            detail="Page and limit must be greater than 0."
        )

    query = db.query(Policy)

    # Search by policy number
    if policy_number:
        query = query.filter(
            Policy.policy_number.ilike(
                f"%{policy_number}%"
            )
        )

    # Filter by status
    if status:
        query = query.filter(
            Policy.status == status
        )

    # Customer policies
    if customer_id:
        query = query.filter(
            Policy.customer_id == customer_id
        )

    total = query.count()

    policies = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": policies
    }



# GET POLICY BY ID


@router.get("/{policy_id}")
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db)
):

    policy = db.query(Policy).filter(
        Policy.id == policy_id
    ).first()

    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found."
        )

    return policy


# UPDATE POLICY


@router.put("/{policy_id}")
def update_policy(
    policy_id: int,
    policy: PolicyUpdate,
    db: Session = Depends(get_db)
):

    db_policy = db.query(Policy).filter(
        Policy.id == policy_id
    ).first()

    if not db_policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found."
        )

    # Check customer
    customer = db.query(Customer).filter(
        Customer.id == policy.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    # Check duplicate policy number
    duplicate_policy = db.query(Policy).filter(
        Policy.policy_number == policy.policy_number,
        Policy.id != policy_id
    ).first()

    if duplicate_policy:
        raise HTTPException(
            status_code=400,
            detail="Policy number already exists."
        )

    # Date validation
    if policy.policy_end_date <= policy.policy_start_date:
        raise HTTPException(
            status_code=400,
            detail=(
                "Policy end date must be after "
                "policy start date."
            )
        )

    # Status validation
    valid_statuses = [
        "Active",
        "Expired",
        "Cancelled"
    ]

    if policy.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid policy status."
        )

    db_policy.customer_id = policy.customer_id
    db_policy.policy_number = policy.policy_number
    db_policy.policy_type = policy.policy_type
    db_policy.premium_amount = policy.premium_amount
    db_policy.coverage_amount = policy.coverage_amount
    db_policy.policy_start_date = policy.policy_start_date
    db_policy.policy_end_date = policy.policy_end_date
    db_policy.status = policy.status

    db.commit()
    db.refresh(db_policy)

    return db_policy
