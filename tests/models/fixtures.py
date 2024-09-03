"""
This fixtures.py file (second) is created in order to 
extract part of the code that will be utilized by all test files.
"""

import pytest
from sqlalchemy import inspect

@pytest.fixture(scope="function")
def db_inspector(db_session):
    """
    we don't need to import the 'db_session' because it's automatically
    created and available all over the test directory
    (autouse=True in the main fixtures.py)
    """
    return inspect(db_session().bind)
