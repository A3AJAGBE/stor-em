"""Add merchants table

Revision ID: 39aaae8582f2
Revises: fa1e2e0d121a
Create Date: 2021-04-26 13:57:20.862688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39aaae8582f2'
down_revision = 'fa1e2e0d121a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('merchants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('merchant_name', sa.String(length=50), nullable=False),
    sa.Column('contact_name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('merchant_name'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('merchants')
    # ### end Alembic commands ###
