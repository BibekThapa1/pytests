import pytest
from department.data.db.department_repo_implementation import DepartmentRepo
from department.domain.entity.department_entity import DepartmentEntity
from department.models import Department

@pytest.mark.django_db
def test_create_department_repo():
    repo = DepartmentRepo()
    entity = DepartmentEntity(name="HR", content="Human Resources", icon="👥")
    created = repo.create_department(entity)

    assert created.id is not None
    assert created.name == "HR"
    assert Department.objects.count() == 1
