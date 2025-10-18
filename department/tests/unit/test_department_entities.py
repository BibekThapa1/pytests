from department.domain.entity.department_entity import DepartmentEntity

def test_department_entity_creation():
    entity = DepartmentEntity(
        content="something",
        name="bibek thapa",
        icon="something",
        id=None
    )
    assert entity.id is None
    assert entity.name == "bibek thapa"
    assert entity.content == "something"
    assert entity.icon == "something"