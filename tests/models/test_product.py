from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

"""
For the DB construction we will refer to this schema:
https://lucid.app/lucidchart/dcf7e614-f071-4832-99b6-361b13db1a9f/edit?invitationId=inv_12607d3e-7a85-4489-83fd-0aa57812706f&page=0_0#
"""

"""
## Table and Column Validation
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""


def test_model_structure_table_exists(db_inspector):
    """
    db_inspector is function created in fixtures.py
    It's available automatically and there is no need to import it in this file.
    """
    assert db_inspector.has_table("product")


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_types(db_inspector):
    table = "product"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    """columns output example
    {'id': {'name': 'id', 'type': INTEGER(), 'nullable': False, 'default': "nextval('category_id_seq'::regclass)", 'autoincrement': True, 'comment': None}}
    """
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["pid"]["type"], UUID)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["description"]["type"], Text)
    assert isinstance(columns["is_digital"]["type"], Boolean)
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["updated_at"]["type"], DateTime)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["stock_status"]["type"], Enum)
    assert isinstance(columns["category_id"]["type"], Integer)
    assert isinstance(columns["seasonal_event_id"]["type"], Integer)


"""
- [ ] Ensure that column foreign keys are correctly defined.
"""


def test_model_structure_foreign_key(db_inspector):
    table = "product"
    foreign_keys = db_inspector.get_foreign_keys(table)
    category_foreign_key = next(
        (
            fk
            for fk in foreign_keys
            if set(fk["constrained_columns"]) == {"category_id"}
            or set(fk["constrained_columns"]) == {"seasonal_event_id"}
        ),
        None,
    )
    assert category_foreign_key is not None


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_nullable_contraints(db_inspector):
    table = "product"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "pid": False,
        "name": False,
        "slug": False,
        "description": True,
        "is_digital": False,
        "created_at": False,
        "updated_at": False,
        "is_active": False,
        "stock_status": False,
        "category_id": False,
        "seasonal_event_id": True,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"


"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
"""


def test_model_structure_column_constraints(db_inspector):
    table = "product"
    constraints = db_inspector.get_check_constraints(table)

    # we test if constraints with these names exist (see models.py)
    assert any(
        constraint["name"] == "product_name_length_check" for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_slug_length_check" for constraint in constraints
    )


"""
- [ ] Verify the correctness of default values for relevant columns.
"""


def test_model_structure_column_default_values(db_inspector):
    table = "product"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["is_digital"]["default"] == "false"
    assert columns["is_active"]["default"] == "false"
    assert columns["stock_status"]["default"] == "'oos'::status_enum"


"""
- [ ] Ensure that column lengths align with defined requirements.
"""


def test_model_structure_column_lenghts(db_inspector):
    table = "product"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["name"]["type"].length == 200
    assert columns["slug"]["type"].length == 220


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""


def test_model_structure_unique_constraints(db_inspector):
    table = "product"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "uq_product_pid" for constraint in constraints)
    assert any(constraint["name"] == "uq_product_name" for constraint in constraints)
    assert any(constraint["name"] == "uq_product_slug" for constraint in constraints)
