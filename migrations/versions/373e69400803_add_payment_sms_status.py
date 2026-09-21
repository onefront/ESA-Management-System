"""Add payment SMS status

Revision ID: 373e69400803
Revises: f8c4360a8941
Create Date: 2026-09-21 13:45:09.471503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '373e69400803'
down_revision = 'f8c4360a8941'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'sms_sent',
                sa.Boolean(),
                nullable=False,
                server_default=sa.false()
            )
        )

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_column('sms_sent')

    # ### end Alembic commands ###
