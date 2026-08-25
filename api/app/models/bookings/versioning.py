"""Metadata definitions for manual appointment versioning tables."""

from sqlalchemy import DateTime, Index, PrimaryKeyConstraint

from qsystem import db


appointment_version = db.Table(
    "appointment_version",
    db.metadata,
    db.Column("appointment_id", db.Integer, nullable=False),
    db.Column("office_id", db.Integer, nullable=True),
    db.Column("service_id", db.Integer, nullable=True),
    db.Column("citizen_id", db.Integer, nullable=True),
    db.Column("start_time", DateTime(timezone=True), nullable=True),
    db.Column("end_time", DateTime(timezone=True), nullable=True),
    db.Column("checked_in_time", DateTime(timezone=True), nullable=True),
    db.Column("comments", db.String(255), nullable=True),
    db.Column("citizen_name", db.String(255), nullable=True),
    db.Column("contact_information", db.String(255), nullable=True),
    db.Column("blackout_flag", db.String(1), nullable=True),
    db.Column("recurring_uuid", db.String(255), nullable=True),
    db.Column("online_flag", db.Boolean(), nullable=True),
    db.Column("is_draft", db.Boolean(), nullable=True),
    db.Column("created_at", DateTime(timezone=True), nullable=True),
    db.Column("stat_flag", db.Boolean(), nullable=True),
    db.Column("updated_at", DateTime(timezone=True), nullable=True),
    db.Column("updated_by", db.String(), nullable=True),
    db.Column("transaction_id", db.BigInteger, nullable=False),
    db.Column("end_transaction_id", db.BigInteger, nullable=True),
    db.Column("operation_type", db.SmallInteger, nullable=False),
    PrimaryKeyConstraint(
        "appointment_id",
        "transaction_id",
        name="appointment_version_pkey",
    ),
    Index("ix_appointment_version_transaction_id", "transaction_id"),
    Index("ix_appointment_version_operation_type", "operation_type"),
    Index("ix_appointment_version_end_transaction_id", "end_transaction_id"),
)


transaction = db.Table(
    "transaction",
    db.metadata,
    db.Column("issued_at", DateTime(), nullable=True),
    db.Column("id", db.BigInteger, autoincrement=True, nullable=False),
    db.Column("remote_addr", db.String(50), nullable=True),
    PrimaryKeyConstraint("id", name="transaction_pkey"),
)
