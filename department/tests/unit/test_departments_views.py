import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from department.models import Department

@pytest.mark.django_db
def test_create_department_api():
    client = APIClient()
    url = reverse("department-list")  # Assuming router registered as 'department'
    
    data = {"name": "Research", "content": "Research Department", "icon": "🔬"}
    response = client.post(url, data, format="json")

    print("Status code:", response.status_code)
    print("Response data:", response.data)  # This shows exactly why 400

    assert response.status_code == 201
    assert response.data["data"]["name"] == "Research"
    assert Department.objects.filter(name="Research").exists()
