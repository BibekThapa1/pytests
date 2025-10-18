from department.domain.entity.department_entity import DepartmentEntity
from department.domain.repo.department_repo import DepartmentRepoAbstract

class UpdateDepartmentUsecase:
    def __init__(self, department_repo: DepartmentRepoAbstract):
        self.department_repo = department_repo
        
    def execute(self, department_id: int, updated_data: dict) -> DepartmentEntity:
        return self.department_repo.update_department(department_id,updated_data)