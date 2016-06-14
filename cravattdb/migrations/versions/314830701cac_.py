"""empty message

Revision ID: 314830701cac
Revises: 438d968deb2f
Create Date: 2016-06-14 19:56:45.886602

"""

# revision identifiers, used by Alembic.
revision = '314830701cac'
down_revision = '438d968deb2f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('experiment', sa.Column('public', sa.Boolean(), nullable=True))
    op.add_column('experiment', sa.Column('replicate_of', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_experiment_replicate_of'), 'experiment', ['replicate_of'], unique=False)
    op.create_foreign_key(None, 'experiment', 'experiment', ['replicate_of'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'experiment', type_='foreignkey')
    op.drop_index(op.f('ix_experiment_replicate_of'), table_name='experiment')
    op.drop_column('experiment', 'replicate_of')
    op.drop_column('experiment', 'public')
    ### end Alembic commands ###
