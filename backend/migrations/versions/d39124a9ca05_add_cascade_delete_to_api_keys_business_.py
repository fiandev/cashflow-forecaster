"""Add CASCADE delete to api_keys business_id foreign key

Revision ID: d39124a9ca05
Revises: 120642e26b6b
Create Date: 2025-12-01 10:54:43.045558

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = 'd39124a9ca05'
down_revision = '120642e26b6b'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new api_keys table with CASCADE on delete
    op.create_table(
        'api_keys_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=True),
        sa.Column('key_hash', sa.String(length=255), nullable=True),
        sa.Column('scopes', sa.Text(), nullable=True),
        sa.Column('revoked', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from old table to new table
    op.execute("INSERT INTO api_keys_new SELECT id, business_id, name, key_hash, scopes, revoked, created_at FROM api_keys")

    # Drop the old table
    op.drop_table('api_keys')

    # Rename the new table to original name
    op.execute("ALTER TABLE api_keys_new RENAME TO api_keys")


def downgrade():
    # Create a new api_keys table without CASCADE on delete
    op.create_table(
        'api_keys_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=True),
        sa.Column('key_hash', sa.String(length=255), nullable=True),
        sa.Column('scopes', sa.Text(), nullable=True),
        sa.Column('revoked', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.ForeignKeyConstraint(['business_id'], ['businesses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from current table to old table
    op.execute("INSERT INTO api_keys_old SELECT id, business_id, name, key_hash, scopes, revoked, created_at FROM api_keys")

    # Drop the current table
    op.drop_table('api_keys')

    # Rename the old table to original name
    op.execute("ALTER TABLE api_keys_old RENAME TO api_keys")
