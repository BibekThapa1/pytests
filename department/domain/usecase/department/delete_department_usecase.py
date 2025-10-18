from department.domain.entity.department_entity import DepartmentEntity
from department.domain.repo.department_repo import DepartmentRepoAbstract
from typing import Optional

class DeleteDepartmentUsecase:
    def __init__(self, department_repo: DepartmentRepoAbstract):
        self.department_repo = department_repo
        
    def execute(self, department_id: int) -> Optional[bool]:
        return self.department_repo.delete_department(department_id)