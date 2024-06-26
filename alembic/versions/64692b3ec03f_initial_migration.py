"""Initial migration.

Revision ID: 64692b3ec03f
Revises: 
Create Date: 2024-03-25 15:14:30.179295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64692b3ec03f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('objectives', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_objectives_subtitle_id', 'subtitles', ['subtitle_id'], ['id'])

    with op.batch_alter_table('takeaways', schema=None) as batch_op:
        batch_op.drop_column('subtitle_id')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('takeaways', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subtitle_id', sa.VARCHAR(length=60), nullable=True))

    with op.batch_alter_table('objectives', schema=None) as batch_op:
        batch_op.drop_constraint('fk_objectives_subtitle_id', type_='foreignkey')

    # ### end Alembic commands ###
