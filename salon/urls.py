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
    AppointmentServiceViewSet,
    EmployeePayrollTurnViewSet,
    PayrollTurnViewSet,
    EmployeePayslipsViewSet
)

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView


router = DefaultRouter()

router.register(r'employees', EmployeeViewSet, )
router.register(r'users', UserViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'nailservicecategories', NailServiceCategoryViewSet)
router.register(r'nailservices', NailServiceViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'appointment-services', AppointmentServiceViewSet)
router.register(r'employee-payroll-turn', EmployeePayrollTurnViewSet)
router.register(r'payroll-turn', PayrollTurnViewSet)
router.register(r'employee-payslips', EmployeePayslipsViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
