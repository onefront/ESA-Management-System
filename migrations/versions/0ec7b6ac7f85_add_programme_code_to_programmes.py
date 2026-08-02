"""Add programme_code to programmes

Revision ID: 0ec7b6ac7f85
Revises: 29d357ee281c
Create Date: 2026-07-31 23:29:46.517436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ec7b6ac7f85'
down_revision = '29d357ee281c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('programmes', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'programme_code',
                sa.String(length=20),
                nullable=True
            )
        )

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('programmes', schema=None) as batch_op:
        batch_op.drop_column('programme_code')

    # ### end Alembic commands ###
