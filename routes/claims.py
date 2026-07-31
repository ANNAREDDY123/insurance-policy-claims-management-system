from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Claim, Policy
from schemas import ClaimCreate, ClaimUpdate


router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)



# CREATE CLAIM

@router.post("/")
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db)
):

    policy = db.query(Policy).filter(
        Policy.id == claim.policy_id
    ).first()

    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found."
        )

    # Claims only for active policies
    if policy.status != "Active":
        raise HTTPException(
            status_code=400,
            detail="Claims can be raised only for active policies."
        )

    # Claim cannot exceed coverage
    if claim.claim_amount > policy.coverage_amount:
        raise HTTPException(
            status_code=400,
            detail="Claim amount cannot exceed policy coverage amount."
        )

    valid_statuses = [
        "Submitted",
        "Under Review",
        "Approved",
        "Rejected"
    ]

    if claim.claim_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid claim status."
        )

    db_claim = Claim(
        policy_id=claim.policy_id,
        claim_amount=claim.claim_amount,
        claim_reason=claim.claim_reason,
        claim_date=claim.claim_date,
        claim_status=claim.claim_status
    )

    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)

    return db_claim



# GET CLAIMS


@router.get("/")
def get_claims(
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

    query = db.query(Claim)

    # Filter claims by status
    if status:
        query = query.filter(
            Claim.claim_status == status
        )

    # Customer claim history
    if customer_id:
        query = query.join(
            Policy,
            Claim.policy_id == Policy.id
        ).filter(
            Policy.customer_id == customer_id
        )

    total = query.count()

    claims = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": claims
    }


# GET CLAIM BY ID


@router.get("/{claim_id}")
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    claim = db.query(Claim).filter(
        Claim.id == claim_id
    ).first()

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found."
        )

    return claim



# UPDATE CLAIM


@router.put("/{claim_id}")
def update_claim(
    claim_id: int,
    claim: ClaimUpdate,
    db: Session = Depends(get_db)
):

    db_claim = db.query(Claim).filter(
        Claim.id == claim_id
    ).first()

    if not db_claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found."
        )

    # Approved or rejected claims cannot be modified
    if db_claim.claim_status in [
        "Approved",
        "Rejected"
    ]:
        raise HTTPException(
            status_code=400,
            detail=(
                "Approved or rejected claims "
                "cannot be modified."
            )
        )

    policy = db.query(Policy).filter(
        Policy.id == claim.policy_id
    ).first()

    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found."
        )

    if policy.status != "Active":
        raise HTTPException(
            status_code=400,
            detail="Claim requires an active policy."
        )

    if claim.claim_amount > policy.coverage_amount:
        raise HTTPException(
            status_code=400,
            detail="Claim amount cannot exceed policy coverage amount."
        )

    valid_statuses = [
        "Submitted",
        "Under Review"
    ]

    if claim.claim_status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Use verify, approve or reject "
                "endpoints to process the claim."
            )
        )

    db_claim.policy_id = claim.policy_id
    db_claim.claim_amount = claim.claim_amount
    db_claim.claim_reason = claim.claim_reason
    db_claim.claim_date = claim.claim_date
    db_claim.claim_status = claim.claim_status

    db.commit()
    db.refresh(db_claim)

    return db_claim



# VERIFY CLAIM


@router.post("/{claim_id}/verify")
def verify_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    claim = db.query(Claim).filter(
        Claim.id == claim_id
    ).first()

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found."
        )

    if claim.claim_status != "Submitted":
        raise HTTPException(
            status_code=400,
            detail="Only submitted claims can be verified."
        )

    claim.claim_status = "Under Review"

    db.commit()
    db.refresh(claim)

    return {
        "message": "Claim verified successfully.",
        "claim": claim
    }


# APPROVE CLAIM


@router.post("/{claim_id}/approve")
def approve_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    claim = db.query(Claim).filter(
        Claim.id == claim_id
    ).first()

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found."
        )

    if claim.claim_status != "Under Review":
        raise HTTPException(
            status_code=400,
            detail=(
                "Only claims under review "
                "can be approved."
            )
        )

    claim.claim_status = "Approved"

    db.commit()
    db.refresh(claim)

    return {
        "message": "Claim approved successfully.",
        "claim": claim
    }


# REJECT CLAIM


@router.post("/{claim_id}/reject")
def reject_claim(
    claim_id: int,
    db: Session = Depends(get_db)
):

    claim = db.query(Claim).filter(
        Claim.id == claim_id
    ).first()

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found."
        )

    if claim.claim_status != "Under Review":
        raise HTTPException(
            status_code=400,
            detail=(
                "Only claims under review "
                "can be rejected."
            )
        )

    claim.claim_status = "Rejected"

    db.commit()
    db.refresh(claim)

    return {
        "message": "Claim rejected successfully.",
        "claim": claim
    }
