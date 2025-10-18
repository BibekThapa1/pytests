from department.domain.entity.department_entity import DepartmentEntity
from department.domain.repo.department_repo import DepartmentRepoAbstract
from department.models import Department
from typing import List, Optional

class DepartmentRepo(DepartmentRepoAbstract):
    def create_department(self, department_entity) -> DepartmentEntity:
        try:
            department_model = DepartmentMapper.to_model(department_entity)
            department_model.save()
            return DepartmentMapper.to_entity(department_model)
        except Exception as e:
            return e 

    def update_department(self, department_id: int, updated_data: dict) -> DepartmentEntity:
        try:
            department_model = Department.objects.get(id=department_id)
            
            ALLOWED_UPDATE_FIELDS = ['name', 'content', 'icon']
            
            for field,value in updated_data.items():
                if field in ALLOWED_UPDATE_FIELDS and value is not None:
                    setattr(department_model, field, value)
                    
            department_model.save()
            return DepartmentMapper.to_entity(department_model)
        
        except Department.DoesNotExist:
            return None
        
    def delete_department(self, department_id: int) -> bool:
        try:
            department_model = Department.objects.get(id = department_id)
            department_model.delete()
            return True
        except Department.DoesNotExist:
            return False
        
    def list_departments(self) -> List[DepartmentEntity]:
        try:
            departments = Department.objects.all()
            departments_entities = [DepartmentMapper.to_entity(department) for department in departments]
            return departments_entities
        except Department.DoesNotExist:
            return []
        
    def get_specific_department(self, department_id:id) -> Optional[DepartmentEntity]:
        try:
            department_model = Department.objects.get(id=department_id)
            return DepartmentMapper.to_entity(department_model)
        except Department.DoesNotExist:
            return None
    
class DepartmentMapper:
    @staticmethod
    def to_entity(department_model: Department) -> DepartmentEntity:
        return DepartmentEntity(
            id = department_model.id,
            name = department_model.name,
            content = department_model.content,
            icon = department_model.icon,
            created_at= department_model.created_at,
            updated_at = department_model.updated_at
        )
        
    @staticmethod
    def to_model(department_entity: DepartmentEntity) -> Department:
        return Department(
            name = department_entity.name,
            content = department_entity.content,
            icon = department_entity.icon,
        )