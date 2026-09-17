from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


revision: str = "f2f21570455c"
down_revision: Union[str, Sequence[str], None] = "14ec9d499ec3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # 1. Old author names-la irunthu authors table-ku data create panrom
    op.execute("""
        INSERT INTO authors (name, email, country)
        SELECT DISTINCT
            b.author,
            CONCAT(
                LOWER(REPLACE(b.author, ' ', '.')),
                '@example.com'
            ),
            NULL
        FROM books b
        WHERE b.author IS NOT NULL
        AND NOT EXISTS (
            SELECT 1
            FROM authors a
            WHERE a.name = b.author
        )
    """)

    # 2. Old category names-la irunthu categories table-ku data create panrom
    op.execute("""
        INSERT INTO categories (name, description)
        SELECT DISTINCT
            b.category,
            NULL
        FROM books b
        WHERE b.category IS NOT NULL
        AND NOT EXISTS (
            SELECT 1
            FROM categories c
            WHERE c.name = b.category
        )
    """)

    # 3. Book-oda author_id update panrom
    # Old author name -> authors table id
    op.execute("""
        UPDATE books b
        JOIN authors a ON b.author = a.name
        SET b.author_id = a.id
    """)

    # 4. Book-oda category_id update panrom
    # Old category name -> categories table id
    op.execute("""
        UPDATE books b
        JOIN categories c ON b.category = c.name
        SET b.category_id = c.id
    """)

    # 5. author_id NULL-a irukka koodathu
    op.alter_column(
        "books",
        "author_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    # 6. category_id NULL-a irukka koodathu
    op.alter_column(
        "books",
        "category_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    # 7. Foreign Key create panrom
    op.create_foreign_key(
        "fk_books_author_id",
        "books",
        "authors",
        ["author_id"],
        ["id"]
    )

    op.create_foreign_key(
        "fk_books_category_id",
        "books",
        "categories",
        ["category_id"],
        ["id"]
    )

    # 8. Old author column remove panrom
    op.drop_column("books", "author")

    # 9. Old category column remove panrom
    op.drop_column("books", "category")


def downgrade() -> None:

    # Add old columns back

    op.add_column(
        "books",
        sa.Column(
            "author",
            mysql.VARCHAR(length=100),
            nullable=True
        )
    )

    op.add_column(
        "books",
        sa.Column(
            "category",
            mysql.VARCHAR(length=100),
            nullable=True
        )
    )

    # Restore author names

    op.execute(
        """
        UPDATE books b
        JOIN authors a
            ON b.author_id = a.id
        SET b.author = a.name
        """
    )

    # Restore category names

    op.execute(
        """
        UPDATE books b
        JOIN categories c
            ON b.category_id = c.id
        SET b.category = c.name
        """
    )

    # Drop foreign keys

    op.drop_constraint(
        "fk_books_author_id",
        "books",
        type_="foreignkey"
    )

    op.drop_constraint(
        "fk_books_category_id",
        "books",
        type_="foreignkey"
    )

    # Remove new columns

    op.drop_column("books", "category_id")
    op.drop_column("books", "author_id")
    op.drop_column("books", "stock")