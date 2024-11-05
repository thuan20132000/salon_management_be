from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet,
    UserViewSet,
    SkillViewSet,
    NailServiceCategoryViewSet,
    NailServiceViewSet,
    AppointmentViewSet,
    CustomerViewSet,
    AppointmentServiceViewSet

)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'users', UserViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'nailservicecategories', NailServiceCategoryViewSet)
router.register(r'nailservices', NailServiceViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'appointment-services', AppointmentServiceViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]
