import pytest
import sys
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from rest_framework import status
from unittest.mock import MagicMock
from department.adapter.views.department_view import DepartmentViewSet
from department.domain.entity.department_entity import DepartmentEntity
from rest_framework.viewsets import ViewSet
@pytest.fixture
def api_factory():
    return APIRequestFactory()

@pytest.fixture
def sample_department_entity():
    return DepartmentEntity(
        id=1,
        name="IT",
        content="Information Technology",
        icon="it-icon.png"
    )
    
@pytest.fixture
def viewset():
    view = DepartmentViewSet()
    
    # Mocking all usecases
    view.create_department_usecase = MagicMock()
    view.delete_department_usecase = MagicMock()
    view.get_specific_department_usecase = MagicMock()
    view.list_departments_usecase = MagicMock()
    view.update_department_usecase = MagicMock()
    
    return view

@pytest.mark.django_db
def test_create_department_success(api_factory, viewset: DepartmentViewSet, sample_department_entity):
    # Create the factory request
    factory_request = api_factory.post(
        "/departments/",
        {"name": "IT", "content": "Information Technology", "icon": "it-icon.png"},
        format='json'
    )

    # Set up the action_map (this is what as_view() normally does)
    viewset.action_map = {'post': 'create'}
    viewset.format_kwarg = None
    viewset.action = 'create'

    # Convert to DRF Request
    drf_request = viewset.initialize_request(factory_request)
    viewset.request = drf_request
    
    # Force parse the request data
    drf_request._full_data
    
    # Mock usecase
    viewset.create_department_usecase.execute = MagicMock(return_value=sample_department_entity)
    
    # Call with the DRF request
    response = viewset.create(drf_request)
    
    print(response.data, flush=True)
    print(response.status_code, flush=True)
    sys.stdout.flush()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "Department created successfully"
    assert response.data["data"]["name"] == "IT"
    
@pytest.mark.django_db
def test_create_department_failure(api_factory, viewset):
    request = api_factory.post("/departments/", {
        "name": "IT",
        "content": "Information Technology",
        "icon": "it-icon.png"
    }, format='json')
    
    viewset.create_department_usecase.execute.return_value = None
    
    response = viewset.create(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Something went wrong" in response.data["message"]

# # ------------------ RETRIEVE ------------------
# def test_retrieve_department_success(api_factory, viewset, sample_department_entity):
#     request = api_factory.get("/departments/1/")
#     viewset.get_specific_department_usecase.execute.return_value = sample_department_entity
    
#     response = viewset.retrieve(request, pk=1)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["data"]["id"] == 1

# def test_retrieve_department_not_found(api_factory, viewset):
#     request = api_factory.get("/departments/1/")
#     viewset.get_specific_department_usecase.execute.return_value = None
    
#     response = viewset.retrieve(request, pk=1)
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#     assert "Department not found" in response.data["message"]

# # ------------------ LIST ------------------
# def test_list_departments(api_factory, viewset, sample_department_entity):
#     request = api_factory.get("/departments/")
#     viewset.list_departments_usecase.execute.return_value = [sample_department_entity]
    
#     response = viewset.list(request)
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data["data"]) == 1

# # ------------------ PARTIAL UPDATE ------------------
# def test_partial_update_success(api_factory, viewset, sample_department_entity):
#     request = api_factory.patch("/departments/1/", {"content": "Updated Content"}, format='json')
#     viewset.update_department_usecase.execute.return_value = sample_department_entity
    
#     response = viewset.partial_update(request, pk=1)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.data["data"]["name"] == "IT"

# def test_partial_update_not_found(api_factory, viewset):
#     request = api_factory.patch("/departments/1/", {"content": "Updated Content"}, format='json')
#     viewset.update_department_usecase.execute.return_value = None
    
#     response = viewset.partial_update(request, pk=1)
#     assert response.status_code == status.HTTP_404_NOT_FOUND

# # ------------------ DELETE ------------------
# def test_delete_department_success(api_factory, viewset):
#     request = api_factory.delete("/departments/1/")
#     viewset.delete_department_usecase.execute.return_value = True
    
#     response = viewset.destroy(request, pk=1)
#     assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_delete_department_not_found(api_factory, viewset):
#     request = api_factory.delete("/departments/1/")
#     viewset.delete_department_usecase.execute.return_value = None
    
#     response = viewset.destroy(request, pk=1)
#     assert response.status_code == status.HTTP_404_NOT_FOUND
