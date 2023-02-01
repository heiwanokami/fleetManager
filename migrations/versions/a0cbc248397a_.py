"""empty message

Revision ID: a0cbc248397a
Revises: 3b1cce2b6157
Create Date: 2023-02-01 16:24:02.712568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0cbc248397a'
down_revision = '3b1cce2b6157'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('route',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver', sa.Integer(), nullable=True),
    sa.Column('car', sa.Integer(), nullable=True),
    sa.Column('route_desc', sa.String(length=120), nullable=True),
    sa.Column('route_purpose', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('own_gas', sa.Integer(), nullable=True),
    sa.Column('route_length', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car'], ['car.SPZ'], ),
    sa.ForeignKeyConstraint(['driver'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('route', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_route_date'), ['date'], unique=False)
        batch_op.create_index(batch_op.f('ix_route_route_desc'), ['route_desc'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('route', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_route_route_desc'))
        batch_op.drop_index(batch_op.f('ix_route_date'))

    op.drop_table('route')
    # ### end Alembic commands ###