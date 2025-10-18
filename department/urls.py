from django.urls import path, include

from rest_framework.routers import DefaultRouter

from department.adapter.views.department_view import DepartmentViewSet

router = DefaultRouter()
router.register(r'department', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls))
]