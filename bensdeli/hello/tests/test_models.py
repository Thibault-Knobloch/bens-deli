from hello.models import Person
# from pytest import mark
import pytest


@pytest.mark.django_db
def test_person_save():
    person = Person.objects.create(name="John Doe", age=13)
    assert Person.objects.all().count() == 1
    assert person.id is not None
    assert person.name == "John Doe"