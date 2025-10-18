import pytest
from department.adapter.serializers.department_serializer import DepartmentSerializer
from department.models import Department

@pytest.mark.django_db
def test_department_serializer_valid_data():
    # Sample valid data
    data = {
        "name": "IT",
        "content": "Information Technology",
        "icon": "it-icon.png"
    }
    serializer = DepartmentSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    assert validated_data["name"] == "IT"
    assert validated_data["content"] == "Information Technology"
    assert validated_data["icon"] == "it-icon.png"

@pytest.mark.django_db
def test_department_serializer_invalid_data():
    # Missing required field 'name'
    data = {
        "content": "Information Technology",
        "icon": "it-icon.png"
    }
    serializer = DepartmentSerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors

@pytest.mark.django_db
def test_department_serializer_serialization():
    # Create a Department instance
    department = Department.objects.create(
        name="HR",
        content="Human Resources",
        icon="hr-icon.png"
    )
    serializer = DepartmentSerializer(department)
    data = serializer.data
    assert data["id"] == department.id
    assert data["name"] == "HR"
    assert data["content"] == "Human Resources"
    assert data["icon"] == "hr-icon.png"
    assert "created_at" in data
    assert "updated_at" in data
