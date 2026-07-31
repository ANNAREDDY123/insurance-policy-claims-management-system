from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)

from database import Base


# USER MODEL


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False
    )


# CUSTOMER MODEL

class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=False
    )

    address = Column(
        String(255),
        nullable=False
    )


# POLICY MODEL

class Policy(Base):
    __tablename__ = "policies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    policy_number = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    policy_type = Column(
        String(100),
        nullable=False
    )

    premium_amount = Column(
        Float,
        nullable=False
    )

    coverage_amount = Column(
        Float,
        nullable=False
    )

    policy_start_date = Column(
        Date,
        nullable=False
    )

    policy_end_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="Active"
    )


# CLAIM MODEL

class Claim(Base):
    __tablename__ = "claims"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    policy_id = Column(
        Integer,
        ForeignKey("policies.id"),
        nullable=False
    )

    claim_amount = Column(
        Float,
        nullable=False
    )

    claim_reason = Column(
        String(255),
        nullable=False
    )

    claim_date = Column(
        Date,
        nullable=False
    )

    claim_status = Column(
        String(30),
        nullable=False,
        default="Submitted"
    )
