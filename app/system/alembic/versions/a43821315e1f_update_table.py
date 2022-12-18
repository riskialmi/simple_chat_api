"""Update table

Revision ID: a43821315e1f
Revises: 7db371729adc
Create Date: 2022-12-17 09:55:08.179637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a43821315e1f'
down_revision = '7db371729adc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('massage', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'massage', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'massage', type_='foreignkey')
    op.drop_column('massage', 'user_id')
    # ### end Alembic commands ###
