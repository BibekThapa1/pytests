from department.models import Department
from department.adapter.serializers.department_serializer import DepartmentSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action

# Db implementation imports
from department.data.db.department_repo_implementation import DepartmentRepo

# Entity imports 
from department.domain.entity.department_entity import DepartmentEntity

# Usecase imports
from department.domain.usecase.department.create_department_usecase import CreateDepartmentUsecase
from department.domain.usecase.department.delete_department_usecase import DeleteDepartmentUsecase
from department.domain.usecase.department.get_specific_department_usecase import GetSpecificDepartmentUsecase
from department.domain.usecase.department.list_department_usecase import ListDepartmentUsecase
from department.domain.usecase.department.update_department_usecase import UpdateDepartmentUsecase

# Response imports
from utils.response import ResponseMixin

class DepartmentViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.department_repo = DepartmentRepo()
        self.create_department_usecase = CreateDepartmentUsecase(self.department_repo)
        self.delete_department_usecase = DeleteDepartmentUsecase(self.department_repo)
        self.get_specific_department_usecase = GetSpecificDepartmentUsecase(self.department_repo)
        self.list_departments_usecase = ListDepartmentUsecase(self.department_repo)
        self.update_department_usecase = UpdateDepartmentUsecase(self.department_repo)
        
    def create(self,request):
        try:
            serializer = DepartmentSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            department_entity = DepartmentEntity(
                name=validated_data['name'],
                content=validated_data['content'],
                icon= validated_data['icon']
            )
            department = self.create_department_usecase.execute(department_entity)
            
            if department is None:
                return ResponseMixin.error_response(
                    message="Something went wrong while creating department",
                )
            serializer = DepartmentSerializer(department, context={'request': request})
            return ResponseMixin.success_response(
                data=serializer.data,
                message="Department created successfully",
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return ResponseMixin.error_response(
                error=str(e),
                message="Error occurred while creating department",
            )
    
    def retrieve(self, request, pk=None):
        try:
            department = self.get_specific_department_usecase.execute(pk)
            if department is None:
                return ResponseMixin.not_found_response(
                    message="Department not found"
                )
            serializer = DepartmentSerializer(department, context={'request': request})
            return ResponseMixin.success_response(
                data=serializer.data,
                message="Department retrieved successfully",
            )
        except Exception as e:
            return ResponseMixin.error_response(
                error=str(e),
                message="Error occurred while retrieving department",
            )
            
    def partial_update(self, request, pk=None):
        try:
            serializer = DepartmentSerializer(data=request.data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            updated_department = self.update_department_usecase.execute(pk, serializer.validated_data)
            
            if updated_department is None:
                return ResponseMixin.not_found_response(
                    message="Department not found for update"
                )
            serializer = DepartmentSerializer(updated_department, context={'request': request})
            return ResponseMixin.success_response(
                data=serializer.data,
                message="Department updated successfully",
            )
        except Exception as e:
            return ResponseMixin.error_response(
                error=str(e),
                message="Error occurred while updating department",
            )
    
    def destroy(self, request, pk=None):
        try:
            department = self.delete_department_usecase.execute(pk)
            if department is None:
                return ResponseMixin.not_found_response(
                    message="Department not found for deletion"
                )
            
            return ResponseMixin.success_response(
                message="Department deleted successfully",
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return ResponseMixin.error_response(
                error=str(e),
                message="Error occurred while deleting department",
            )

    def list(self, request):
        try:
            departments = self.list_departments_usecase.execute()
            if not departments:
                return ResponseMixin.success_response(
                    data=[],
                    message="No departments found",
                )
            serializer = DepartmentSerializer(departments, many=True, context={'request': request})
            return ResponseMixin.success_response(
                data=serializer.data,
                message="Departments retrieved successfully",
            )
        except Exception as e:
            return ResponseMixin.error_response(
                error=str(e),
                message="Error occurred while retrieving departments",
            )