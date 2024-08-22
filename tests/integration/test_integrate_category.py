from app.models import Category
from tests.factories.models_factory import get_random_category_dict

"""
- [ ] Test POST new category successfully
"""


def test_integrate_create_new_category_successful(client, db_session_integration):
    # Arrange: Prepare test data
    category_data = get_random_category_dict()
    category_id = category_data.pop("id")

    # Act: Make a POST request to create a new category
    response = client.post("api/category/", json=category_data)

    # Assert: Verify response
    assert response.status_code == 201

    # Assert: Verify the response and DB state
    create_category = (
        db_session_integration.query(Category).filter_by(id=category_id).first()
    )

    assert create_category is not None

    # Assert: Verify response data matches databse entry
    assert response.json() == {
        column.name: getattr(create_category, column.name)
        for column in create_category.__table__.columns
    }


"""
- [ ] Test POST new category duplicate name and level
"""


def test_integrate_create_new_category_duplicate(client, db_session_integration):
    category_data = get_random_category_dict()
    new_category = Category(**category_data)
    db_session_integration.add(new_category)
    db_session_integration.commit()
    category_data.pop("id")

    response = client.post("api/category/", json=category_data)

    assert response.status_code == 400


"""
- [ ] Test POST new category duplicate name and level
"""


def test_integrate_create_new_category_duplicate_slug(client, db_session_integration):
    # Generate two random categories
    category_1 = get_random_category_dict()
    category_2 = get_random_category_dict()

    # Ensure both categories have the same slug
    slug = "same-slug"
    category_1["slug"] = slug
    category_2["slug"] = slug

    # Add the first category to the db
    db_session_integration.add(Category(**category_1))
    db_session_integration.commit()

    # attempt to add the second category via the API endpoint
    response = client.post("api/category/", json=category_2)

    # Verify that the insertion of the second category faisl due to duplicate slug
    assert response.status_code == 400


"""
- [ ] Test to return all categories successfully
"""


def test_integrate_get_all_categories(client, db_session_integration):
    categories = [get_random_category_dict() for _ in range(5)]

    for category_data in categories:
        category_data.pop("id")
        new_category = Category(**category_data)
        db_session_integration.add(new_category)
        db_session_integration.commit()

    response = client.get("api/category/")

    assert response.status_code == 200
    assert response.json() is not None

    returned_categories = response.json()
    assert isinstance(returned_categories, list)
    assert len(returned_categories) == len(categories)

    for returned_category, inserted_category_data in zip(
        returned_categories, categories
    ):
        assert returned_category["name"] == inserted_category_data["name"]
        assert returned_category["slug"] == inserted_category_data["slug"]
        assert returned_category["is_active"] == inserted_category_data["is_active"]
        assert returned_category["level"] == inserted_category_data["level"]


"""
- [ ] Test UPDATE category successfully
"""


def test_integrate_update_category_successfully(client, db_session_integration):
    initial_category = get_random_category_dict()
    new_category = Category(**initial_category)
    db_session_integration.add(new_category)
    db_session_integration.commit()

    updated_category_data = {
        "name": "Updated Name",
        "slug": "updated-slug",
        "is_active": False,
        "level": 10,
    }

    response = client.put(
        f"/api/category/{new_category.id}", json=updated_category_data
    )

    assert response.status_code == 201

    updated_category = (
        db_session_integration.query(Category).filter_by(id=new_category.id).first()
    )

    assert updated_category is not None
    assert updated_category.name == updated_category_data["name"]
    assert updated_category.slug == updated_category_data["slug"]
    assert updated_category.is_active == updated_category_data["is_active"]
    assert updated_category.level == updated_category_data["level"]


"""
- [ ] Test DELETE category successfully
"""


def test_integrate_delete_category_successfully(client, db_session_integration):
    category_data = get_random_category_dict()
    new_category = Category(**category_data)

    db_session_integration.add(new_category)
    db_session_integration.commit()

    response = client.delete(f"/api/category/{new_category.id}")

    assert response.status_code == 200
    assert response.json()["id"] == category_data["id"]
    assert response.json()["name"] == category_data["name"]

    deleted_category = (
        db_session_integration.query(Category).filter_by(id=new_category.id).first()
    )

    assert deleted_category is None
