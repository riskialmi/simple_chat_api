"""Added table

Revision ID: 6b94255d1a22
Revises: 
Create Date: 2022-12-16 08:26:04.682852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b94255d1a22'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('massage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('created_dtm', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_name', sa.String(length=10), nullable=True),
    sa.Column('members', sa.JSON(), nullable=True),
    sa.Column('messages', sa.JSON(), nullable=True),
    sa.Column('created_dtm', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('created_dtm', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('room')
    op.drop_table('massage')
    # ### end Alembic commands ###
