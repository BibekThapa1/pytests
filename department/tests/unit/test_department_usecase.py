import pytest
from department.domain.entity.department_entity import DepartmentEntity
from department.data.db.department_repo_implementation import DepartmentRepo
from department.domain.usecase.department.create_department_usecase import CreateDepartmentUsecase

@pytest.mark.django_db
def test_create_department_usecase():
    repo = DepartmentRepo()
    usecase = CreateDepartmentUsecase(repo)
    
    entity = DepartmentEntity(name="Finance", content="Handles money", icon="💰")
    created = usecase.execute(entity)
    
    assert created.name == "Finance"
