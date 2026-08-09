"""Add voter reference to device votes

Revision ID: 65d43f0e2c00
Revises: 18609daaea50
"""

from alembic import op


revision = "65d43f0e2c00"
down_revision = "18609daaea50"
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        "fk_election_device_votes_member_index",
        "election_device_votes",
        "member_indexes",
        ["member_index_id"],
        ["id"]
    )


def downgrade():
    op.drop_constraint(
        "fk_election_device_votes_member_index",
        "election_device_votes",
        type_="foreignkey"
    )

    op.drop_column(
        "election_device_votes",
        "member_index_id"
    )