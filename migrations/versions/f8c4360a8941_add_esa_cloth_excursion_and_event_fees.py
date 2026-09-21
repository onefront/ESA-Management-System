"""Add ESA cloth excursion and event fees

Revision ID: f8c4360a8941
Revises: 21fe83e9b0e2
Create Date: 2026-09-20 21:04:52.322544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8c4360a8941'
down_revision = '21fe83e9b0e2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('fee_settings', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'esa_cloth',
                sa.Float(),
                nullable=False,
                server_default=sa.text('0')
            )
        )

        batch_op.add_column(
            sa.Column(
                'excursion_fee',
                sa.Float(),
                nullable=False,
                server_default=sa.text('0')
            )
        )

        batch_op.add_column(
            sa.Column(
                'event_fee',
                sa.Float(),
                nullable=False,
                server_default=sa.text('0')
            )
        )


def downgrade():
    with op.batch_alter_table('fee_settings', schema=None) as batch_op:
        batch_op.drop_column('event_fee')
        batch_op.drop_column('excursion_fee')
        batch_op.drop_column('esa_cloth')