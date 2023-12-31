"""added hashed_password to user table

Revision ID: 4b193f786801
Revises: a20a6c3aec3f
Create Date: 2023-10-19 14:49:39.720981

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "4b193f786801"
down_revision = "0841a2d5d3f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("hashed_password", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "hashed_password")
    # ### end Alembic commands ###
