"""empty message

Revision ID: 8b195c2e0150
Revises: 12118a9706f7
Create Date: 2016-07-29 18:51:41.827179

"""

# revision identifiers, used by Alembic.
revision = '8b195c2e0150'
down_revision = '12118a9706f7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset', sa.Column('residue_number', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_dataset_residue_number'), 'dataset', ['residue_number'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dataset_residue_number'), table_name='dataset')
    op.drop_column('dataset', 'residue_number')
    ### end Alembic commands ###
