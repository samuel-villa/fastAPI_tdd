from sqlalchemy import Integer, String

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
    assert db_inspector.has_table("product_image")


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_types(db_inspector):
    table = "product_image"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    """columns output example
    {'id': {'name': 'id', 'type': INTEGER(), 'nullable': False, 'default': "nextval('category_id_seq'::regclass)", 'autoincrement': True, 'comment': None}}
    """
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["alternative_text"]["type"], String)
    assert isinstance(columns["url"]["type"], String)
    assert isinstance(columns["order"]["type"], Integer)
    assert isinstance(columns["product_line_id"]["type"], Integer)


"""
- [ ] Ensure that column foreign keys are correctly defined.
"""


def test_model_structure_foreign_key(db_inspector):
    table = "product_image"
    foreign_keys = db_inspector.get_foreign_keys(table)
    product_image_foreign_key = next(
        (
            fk
            for fk in foreign_keys
            if set(fk["constrained_columns"]) == {"product_line_id"}
        ),
        None,
    )
    assert product_image_foreign_key is not None


"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_nullable_contraints(db_inspector):
    table = "product_image"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "alternative_text": False,
        "url": False,
        "order": False,
        "product_line_id": False,
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
    table = "product_image"
    constraints = db_inspector.get_check_constraints(table)

    # we test if constraints with these names exist (see models.py)
    assert any(
        constraint["name"] == "product_image_order_range"
        for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_image_alt_text_length_check"
        for constraint in constraints
    )
    assert any(
        constraint["name"] == "product_image_url_length_check"
        for constraint in constraints
    )


"""
- [ ] Verify the correctness of default values for relevant columns.
"""

"""
- [ ] Ensure that column lengths align with defined requirements.
"""


def test_model_structure_column_lenghts(db_inspector):
    table = "product_image"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["alternative_text"]["type"].length == 100
    assert columns["url"]["type"].length == 100


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""


def test_model_structure_unique_constraints(db_inspector):
    table = "product_image"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "uq_product_image_order_product_line_id"
        for constraint in constraints
    )
