from department.domain.entity.department_entity import DepartmentEntity

def test_department_entity_creation():
    entity = DepartmentEntity(
        content="something",
        name="bibek thapa",
        icon="something",
        id=1
    )
    assert entity.id is None
    assert entity.name == "HR"
    assert entity.content == "Human Resources"
    assert entity.icon == "something"