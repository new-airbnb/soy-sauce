import pytest


# https://stackoverflow.com/questions/54901966/persistent-data-among-tests-with-django-and-pytest
# together with --create-db in pytest.ini,
# we can create a new empty db for every pytest run
# and persist data during the run
# while avoiding rolling back the db (to empty state) for each test case
@pytest.fixture
def db_no_rollback(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)
