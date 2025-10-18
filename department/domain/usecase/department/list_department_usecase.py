from department.domain.entity.department_entity import DepartmentEntity
from department.domain.repo.department_repo import DepartmentRepoAbstract
from typing import List

class ListDepartmentUsecase:
    def __init__(self, department_repo: DepartmentRepoAbstract):
        self.department_repo = department_repo
        
    def execute(self) -> List[DepartmentEntity]:
        return self.department_repo.list_departments()