from department.domain.entity.department_entity import DepartmentEntity
from department.domain.repo.department_repo import DepartmentRepoAbstract

class CreateDepartmentUsecase:
    def __init__(self, department_repo: DepartmentRepoAbstract):
        self.department_repo = department_repo
        
    def execute(self, department_entity: DepartmentEntity) -> DepartmentEntity:
        return self.department_repo.create_department(department_entity)
    