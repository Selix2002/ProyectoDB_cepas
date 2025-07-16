"""Convert hidden_columns to text[]

Revision ID: 1e6317f2eb52
Revises: 6ba2fc716fb8
Create Date: 2025-07-16 15:21:55.940366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision: str = '1e6317f2eb52'
down_revision: Union[str, None] = '6ba2fc716fb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "hidden_columns",
        type_=postgresql.ARRAY(sa.Text()),
        postgresql_using="hidden_columns::text[]",
        nullable=False,
        server_default=sa.text("ARRAY[]::text[]"),
    )

def downgrade() -> None:
    """Downgrade schema."""
    pass
