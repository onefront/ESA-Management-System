"""Separate account creation from voting status

Revision ID: 21fe83e9b0e2
Revises: 65d43f0e2c00
Create Date: 2026-08-09 08:55:10.496076

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.

revision = '21fe83e9b0e2'
down_revision = '65d43f0e2c00'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('member_indexes', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'account_created',
                sa.Boolean(),
                nullable=False,
                server_default=sa.false()
            )
        )


def downgrade():
    with op.batch_alter_table('member_indexes', schema=None) as batch_op:
        batch_op.drop_column('account_created')