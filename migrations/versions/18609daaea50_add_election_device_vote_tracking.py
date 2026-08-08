"""Add election device vote tracking

Revision ID: 18609daaea50
Revises: ac10ab3124d9
Create Date: 2026-08-08 21:03:20.319100

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "18609daaea50"
down_revision = "ac10ab3124d9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "election_device_votes",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "election_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "device_token",
            sa.String(length=128),
            nullable=False
        ),

        sa.Column(
            "voted_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now()
        ),

        sa.ForeignKeyConstraint(
            ["election_id"],
            ["elections.id"]
        ),

        sa.UniqueConstraint(
            "election_id",
            "device_token",
            name="unique_election_device_vote"
        )
    )


def downgrade():
    op.drop_table("election_device_votes")