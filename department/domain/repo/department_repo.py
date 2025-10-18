from typing import List,Optional
from department.domain.entity.department_entity import DepartmentEntity
from abc import ABC, abstractmethod

class DepartmentRepoAbstract(ABC):
    
    @abstractmethod
    def create_department(self, department_entity: DepartmentEntity) -> Optional[DepartmentEntity]:
        """
        Create a new department
        """
        pass
    
    @abstractmethod
    def update_department(self, department_id: int, updated_data: dict) -> DepartmentEntity:
        """
        Update an existing department
        """
        pass
    
    @abstractmethod
    def delete_department(self,department_id: int) -> Optional[bool]:
        """
        Delete an existing department
        """
        pass
    
    @abstractmethod
    def list_departments(self) -> List[DepartmentEntity]:
        """
        Get all department
        """
        pass
    
    @abstractmethod
    def get_specific_department(self, department_id: int) -> Optional[DepartmentEntity]:
        """
        Get specific department
        """
        pass
