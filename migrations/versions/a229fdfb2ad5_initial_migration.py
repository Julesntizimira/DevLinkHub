"""Initial migration

Revision ID: a229fdfb2ad5
Revises: 9e507a7d7ef2
Create Date: 2024-03-22 10:07:38.330330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a229fdfb2ad5'
down_revision: Union[str, None] = '9e507a7d7ef2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'profile_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('profile_id', sa.VARCHAR(length=60), nullable=True))
    # ### end Alembic commands ###
